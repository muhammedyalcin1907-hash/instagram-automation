from __future__ import annotations

import subprocess
from pathlib import Path
from app.config import settings


class VideoBuilder:
    def build_reel_with_generated_background(
        self,
        audio_path: Path | None,
        subtitle_text: str,
        output_name: str,
    ) -> Path:
        output_path = settings.generated_dir / output_name

        width = 720
        height = 1280
        duration = 8

        # Script'i cümlelere böl
        sentences = [s.strip() for s in subtitle_text.split(".") if s.strip()]

        # Her cümleye süre ver
        per_sentence_time = max(1.5, duration / max(len(sentences), 1))

        drawtexts = []

        # İlk hook (büyük)
        if sentences:
            drawtexts.append(
                f"drawtext=text='{sentences[0]}':fontcolor=white:fontsize=50:"
                f"x=(w-text_w)/2:y=h*0.3:enable='between(t,0,2)'"
            )

        # Diğer cümleler sırayla gelsin
        for i, sentence in enumerate(sentences[1:], start=1):
            start = 2 + (i - 1) * per_sentence_time
            end = start + per_sentence_time

            drawtexts.append(
                f"drawtext=text='{sentence}':fontcolor=white:fontsize=36:"
                f"x=(w-text_w)/2:y=h*0.6:"
                f"enable='between(t,{start},{end})'"
            )

        drawtext_filter = ",".join(drawtexts)

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", f"color=c=#0f172a:s={width}x{height}:d={duration}",
        ]

        if audio_path:
            cmd += ["-i", str(audio_path)]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc"]

        cmd += [
            "-vf", drawtext_filter,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-shortest",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)

        return output_path
