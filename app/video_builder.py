from __future__ import annotations

import subprocess
from pathlib import Path

from app.config import settings


def clean_text(text: str) -> str:
    return (
        text.replace("'", "")
        .replace('"', "")
        .replace(":", "")
        .replace(",", "")
        .replace(";", "")
        .replace("\\", "")
        .replace("\n", " ")
        .strip()
    )


class VideoBuilder:
    def build_cinematic_reel(
        self,
        image_paths: list[Path],
        subtitle_lines: list[str],
        output_name: str,
    ) -> Path:
        settings.generated_dir.mkdir(parents=True, exist_ok=True)
        output_path = settings.generated_dir / output_name

        duration_per_scene = 3
        inputs = []
        filters = []

        for i, img in enumerate(image_paths):
            inputs += ["-loop", "1", "-t", str(duration_per_scene), "-i", str(img)]

            filters.append(
                f"[{i}:v]"
                "scale=1080:1920,"
                "zoompan=z='min(zoom+0.0015,1.2)':"
                "d=75:"
                "x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)'"
                f"[v{i}]"
            )

        concat_inputs = "".join([f"[v{i}]" for i in range(len(image_paths))])
        filters.append(f"{concat_inputs}concat=n={len(image_paths)}:v=1:a=0[v]")

        full_text = clean_text(" ".join(subtitle_lines))[:160]

        filters.append(
            f"[v]drawtext=text='{full_text}':"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            "fontcolor=white:"
            "fontsize=46:"
            "box=1:"
            "boxcolor=black@0.55:"
            "boxborderw=14:"
            "x=(w-text_w)/2:"
            "y=h*0.74"
            "[outv]"
        )

        cmd = [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)
        return output_path
