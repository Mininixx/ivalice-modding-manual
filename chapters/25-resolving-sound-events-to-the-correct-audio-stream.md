# 25. Resolving sound events to the correct audio stream

[← Chapter index](../README.md#chapters)

Follow the event mapping; matching a spell name or bank alone is insufficient.

## The extraction chain
Follow this chain: effect OEF audio slot → `SeSep   ` record DWORD at `+8` → sound-ID/event mapping in the binary `*_common.txt` table → FEV event name → matching FSB5 stream name → decoded WAV.

Do not equate an event index with a decoder's subsong index. For NulFrost, event 1123 maps to subsong 1242. Resolve the mapping explicitly; do not extrapolate a constant offset from another bank.

Preserve distinct cues until their triggers are known. Keep Demi main cue 9021 separate from additional cue 14069; do not combine them without resolving their event timing.

Decode the matched ADPCM stream to the required PCM format; the current mixer assets use 16-bit stereo PCM at 48 kHz. Keep extraction separate from trimming, mixing and normalization. Deduplicate identical streams while retaining each event mapping, including shared Break cue 9061.

## A correct weapon bank can still produce the wrong cue
For Ninja Sword bank `se286`, follow the normal-hit path through `0x31ADB0`, with sound class 2 and its output at `+0x34`; event 2 in `0x46C250` selects kind-0 cues 3–5. Event 3/kind 0/cue 10 is a different sound.

Use the event actually reached by the accepted native hit. A swing, contact, critical hit and finishing flourish may share a bank while using different entries. Resolve the actual asset behind an internal symbol: `NinjaHit` can reference a replacement WAV rather than the native bank.

---

[← Previous chapter](24-building-blade-aligned-projectiles-with-one-impact.md) · [Chapter index](../README.md#chapters) · [Next chapter →](26-making-added-sounds-follow-the-games-sfx-volume.md)
