from pathlib import Path
import subprocess


class VideoBuilder:
    def build_reel_with_generated_background(
        self,
        audio_path,
        subtitle_text,
        output_name,
    ):
        output_path = Path("/app/generated") / output_name

        # basit tek renk background
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "color=c=black:s=1080x1920:d=6",

            "-vf",
            "drawtext=text='Bugun basla':"
            "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            "fontcolor=white:"
            "fontsize=60:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2",

            "-pix_fmt", "yuv420p",
            str(output_path),
        ]

        subprocess.run(cmd, check=True)

        return output_path
