from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReelContent:
    hook: str
    script: str
    title: str
    caption: str
    hashtags: str


class ContentGenerator:
    def generate_daily(self, niche: str = "motivasyon") -> ReelContent:
        niche = niche or "motivasyon"

        hook = f"{niche.title()} için bugün bunu duyman gerekiyordu."
        script = (
            f"{niche} konusunda ilerlemek istiyorsan küçük ama sürekli adımlar atmalısın. "
            "Bugün sadece bir şeyi seç, erteleme ve uygula. "
            "Başarı büyük hamlelerden değil, her gün tekrarlanan doğru alışkanlıklardan gelir."
        )
        title = f"{niche.title()} Reels"
        caption = f"{hook}\n\n{script}"
        hashtags = "#motivasyon #basari #gelisim #reels #aireelsotoman"

        return ReelContent(
            hook=hook,
            script=script,
            title=title,
            caption=caption,
            hashtags=hashtags,
        )
