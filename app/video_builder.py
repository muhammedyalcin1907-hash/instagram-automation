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

    def _run(self, cmd: list[str]) -> None:
        subprocess.run(cmd, check=True)

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
        self._run(cmd)
        return output_path

    def build_reel_with_generated_background(
        self,
        audio_path: Path,
        subtitle_text: str,
        output_name: str,
    ) -> Path:
        output_path = settings.generated_dir / output_name
        safe_text = self._escape(subtitle_text)

        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=#4f46e5:s=1080x1920:r=30",
            "testsrc2=size=1080x1920:rate=30",
            "-i",
            str(audio_path),
            "-filter_complex",
            (
                "[0:v]drawbox=x=0:y=0:w=iw:h=ih:color=#0ea5e9@0.35:t=fill,"
                "drawbox=x=0:y=ih*0.55:w=iw:h=ih*0.45:color=#9333ea@0.40:t=fill,"
                "eq=saturation=1.2:contrast=1.1,"
                "[0:v]boxblur=2:1,eq=saturation=1.3:contrast=1.1,"
                f"drawtext=text='{safe_text}':fontcolor=white:fontsize=48:"
                "box=1:boxcolor=black@0.45:boxborderw=10:x=(w-text_w)/2:y=h-(text_h*2)[v]"
            ),
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
        self._run(cmd)
        subprocess.run(cmd, check=True)
        return output_path
