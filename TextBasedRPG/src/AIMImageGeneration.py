import requests
from PIL import Image
from io import BytesIO
from diffusers import DiffusionPipeline
import matplotlib.pyplot as plt
import torch
from typing import Any
from enum import Enum


class GenerationOption(Enum):
    """Enum for card types."""
    ClipDrop = "ClipDrop"
    SDXL = "SDXL"


class SDXLGenerator:

    def __init__(self):
        # Initialize the base pipeline model
        self.basePipe = DiffusionPipeline.from_pretrained("../Models/stable-diffusion-xl-base-1.0",
                                                          torch_dtype=torch.float16,
                                                          use_safetensors=True,
                                                          variant="fp16")
        self.basePipe.to("cuda")

        # Initialize the refiner pipeline model with components from basePipe
        self.refinerPipe = DiffusionPipeline.from_pretrained("../Models/stable-diffusion-xl-refiner-1.0",
                                                             text_encoder_2=self.basePipe.text_encoder_2,
                                                             vae=self.basePipe.vae,
                                                             torch_dtype=torch.float16,
                                                             use_safetensors=True,
                                                             variant="fp16")
        self.refinerPipe.to("cuda")

    def generateSDXLImage(self,
                          prompt: str) -> Any:
        """
        Generates an image based on the given prompt.

        :param prompt: The text prompt for generating the image.
        :return: The generated image.
        """

        # Define the steps and noise fraction
        n_steps = 40
        high_noise_frac = 0.8

        # Generate the base image
        baseImage = self.basePipe(prompt=prompt,
                                  num_inference_steps=n_steps,
                                  denoising_end=high_noise_frac,
                                  output_type="latent").images

        # Refine the image
        refinedImage = self.refinerPipe(prompt=prompt,
                                        num_inference_steps=n_steps,
                                        denoising_start=high_noise_frac,
                                        image=baseImage).images[0]

        return refinedImage


def generateClipDropImage(prompt: str) -> Image:
    clipDropAPIKey: str = "1529f6d30cc7ae8444632a20a1687462f0dd50e5f95ef2369c3c5c46ea74eb51ca61fb204a5c0f6235844cd6e00a0877"

    r = requests.post("https://clipdrop-api.co/text-to-image/v1",
                      files={
                          'prompt': (None, prompt, 'text/plain')
                      },
                      headers={
                          'x-api-key': clipDropAPIKey}

                      )
    if r.ok:
        return Image.open(BytesIO(r.content))
    else:
        r.raise_for_status()
