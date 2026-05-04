from pathlib import Path
import random
import subprocess
from app.config import settings


class VideoBuilder:
    def build_reel_with_generated_background(self, audio_path, subtitle_text, output_name):
        settings.generated_dir.mkdir(parents=True, exist_ok=True)
        output_path = settings.generated_dir / output_name

        quotes = [
            ("Bitti dediğin yer", "BAŞLADIĞIN YERDİR"),
            ("Kimse seni kurtarmayacak", "KENDİN BAŞLA"),
            ("Motivasyon biter", "DİSİPLİN KALIR"),
            ("Sessiz çalış", "SONUÇLAR KONUŞSUN"),
            ("Zor geliyorsa", "DEĞİŞİYORSUN"),
        ]

        top, main = random.choice(quotes)

        vf = (
            "colorchannelmixer=aa=1,"
            f"drawtext=text='{top}':"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
            "fontcolor=white@0.92:"
            "fontsize=52:"
            "x=70:"
            "y=h*0.42,"
            f"drawtext=text='{main}':"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            "fontcolor=white:"
            "fontsize=60:"
            "x=70:"
            "y=h*0.47,"
            "drawtext=text='-Aireelsotoman':"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
            "fontcolor=white@0.35:"
            "fontsize=34:"
            "x=w-text_w-90:"
            "y=h-170"
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "color=c=black:s=1080x1920:d=7:r=24",
            "-vf", vf,
            "-t", "7",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)
        return output_path

    def build_reel(self, media_path, audio_path, subtitle_text, output_name):
        return self.build_reel_with_generated_background(audio_path, subtitle_text, output_name)
        
