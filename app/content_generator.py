from __future__ import annotations

import json
from dataclasses import dataclass

from openai import OpenAI

from app.config import settings


@dataclass
class ReelContent:
    idea: str
    hook: str
    script: str
    title: str
    caption: str
    hashtags: str


class ContentGenerator:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def _fallback(self, niche: str) -> ReelContent:
        return ReelContent(
            idea=f"{niche} için hızlı günlük motivasyon fikri",
            hook="Bugün 30 saniyede hayatını değiştirecek bir fikir öğren!",
            script=(
                "Her gün sadece 10 dakika odaklı çalışma, uzun vadede büyük fark yaratır. "
                "Telefonunu sessize al, tek bir hedef seç ve hemen başla."
            ),
            title="10 Dakika Kuralı ile Verimlilik",
            caption="Küçük adımlar büyük sonuçlar getirir. Bugün dene.",
            hashtags="#reels #motivasyon #kişiselgelişim #verimlilik #alışkanlık",
        )

    def generate_daily_reel(self, niche: str = "kişisel gelişim") -> ReelContent:
        if not self.client:
            return self._fallback(niche)

        prompt = (
            "Sen bir Türkçe Reels içerik editörüsün. Sadece geçerli JSON döndür. "
            "JSON alanları: idea, hook, script, title, caption, hashtags. "
            "Hook kısa ve vurucu olsun. Script maksimum 120 kelime olsun. "
            f"Niş: {niche}"
        )
        response = self.client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )
        text = (response.output_text or "").strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()

        try:
            data = json.loads(text)
            return ReelContent(**data)
        except Exception:
            return self._fallback(niche)
