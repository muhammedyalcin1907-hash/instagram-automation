from openai import OpenAI
from pathlib import Path
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)


class ImageGenerator:
    def generate_background(self, prompt: str, filename: str) -> Path:
        settings.generated_dir.mkdir(parents=True, exist_ok=True)

        output_path = settings.generated_dir / filename

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1792"
        )

        image_base64 = result.data[0].b64_json

        import base64
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        return output_path
