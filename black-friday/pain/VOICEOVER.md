# X7 Black Friday – سكريبت الفويس أوفر (مصري)

**Length:** 28 seconds. Start speaking at 0.3 s. Each line has to fit its time window, because the on-screen captions follow these timings.
**Who reads it:** an Egyptian speaker, man or woman. A coach from the gym is ideal: a real voice people know is more convincing than any AI voice.
**Tone:** start low and close, like talking to a friend (*not* an announcer voice). At line 4 the voice picks up and fills with energy, and the last line is a push.
**Recording:** on a phone is fine, in a quiet room, phone 20–30 cm from the mouth, voice-memo app. Leave 1 second of silence before you start.

| # | Time | Line (exactly as written) | How to say it |
|---|---|---|---|
| 1 | 0.3 – 4.6 | كل سبت تقول: خلاص، من النهارده هبدأ… ويعدّي السبت، واللي بعده، واللي بعده. | Calm, a little sarcastic, like you know them. Slow down a touch on "واللي بعده" the second time. |
| 2 | 4.8 – 8.2 | تطلع السلم تنهج… والهدوم اللي بتحبها بقت ضيقة عليك. | A short breath after "تنهج". Personal, not mocking. |
| 3 | 8.4 – 11.2 | واشتركت في جيم قبل كده… روحت أسبوع، وبطّلت. | A light pause before "وبطّلت", then say it plainly. |
| 4 | 11.4 – 14.4 | المشكلة مش فيك. المشكلة إنك كنت لوحدك. | **The turn.** Slow and sure. Stress "مش فيك" and "لوحدك". |
| 5 | 14.6 – 17.8 | في إكس سڤن، مش هتبقى لوحدك… هنمشي معاك خطوة بخطوة. | Warm, with a smile in your voice. The music opens up here. |
| 6 | 18.0 – 20.4 | وفي البلاك فرايداي… خصم تلاتين في المية. | Excited. Hit "تلاتين" hard. |
| 7 | 20.6 – 26.8 | متستناش السبت الجاي. ابعتلنا رسالة دلوقتي… ابدأ رحلتك، وغيّر حياتك مع إكس سڤن. | Strong, then calmer on "ابدأ رحلتك", ending on a confident high. |

### Notes
- The script is written in everyday Egyptian Arabic, not formal Arabic, and not a translation of English copy: "هبدأ", "بطّلت", "متستناش", "دلوقتي".
- "X7" is read as **إكس سڤن**. If the gym says the name differently (for example "إكس سڤن بلس"), say it the way you always do.
- Line 5 ("هنمشي معاك خطوة بخطوة") promises that the gym will follow people's progress. Only keep it if that's true for X7; otherwise change it.

### Adding the voice to the video
```
cd black-friday/pain
./add_voice.sh voice.m4a        # or pass a start time: ./add_voice.sh voice.m4a 0.5
```
It produces `black-friday/final/X7-Black-Friday-Pain-Promo.mp4`. It lowers the music while you speak and keeps the volume at a standard level for social media.
