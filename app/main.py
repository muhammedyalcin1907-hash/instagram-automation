from __future__ import annotations

import logging
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.content_generator import ContentGenerator
from app.database import ReelHistory, get_db, init_db, save_history
from app.instagram_client import InstagramClient
from app.scheduler import shutdown_scheduler, start_scheduler
from app.tts import TTSService
from app.video_builder import VideoBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    filename="app.log",
)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

content_generator = ContentGenerator()
tts_service = TTSService()
video_builder = VideoBuilder()
instagram_client = InstagramClient()


class ReelRequest(BaseModel):
    niche: str = Field(default="motivasyon", examples=["motivasyon"])
    voice_gender: str = Field(default="female", examples=["female", "male"])
    media_filename: str | None = Field(default=None, examples=[None, "sample.mp4"])
    publish: bool = Field(default=False, examples=[False])
    niche: str = "kişisel gelişim"
    voice_gender: str = "female"
    media_filename: str | None = None
    media_filename: str
    publish: bool = False


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    settings.generated_dir.mkdir(parents=True, exist_ok=True)
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown() -> None:
    shutdown_scheduler()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.env, "dry_run": settings.dry_run}


@app.get("/dry-run/test")
def dry_run_test() -> dict:
    result = instagram_client.publish_reel("https://example.com/video.mp4", "dry run test")
    return {"dry_run": settings.dry_run, "result": result}


@app.get("/reels/history")
def list_history(limit: int = 20, db: Session = Depends(get_db)) -> dict:
    items = db.query(ReelHistory).order_by(ReelHistory.id.desc()).limit(limit).all()
    return {
        "items": [
            {
                "id": i.id,
                "title": i.title,
                "share_status": i.share_status,
                "media_path": i.media_path,
                "created_at": i.created_at.isoformat(),
            }
            for i in items
        ]
    }


@app.post("/reels/generate")
def generate_reel(req: ReelRequest, db: Session = Depends(get_db)) -> dict:
 try:

    content = content_generator.generate_daily(...)

    ts = datetime.utcnow().strftime(...)

    audio_path = settings.generated_dir / ...

    tts_service.synthesize(...)

                    if req.media_filename:
            media_path = settings.uploads_dir / req.media_filename

            if not media_path.exists():
                raise HTTPException(status_code=404, detail="Media not found")

            final_video = video_builder.build_reel(
                media_path=media_path,
                audio_path=audio_path,
                subtitle_text=content.script,
                output_name=f"reel_{ts}.mp4",
            )

        else:
            final_video = video_builder.build_reel_with_generated_background(
                audio_path=audio_path,
                subtitle_text=content.script,
                output_name=f"reel_{ts}.mp4",
            )
    

        publish_result = {"status": "prepared"}
        if req.publish:
            publish_result = instagram_client.publish_local_reel(
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
                "instagram_creation_id": publish_result.get("creation_id"),
                "instagram_media_id": publish_result.get("media_id"),
                "dry_run": settings.dry_run,
            },
        )

        return {
            "content": content.__dict__,
            "audio_path": str(audio_path),
            "video_path": str(final_video),
            "publish_result": publish_result,
            "history_id": history.id,
        }
    except Exception as exc:
        logger.exception("Reel generation failed")
        raise HTTPException(status_code=500, detail=f"Reel generation failed: {exc}") from exc


@app.get("/reels/history/{history_id}")
def get_history(history_id: int, db: Session = Depends(get_db)) -> dict:
    item = db.query(ReelHistory).filter(ReelHistory.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="History item not found")
    return {
        "id": item.id,
        "title": item.title,
        "caption": item.caption,
        "hashtags": item.hashtags,
        "media_path": item.media_path,
        "share_status": item.share_status,
        "created_at": item.created_at.isoformat(),
    }
