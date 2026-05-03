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
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger:
- `http://localhost:8000/docs`

## Endpointler
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

```bash
curl -X POST http://localhost:8000/reels/generate \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "motivasyon",
    "voice_gender": "female",
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
