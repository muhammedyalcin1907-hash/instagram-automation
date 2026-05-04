from __future__ import annotations

import logging
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.content_generator import ContentGenerator
from app.database import ReelHistory, get_db, save_history, init_db
from app.image_generator import ImageGenerator
from app.instagram_client import InstagramClient
from app.scheduler import shutdown_scheduler
from app.tts import TTSService
from app.video_builder import VideoBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

init_db()

content_generator = ContentGenerator()
tts_service = TTSService()
video_builder = VideoBuilder()
instagram_client = InstagramClient()
image_generator = ImageGenerator()


class ReelRequest(BaseModel):
    niche: str = "motivasyon"
    voice_gender: str = "female"
    media_filename: str | None = None
    publish: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/dry-run/test")
def dry_run_test():
    return {"dry_run": settings.dry_run, "status": "ok"}


@app.get("/reels/history")
def list_history(limit: int = 20, db: Session = Depends(get_db)):
    items = db.query(ReelHistory).order_by(ReelHistory.id.desc()).limit(limit).all()
    return {
        "items": [
            {
                "id": i.id,
                "title": i.title,
                "share_status": i.share_status,
                "media_path": i.media_path,
                "created_at": i.created_at.isoformat() if i.created_at else None,
            }
            for i in items
        ]
    }


@app.get("/reels/history/{history_id}")
def get_history(history_id: int, db: Session = Depends(get_db)):
    item = db.query(ReelHistory).filter(ReelHistory.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="History item not found")

    return {
        "id": item.id,
        "hook": item.hook,
        "script": item.script,
        "title": item.title,
        "caption": item.caption,
        "hashtags": item.hashtags,
        "media_path": item.media_path,
        "share_status": item.share_status,
        "created_at": item.created_at.isoformat() if item.created_at else None,
    }


@app.post("/reels/generate")
def generate_reel(req: ReelRequest, db: Session = Depends(get_db)):
    try:
        content = content_generator.generate_daily(req.niche)

        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        try:
            audio_path = settings.generated_dir / f"voice_{ts}.mp3"
            tts_service.synthesize(
                text=content.script,
                output_path=audio_path,
                voice_gender=req.voice_gender,
            )
        except Exception as e:
            logger.warning("TTS failed, continuing without audio: %s", e)
            audio_path = None

        scene_images = image_generator.generate_dark_cinematic_scenes(
            niche=req.niche,
            ts=ts,
        )

        subtitle_lines = [
            line.strip()
            for line in content.script.replace("!", ".").replace("?", ".").split(".")
            if line.strip()
        ]

        final_video = video_builder.build_cinematic_reel(
            image_paths=scene_images,
            subtitle_lines=subtitle_lines,
            output_name=f"reel_{ts}.mp4",
        )

        publish_result = {"status": "prepared"}

        if req.publish:
            publish_result = instagram_client.publish_local(
                local_video_path=final_video,
                caption=f"{content.caption}\n\n{content.hashtags}",
            )

        history = save_history(
            db,
            {
                "hook": content.hook,
                "script": content.script,
                "title": content.title,
                "caption": content.caption,
                "hashtags": content.hashtags,
                "media_path": str(final_video),
                "share_status": publish_result["status"],
            },
        )

        filename = str(final_video).split("/")[-1]

        return {
            "status": "success",
            "id": history.id,
            "title": content.title,
            "caption": content.caption,
            "hashtags": content.hashtags,
            "video": str(final_video),
            "download_url": f"/download/{filename}",
            "publish": publish_result,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Generate reel failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = settings.generated_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename,
    )


@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()
