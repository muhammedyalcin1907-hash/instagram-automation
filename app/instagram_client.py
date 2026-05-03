from __future__ import annotations

from pathlib import Path

import requests

from app.config import settings


class InstagramClient:
    def __init__(self) -> None:
        self.base_url = f"https://graph.facebook.com/{settings.instagram_api_version}"
        self.account_id = settings.instagram_business_account_id
        self.token = settings.instagram_access_token

    def publish_reel(self, video_url: str, caption: str) -> dict:
        if settings.dry_run or not (self.account_id and self.token):
            return {
                "status": "dry_run",
                "creation_id": "dry_run_creation_id",
                "media_id": "dry_run_media_id",
            }

        create_url = f"{self.base_url}/{self.account_id}/media"
        create_resp = requests.post(
            create_url,
            data={
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "share_to_feed": "true",
                "access_token": self.token,
            },
            timeout=30,
        )
        create_resp.raise_for_status()
        creation_id = create_resp.json()["id"]

        publish_url = f"{self.base_url}/{self.account_id}/media_publish"
        publish_resp = requests.post(
            publish_url,
            data={"creation_id": creation_id, "access_token": self.token},
            timeout=30,
        )
        publish_resp.raise_for_status()
        media_id = publish_resp.json()["id"]

        return {"status": "published", "creation_id": creation_id, "media_id": media_id}

    def publish_local_reel(self, local_video_path: Path, caption: str) -> dict:
        # Graph API doğrudan local dosya kabul etmez; public URL gerekir.
        fake_url = f"https://example.com/{local_video_path.name}"
        return self.publish_reel(video_url=fake_url, caption=caption)
