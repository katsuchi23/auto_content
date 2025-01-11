"""
Image Generator Module
Handles image generation using Stable Diffusion
"""

import torch
from diffusers import DiffusionPipeline, LCMScheduler
import os
from src.utils.ensure_output_dir import ensure_output_dirs
from pathlib import Path

class ImageGenerator:
    def __init__(self, style="pixel"):
        """
        Initialize the image generator with specified style
        Args:
            style (str): Either "pixel" or "papercut"
        """
        self.style = style
        self.image_generator = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16"
        ).to("cuda")
        
        self._setup_model()
        ensure_output_dirs()

    def _setup_model(self):
        """Set up the model with appropriate style and configurations"""
        self.image_generator.scheduler = LCMScheduler.from_config(
            self.image_generator.scheduler.config
        )
        self.image_generator.load_lora_weights(
            "latent-consistency/lcm-lora-sdxl",
            adapter_name="lcm"
        )
        
        if self.style == "pixel":
            self.image_generator.load_lora_weights(
                "nerijs/pixel-art-xl",
                adapter_name="pixel"
            )
            self.image_generator.set_adapters(
                ["lcm", "pixel"],
                adapter_weights=[1.0, 1.2]
            )
        elif self.style == "papercut":
            self.image_generator.load_lora_weights(
                "TheLastBen/Papercut_SDXL",
                weight_name="papercut.safetensors",
                adapter_name="papercut"
            )
            self.image_generator.set_adapters(
                ["lcm", "papercut"],
                adapter_weights=[1.0, 0.8]
            )

    def generate_images(self, script):
        """
        Generate images from script text
        Args:
            script (str): Input text to generate images from
        Returns:
            list: List of metadata for generated images
        """
        sentences = [s.strip() + '.' for s in script.split('.') if s.strip()]
        image_metadata = []

        for i, sentence in enumerate(sentences):
            print(f"\nGenerating image for sentence {i+1}/{len(sentences)}:")
            print(f"Text: {sentence}")
            
            image = self._generate_image_chunk(sentence)
            image_path = Path("src/output/images") / f"chunk_{i}.png"
            image.save(image_path)
            
            image_metadata.append({
                "chunk_index": i,
                "text": sentence,
                "image_path": str(image_path)
            })
        
        self._cleanup()
        return image_metadata

    def _generate_image_chunk(self, text):
        """Generate a single image from text"""
        negative_prompt = "3d render, realistic"
        enhanced_prompt = self._enhance_prompt(text)
        generator = torch.manual_seed(0)
        
        image = self.image_generator(
            enhanced_prompt,
            num_inference_steps=8,
            height=1920,
            width=1080,
            guidance_scale=1,
            generator=generator,
            negative_prompt=negative_prompt
        ).images[0]
        
        return image

    def _enhance_prompt(self, text):
        """Enhance the prompt with style-specific additions"""
        base_prompt = text[:200]
        return f"{base_prompt}, {self.style}"

    def _cleanup(self):
        """Clean up GPU memory"""
        torch.cuda.empty_cache()
        del self.image_generator
        torch.cuda.empty_cache()