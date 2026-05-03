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
        duration = 8
        width = 720
        height = 1280

        sentences = [s.strip() for s in subtitle_text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        if not sentences:
            sentences = ["Bugün başla."]

        text_files = []
        drawtexts = []

        for i, sentence in enumerate(sentences[:5]):
            text_path = settings.generated_dir / f"text_{i}_{output_name}.txt"
            text_path.write_text(sentence, encoding="utf-8")
            text_files.append(text_path)

            start = 0 if i == 0 else 2 + (i - 1) * 1.5
            end = 2 if i == 0 else start + 1.5
            fontsize = 46 if i == 0 else 34
            y_pos = "h*0.32" if i == 0 else "h*0.58"

            drawtexts.append(
                "drawtext="
                f"textfile='{text_path}':"
                "fontcolor=white:"
                f"fontsize={fontsize}:"
                "box=1:"
                "boxcolor=black@0.55:"
                "boxborderw=12:"
                "x=(w-text_w)/2:"
                f"y={y_pos}:"
                f"enable='between(t,{start},{end})'"
            )

        vf = ",".join(drawtexts)

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", f"color=c=#0f172a:s={width}x{height}:d={duration}:r=24",
        ]

        if audio_path and Path(audio_path).exists():
            cmd += ["-i", str(audio_path), "-shortest"]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

        cmd += [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-movflags", "+faststart",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)

        return output_path
