# X7 Black Friday – سكريبت الفويس أوفر (النسخة القصيرة)

The voice is **Shaker** from [VoiceTut-TTS](https://github.com/MohammedAly22/VoiceTuT-TTS), a model fine-tuned on Egyptian Arabic (Apache 2.0), run locally. Each line was generated 1–3 times and the clearest take kept; pauses longer than 0.25 s are shortened to 0.15 s so there's no lag. Video length: 22.5 s.

| # | Starts at | Line |
|---|---|---|
| 1 | 0.1s | كل سبت تقول: هبدأ، ومبتبدأش. |
| 2 | 2.7s | تطلع السلم تنهج، وهدومك بقت ضيقة. |
| 3 | 5.4s | اشتركت في جيم، وبطّلت بعد أسبوع. |
| 4 | 8.0s | المشكلة مش فيك، المشكلة إنك كنت لوحدك. |
| 5 | 11.1s | مع إكس سفن، مش هتبقى لوحدك. |
| 6 | 13.3s | البلاك فرايداي، خصم تلاتين في المية! |
| 7 | 16.2s | متستناش السبت الجاي، ابعتلنا دلوقتي، وغيّر حياتك مع إكس سفن. |

### Regenerate
```
python3 gen_vt.py Shaker 32          # all lines (another voice: Ramy, Mahmoud, Ali ...)
python3 regen_best.py 4,5 2           # 2 extra takes of lines 4 and 5, keep the clearest
then: post-process, python3 build_vo.py, render, ./add_voice.sh vo/voice.wav 0
```
