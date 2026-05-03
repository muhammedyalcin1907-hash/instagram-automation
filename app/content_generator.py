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
        niche = niche or "motivasyon"

        hooks = [
            "Bugün kendine bir iyilik yap: vazgeçme.",
            "Hayatını değiştirecek şey motivasyon değil, disiplin.",
            "Kimse görmüyorken yaptıkların seni büyütür.",
            "Başlamak için mükemmel günü bekleme.",
        ]

        scripts = [
            [
                "Bugün küçük bir adım at.",
                "Telefonu bırak ve hedefini hatırla.",
                "Kimse senin yerine başlamayacak.",
                "Zor gelen şey seni güçlendirecek.",
                "Devam edersen değişim kaçınılmaz.",
            ],
            [
                "Her gün aynı yerde kalmak zorunda değilsin.",
                "Bir karar ver ve arkasında dur.",
                "Motivasyon geçer ama disiplin kalır.",
                "Küçük alışkanlıklar büyük sonuçlar doğurur.",
                "Bugün başladığın şey yarın seni kurtarabilir.",
            ],
            [
                "Kendine verdiğin sözleri tut.",
                "Başarı bir anda gelmez.",
                "Sessizce çalış, sonuçlar konuşsun.",
                "Ertelediğin hayat seni beklemiyor.",
                "Şimdi başla, çünkü en doğru zaman bu.",
            ],
        ]

        hook = random.choice(hooks)
        lines = random.choice(scripts)

        script = " ".join(lines)
        title = f"{niche.title()} Reels"
        caption = f"{hook}\n\n{script}"
        hashtags = "#motivasyon #basari #gelisim #disiplin #reels #aireelsotoman"

        return ReelContent(
            hook=hook,
            script=script,
            title=title,
            caption=caption,
            hashtags=hashtags,
        )
