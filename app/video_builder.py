from __future__ import annotations

import subprocess
from pathlib import Path

from app.config import settings


class VideoBuilder:
    def __init__(self) -> None:
        settings.generated_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace("'", "\\'").replace(":", "\\:")

    def build_reel(self, media_path: Path, audio_path: Path, subtitle_text: str, output_name: str) -> Path:
        output_path = settings.generated_dir / output_name
        safe_text = self._escape(subtitle_text)

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(media_path),
            "-i",
            str(audio_path),
            "-vf",
            (
                "scale=1080:1920:force_original_aspect_ratio=decrease,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,"
                f"drawtext=text='{safe_text}':fontcolor=white:fontsize=48:"
                "box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y=h-(text_h*2)"
            ),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)
        return output_path
