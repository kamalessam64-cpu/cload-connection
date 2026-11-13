#!/usr/bin/env bash
# usage: ./add_voice.sh voice.m4a [start_seconds=0.3]
# Lays an Egyptian voice-over recording over the pain promo, ducks the music under the voice, and normalises to -16 LUFS.
set -euo pipefail
VOICE="$1"; START="${2:-0.3}"; MS=$(python3 -c "print(int(float('$START')*1000))")
IN="../final/X7-Black-Friday-Pain-Promo-NoVoice.mp4"; OUT="../final/X7-Black-Friday-Pain-Promo.mp4"
ffmpeg -v error -y -i "$IN" -i "$VOICE" -filter_complex \
 "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=10:release=150,adelay=${MS}|${MS},volume=1.6,asplit[vo1][vo2];\
  [0:a]aformat=sample_rates=48000:channel_layouts=stereo[mus];[mus][vo1]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];\
  [duck][vo2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-5.5:LRA=11[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k "$OUT"
echo "done -> $OUT"
