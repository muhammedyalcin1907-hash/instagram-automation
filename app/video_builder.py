from __future__ import annotations

import subprocess
from pathlib import Path

from app.config import settings


class VideoBuilder:
    def build_reel(
        self,
        media_path: Path,
        audio_path: Path | None,
        subtitle_text: str,
        output_name: str,
    ) -> Path:
        return self.build_reel_with_generated_background(
            audio_path=audio_path,
            subtitle_text=subtitle_text,
            output_name=output_name,
        )

    def build_reel_with_generated_background(
        self,
        audio_path: Path | None,
        subtitle_text: str,
        output_name: str,
    ) -> Path:
        settings.generated_dir.mkdir(parents=True, exist_ok=True)
        output_path = settings.generated_dir / output_name

        safe_text = subtitle_text.replace(":", "\\:").replace("'", "\\'").replace("\n", " ")

        filter_complex = (
            "drawtext="
            f"text='{safe_text}':"
            "fontcolor=white:"
            "fontsize=28:"
            "box=1:"
            "boxcolor=black@0.45:"
            "boxborderw=10:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2"
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=#4f46e5:s=720x1280:r=24",
        ]

        if audio_path and Path(audio_path).exists():
            cmd += ["-i", str(audio_path)]
            cmd += ["-shortest"]

        cmd += [
            "-vf",
            filter_complex,
            "-t",
            "8",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)

        return output_path
