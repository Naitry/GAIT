# !pip install opencv-python transformers accelerate
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel, AutoencoderKL
from diffusers.utils import load_image
import numpy as np
import torch

import cv2
from PIL import Image

prompt = "A stylized blank trading card in the theme of The Lord of the Rings with a well defined border art, " \
         "Trading Card Game, Magic the Gathering, Yu-Gi-Oh --style fine art, UHD, painted"
negative_prompt = "Poor Quality, Characters, People, text, numbers, letters, blurry, out of focus"

# download an image
image = load_image("../Media/ControlNetsImages/CardTest.png")

# initialize the models and pipeline
controlnet_conditioning_scale = 0.5  # recommended for good generalization
controlnet = ControlNetModel.from_pretrained(
    "../Models/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16
)
vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "../Models/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    vae=vae,
    torch_dtype=torch.float16
)
pipe.enable_model_cpu_offload()

# generate image
image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    guidance_scale=30.0,
    controlnet_conditioning_scale=1.5,
    num_inference_steps=50,
    image=image
).images[0]

image.show()
