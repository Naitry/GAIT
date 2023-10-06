import torch
from PIL import Image
import random
from diffusers import (
    AutoencoderKL,
    StableDiffusionControlNetPipeline,
    StableDiffusionXLControlNetPipeline,
    ControlNetModel,
    StableDiffusionControlNetImg2ImgPipeline,
    DPMSolverMultistepScheduler,  # <-- Added import
    EulerDiscreteScheduler  # <-- Added import
)
import time
from torchvision.transforms import ToPILImage
from torchvision.transforms import Pad

BASE_MODEL = "../Models/stable-diffusion-xl-base-1.0"

# Initialize both pipelines
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)
controlnet = ControlNetModel.from_pretrained("monster-labs/control_v1p_sd15_qrcode_monster", torch_dtype=torch.float16)
main_pipe = StableDiffusionControlNetPipeline.from_pretrained(
    pretrained_model_name_or_path=BASE_MODEL,
    vae=vae,
    controlnet=controlnet,
    safety_checker=None,
    torch_dtype=torch.float16,
).to("cuda")
image_pipe = StableDiffusionControlNetImg2ImgPipeline(**main_pipe.components)

# Sampler map
SAMPLER_MAP = {
    "DPM++ Karras SDE": lambda config: DPMSolverMultistepScheduler.from_config(config, use_karras=True,
                                                                               algorithm_type="sde-dpmsolver++"),
    "Euler": lambda config: EulerDiscreteScheduler.from_config(config),
}


def center_crop_resize(img, output_size=(512, 512)):
    width, height = img.size

    # Calculate dimensions to crop to the center
    new_dimension = min(width, height)
    left = (width - new_dimension) / 2
    top = (height - new_dimension) / 2
    right = (width + new_dimension) / 2
    bottom = (height + new_dimension) / 2

    # Crop and resize
    img = img.crop((left, top, right, bottom))
    img = img.resize(output_size)

    return img


def aspect_fit_resize(img: Image.Image, output_size=(512, 512)) -> Image.Image:
    """
    Resize the image while maintaining its aspect ratio to fit into the output dimensions.
    :param img: Input PIL Image
    :param output_size: Tuple containing the output width and height
    :return: Resized PIL Image
    """
    width, height = img.size
    aspect_ratio = width / height

    new_width, new_height = output_size
    new_aspect_ratio = new_width / new_height

    if aspect_ratio > new_aspect_ratio:
        # Original image is wider than the target dimensions
        new_height = int(new_width / aspect_ratio)
    else:
        # Original image is taller than the target dimensions
        new_width = int(new_height * aspect_ratio)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    return img


def pad_to_desired(img: Image.Image, desired_size=(512, 512)) -> Image.Image:
    """
    Pad the image to the desired dimensions.
    :param img: Input PIL Image
    :param desired_size: Tuple containing the desired width and height
    :return: Padded PIL Image
    """
    img_w, img_h = img.size
    pad_w = desired_size[0] - img_w
    pad_h = desired_size[1] - img_h

    padding = (pad_w // 2, pad_h // 2, pad_w - (pad_w // 2), pad_h - (pad_h // 2))
    return Pad(padding)(img)


def common_upscale(samples, width, height, upscale_method, crop=False):
    if crop == "center":
        old_width = samples.shape[3]
        old_height = samples.shape[2]
        old_aspect = old_width / old_height
        new_aspect = width / height
        x = 0
        y = 0
        if old_aspect > new_aspect:
            x = round((old_width - old_width * (new_aspect / old_aspect)) / 2)
        elif old_aspect < new_aspect:
            y = round((old_height - old_height * (old_aspect / new_aspect)) / 2)
        s = samples[:, :, y:old_height - y, x:old_width - x]
    else:
        s = samples

    return torch.nn.functional.interpolate(s, size=(height, width), mode=upscale_method)


def upscale(samples, upscale_method, scale_by):
    # s = samples.copy()
    width = round(samples["images"].shape[3] * scale_by)
    height = round(samples["images"].shape[2] * scale_by)
    s = common_upscale(samples["images"], width, height, upscale_method, "disabled")
    return (s)


# Inference function
def inference(
        controlImage: Image.Image,
        prompt: str,
        negative_prompt: str,
        guidance_scale: float = 8.0,
        controlnet_conditioning_scale: float = 2.5,
        control_guidance_start: float = 0.0,
        control_guidance_end: float = 1,
        upscaler_strength: float = 0.5,
        seed: int = -1,
        sampler="DPM++ Karras SDE",
) -> torch.Tensor:
    start_time = time.time()
    start_time_struct = time.localtime(start_time)
    start_time_formatted = time.strftime("%H:%M:%S", start_time_struct)
    print(f"Inference started at {start_time_formatted}")

    # Generate the initial image
    # init_image = init_pipe(prompt).images[0]

    # Rest of your existing code
    control_image_small = center_crop_resize(controlImage)
    control_image_large = aspect_fit_resize(controlImage, (1024, 1024))
    control_image_padded = pad_to_desired(control_image_large, (1024, 1024))

    # try:
    #     control_image_padded = control_image_padded.convert("RGB")
    #     control_image_padded.show()
    # except Exception as e:
    #     print(f"An error occurred while converting or showing the image: {e}")

    print(control_image_padded.size)
    main_pipe.scheduler = SAMPLER_MAP[sampler](main_pipe.scheduler.config)
    my_seed = random.randint(0, 2 ** 32 - 1) if seed == -1 else seed
    generator = torch.Generator(device="cuda").manual_seed(my_seed)

    out = main_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=control_image_small,
        guidance_scale=float(guidance_scale),
        controlnet_conditioning_scale=float(controlnet_conditioning_scale),
        generator=generator,
        control_guidance_start=float(control_guidance_start),
        control_guidance_end=float(control_guidance_end),
        num_inference_steps=80,
        output_type="latent"
    )
    upscaled_latents = upscale(out, "nearest-exact", 2)
    out_image = image_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        control_image=control_image_padded,
        image=upscaled_latents,
        guidance_scale=float(guidance_scale),
        generator=generator,
        num_inference_steps=80,
        strength=upscaler_strength,
        control_guidance_start=float(control_guidance_start),
        control_guidance_end=float(control_guidance_end),
        controlnet_conditioning_scale=float(controlnet_conditioning_scale)
    )
    end_time = time.time()
    end_time_struct = time.localtime(end_time)
    end_time_formatted = time.strftime("%H:%M:%S", end_time_struct)
    print(f"Inference ended at {end_time_formatted}, taking {end_time - start_time}s")
    return out_image["images"][0]


if __name__ == "__main__":
    controlImage = Image.open("../Media/ControlNetsImages/CardTest.png")
    output_image = inference(controlImage=controlImage,
                             prompt="A stylized blank trading card in the theme of Harry Potter with a well defined border art, Trading Card Game, Magic the Gathering, Yu-Gi-Oh --style fine art, UHD, painted",
                             negative_prompt="Poor Quality, Characters, People, text, numbers, letters, blurry, out of focus",
                             guidance_scale=30.0)

    # Check if output_image is actually a PIL.Image.Image
    if isinstance(output_image, Image.Image):
        # Directly display the image
        output_image.show()
    else:
        print("Debug: output_image type:", type(output_image))
