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
        duration = 9
        width = 720
        height = 1280

        sentences = [
            s.strip()
            for s in subtitle_text.replace("!", ".").replace("?", ".").split(".")
            if s.strip()
        ]

        if not sentences:
            sentences = ["Bugün başla."]

        sentences = sentences[:5]

        text_files = []
        drawtexts = []

        # Hook text: first sentence, big impact
        for i, sentence in enumerate(sentences):
            text_path = settings.generated_dir / f"text_{i}_{output_name}.txt"
            text_path.write_text(sentence, encoding="utf-8")
            text_files.append(text_path)

            if i == 0:
                start = 0
                end = 2.2
                fontsize = 44
                y_pos = "h*0.34"
                boxcolor = "black@0.65"
            else:
                start = 2.2 + (i - 1) * 1.55
                end = start + 1.55
                fontsize = 32
                y_pos = "h*0.58"
                boxcolor = "black@0.50"

            drawtexts.append(
                "drawtext="
                f"textfile='{text_path}':"
                "fontcolor=white:"
                f"fontsize={fontsize}:"
                "font='DejaVu Sans':"
                "box=1:"
                f"boxcolor={boxcolor}:"
                "boxborderw=14:"
                "x=(w-text_w)/2:"
                f"y={y_pos}:"
                f"enable='between(t,{start},{end})'"
            )

        brand_path = settings.generated_dir / f"brand_{output_name}.txt"
        brand_path.write_text("@Aireelsotoman", encoding="utf-8")

        drawtexts.append(
            "drawtext="
            f"textfile='{brand_path}':"
            "fontcolor=white@0.85:"
            "fontsize=22:"
            "font='DejaVu Sans':"
            "x=w-text_w-35:"
            "y=h-70"
        )

        vf = (
            "format=rgb24,"
            "geq="
            "r='80+70*sin(2*PI*(X/W)+T*0.8)+35*sin(2*PI*(Y/H)+T*0.4)':"
            "g='25+45*sin(2*PI*(X/W)+T*0.5)+25*sin(T*1.2)':"
            "b='120+80*sin(2*PI*(Y/H)+T*0.7)+35*sin(2*PI*(X/W)+T*0.3)',"
            "boxblur=12:1,"
            "eq=contrast=1.25:saturation=1.35:brightness=-0.05,"
            "vignette=PI/4,"
            "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.12:t=fill,"
            + ",".join(drawtexts)
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"nullsrc=s={width}x{height}:d={duration}:r=24",
        ]

        if audio_path and Path(audio_path).exists():
            cmd += ["-i", str(audio_path), "-shortest"]
        else:
            cmd += [
                "-f",
                "lavfi",
                "-i",
                "anullsrc=channel_layout=stereo:sample_rate=44100",
            ]

        cmd += [
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-t",
            str(duration),
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-movflags",
            "+faststart",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)
        return output_path
