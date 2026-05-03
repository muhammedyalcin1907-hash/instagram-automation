# Instagram Reels Automation (FastAPI + OpenAI + FFmpeg)

Bu repo, Python ile Instagram Reels üretim hattının çalışabilir temel sürümünü sağlar.

## Özellikler
- FastAPI backend
- Türkçe içerik üretimi (hook/senaryo/başlık/açıklama/hashtag)
- OpenAI TTS ile kadın/erkek seslendirme
- FFmpeg ile 9:16 video + ses + altyazı bindirme
- Media gönderilmezse otomatik gradient/renkli arka plan video üretimi
- Instagram Graph API publish modülü
- Dry-run test sistemi (token yoksa güvenli mock)
- SQLite paylaşım geçmişi

## Kurulum
1. Python 3.11+ kur.
2. FFmpeg kur ve `ffmpeg -version` ile doğrula.
3. Sanal ortam:
## Proje Yapısı
```text
app/
  main.py
  config.py
  content_generator.py
  tts.py
  video_builder.py
  instagram_client.py
  database.py
  scheduler.py
uploads/
generated/
requirements.txt
.env.example
README.md
```

## 1) Kurulum (adım adım)
1. Python 3.11+ kurulu olduğundan emin olun.
2. FFmpeg kurun ve terminalden `ffmpeg -version` çalıştığını doğrulayın.
3. Sanal ortam oluşturun:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
4. Paketleri yükle:
   ```bash
   pip install -r requirements.txt
   ```
5. Ortam dosyası:
   ```bash
   cp .env.example .env
   ```

## Çalıştırma
4. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
5. Ortam değişkenlerini hazırlayın:
   ```bash
   cp .env.example .env
   ```
6. `.env` dosyasını düzenleyin (`OPENAI_API_KEY`, Instagram alanları, `DRY_RUN`).

## 2) Uygulamayı çalıştırma
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger:
- `http://localhost:8000/docs`

## Endpointler
## 3) Endpointler
- `GET /health`
- `GET /dry-run/test`
- `POST /reels/generate`
- `GET /reels/history`
- `GET /reels/history/{id}`

## /reels/generate örnek JSON (istenen format)
```json
{
  "niche": "motivasyon",
  "voice_gender": "female",
  "publish": false
}
```

> `media_filename` opsiyoneldir. Gönderilmezse sistem otomatik 9:16 gradient/renkli background video üretir.

## Demo komutlar
```bash
curl http://localhost:8000/health
curl http://localhost:8000/dry-run/test
```

## 4) Demo komutlar
### Sağlık kontrolü
```bash
curl http://localhost:8000/health
```

### Dry-run test
```bash
curl http://localhost:8000/dry-run/test
```

### Reels üretimi (dosya ile)
### Reels üretimi
Önce `uploads/` içine `sample.mp4` koyun.

```bash
curl -X POST http://localhost:8000/reels/generate \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "motivasyon",
    "voice_gender": "female",
    "niche": "kişisel gelişim",
    "voice_gender": "female",
    "media_filename": "sample.mp4",
    "publish": false
  }'
```

## Fallback davranışı
- `OPENAI_API_KEY` yoksa fallback metin üretilir.
- TTS servisinde hata olursa sessiz MP3 oluşturulur.
- Böylece sistem yine `generated/` klasörüne final MP4 üretir.

## Çıktılar
- Girdi medya: `uploads/`
- Üretilen dosyalar: `generated/`
- Veritabanı: `reels.db`
- Log: `app.log`

## Railway Deploy
`Procfile`:
```txt
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
```

### Reels üretimi (dosyasız otomatik background)
`media_filename` göndermezseniz sistem otomatik motion/renkli 9:16 arka plan üretir:

```bash
curl -X POST http://localhost:8000/reels/generate \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "teknoloji",
    "voice_gender": "male",
    "publish": false
  }'
```

### Geçmiş listesi
```bash
curl http://localhost:8000/reels/history
```

## 5) Dry-run ve gerçek paylaşım
- `DRY_RUN=true`: Gerçek publish yapmaz, mock sonuç döner.
- `DRY_RUN=false`: Geçerli `INSTAGRAM_ACCESS_TOKEN` ve `INSTAGRAM_BUSINESS_ACCOUNT_ID` ile Graph API publish akışı dener.

> Not: Graph API publish için video dosyasının herkese açık bir URL'de erişilebilir olması gerekir.

## 6) Çıktılar
- Girdi medya: `uploads/`
- Üretilen dosyalar: `generated/`
- Veritabanı: `reels.db`
- Log dosyası: `app.log`

## Railway Deploy
- `Procfile` eklendi ve Railway için web process tanımlandı:
  `web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT}`
- Railway ortamında `PORT` değişkeni platform tarafından verilir.
