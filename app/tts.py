from __future__ import annotations

import subprocess
from pathlib import Path

from openai import OpenAI

from app.config import settings


class TTSService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def _create_silent_audio(self, output_path: Path, duration: int = 6) -> Path:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=44100:cl=stereo",
                "-t",
                str(duration),
                "-q:a",
                "9",
                "-acodec",
                "libmp3lame",
                str(output_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output_path

    def synthesize(self, text: str, output_path: Path, gender: str = "female") -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.client:
            return self._create_silent_audio(output_path)

        voice = settings.tts_voice_female if gender.lower() == "female" else settings.tts_voice_male
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model=settings.tts_model,
                voice=voice,
                input=text,
                format="mp3",
            ) as response:
                response.stream_to_file(output_path)
            return output_path
        except Exception:
            return self._create_silent_audio(output_path)
