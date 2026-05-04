from pathlib import Path
import random
import subprocess
from app.config import settings


class VideoBuilder:
    def build_reel_with_generated_background(
        self,
        audio_path,
        subtitle_text,
        output_name,
    ):
        settings.generated_dir.mkdir(parents=True, exist_ok=True)
        output_path = settings.generated_dir / output_name

        messages = [
            "Kimse seni kurtarmayacak\\nKendin başla",
            "Motivasyon bekleme\\nDisiplin kur",
            "Sessiz çalış\\nSonuçlar konuşsun",
            "Bugün zor mu?\\nİyi. Büyüyorsun",
            "Hayatını değiştirmek için\\nBUGÜN başla",
        ]

        text = random.choice(messages)

        backgrounds = [
            "gradient",
            "dark",
            "gold",
            "blue",
        ]

        bg = random.choice(backgrounds)

        if bg == "gradient":
            source = "testsrc2=s=1080x1920:d=7:r=24"
        elif bg == "gold":
            source = "color=c=#1a120b:s=1080x1920:d=7:r=24"
        elif bg == "blue":
            source = "color=c=#020617:s=1080x1920:d=7:r=24"
        else:
            source = "color=c=black:s=1080x1920:d=7:r=24"

        vf = (
            "eq=contrast=1.25:brightness=-0.04,"
            "vignette=PI/4,"
            f"drawtext=text='{text}':"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            "fontcolor=white:"
            "fontsize=72:"
            "line_spacing=18:"
            "box=1:"
            "boxcolor=black@0.55:"
            "boxborderw=24:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2"
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", source,
            "-vf", vf,
            "-t", "7",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)
        return output_path

    def build_reel(
        self,
        media_path,
        audio_path,
        subtitle_text,
        output_name,
    ):
        return self.build_reel_with_generated_background(
            audio_path=audio_path,
            subtitle_text=subtitle_text,
            output_name=output_name,
        )
