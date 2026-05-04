from __future__ import annotations

import random
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
        niche = (niche or "motivasyon").strip()

        hooks = [
            "Bugün pes etmezsen, yarın kendine teşekkür edeceksin.",
            "Disiplin, motivasyonun bittiği yerde başlar.",
            "Kimse görmüyorken yaptıkların kaderini değiştirir.",
            "Hayatını değiştirmek için büyük bir gün değil, küçük bir karar gerekir.",
            "Başlamak için hazır olmayı bekleme. Hazır olmak, başlayınca gelir.",
        ]

        scripts = [
            [
                "Bugün sadece bir adım at.",
                "Küçük görünse bile devam et.",
                "Çünkü seni değiştiren şey hız değil, sürekliliktir.",
                "Kimse görmese bile çalış.",
                "Bir gün sonuçlar senin adına konuşacak.",
            ],
            [
                "Kendine verdiğin sözü bugün tut.",
                "Ertelediğin her şey zihninde ağırlık olur.",
                "Başlamak korkutabilir ama beklemek daha pahalıdır.",
                "Bugün yapacağın küçük hamle yarın seni farklı biri yapar.",
                "Şimdi başla.",
            ],
            [
                "Motivasyon bekleme.",
                "Disiplin kur.",
                "Her gün aynı saatte küçük bir işi bitir.",
                "Bunu yeterince uzun yaparsan özgüvenin geri gelir.",
                "Çünkü güven, kendine verdiğin sözleri tutunca büyür.",
            ],
        ]

        hook = random.choice(hooks)
        lines = random.choice(scripts)

        script = ". ".join(lines) + "."
        title = f"{niche.title()} İçin Güçlü Reels"
        caption = f"{hook}\n\n{script}\n\nKaydet ve bugün uygula."
        hashtags = "#motivasyon #disiplin #basari #kisiselgelisim #reels #aireelsotoman"

        return ReelContent(
            hook=hook,
            script=script,
            title=title,
            caption=caption,
            hashtags=hashtags,
        )
