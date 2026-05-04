from __future__ import annotations

import base64
from pathlib import Path

from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.openai_api_key)


class ImageGenerator:
    def generate_background(self, prompt: str, filename: str) -> Path:
        settings.generated_dir.mkdir(parents=True, exist_ok=True)

        output_path = settings.generated_dir / filename

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1536",
        )

        image_base64 = result.data[0].b64_json

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        return output_path

    def generate_dark_cinematic_scenes(self, niche: str, ts: str) -> list[Path]:
        prompts = [
            f"""
            dark cinematic motivation scene, lonely ambitious man walking at night,
            rainy city street, neon reflections, black hoodie, luxury lifestyle mood,
            {niche}, realistic photography, dramatic lighting, 9:16 vertical
            """,
            f"""
            dark cinematic luxury car scene at night, wet asphalt, neon lights,
            powerful success motivation atmosphere, premium lifestyle, no text,
            {niche}, realistic photo, high contrast, 9:16 vertical
            """,
            f"""
            cinematic gym discipline scene, athlete training alone at night,
            dramatic shadows, sweat, focus, ambition, dark moody aesthetic,
            {niche}, realistic photography, 9:16 vertical
            """,
        ]

        paths: list[Path] = []

        for i, prompt in enumerate(prompts, start=1):
            paths.append(
                self.generate_background(
                    prompt=prompt,
                    filename=f"scene_{i}_{ts}.png",
                )
            )

        return paths
