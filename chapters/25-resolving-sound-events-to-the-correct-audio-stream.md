# 25. Resolving sound events to the correct audio stream

[← Chapter index](../README.md#chapters)

Resolve audio from the native event that actually plays it. A spell, weapon or animation name does not uniquely identify a sound resource.

## Trace the caller before decoding a bank

Begin with a stock sound event: ordinary weapon contact, a critical impact, an interface action or a native spell. Trace from the animation/action event to the audio request, recording the event discriminator, bank/resource identity and selected cue.

For the reference executable, weapon-hit investigation can start near `0x31ADB0`; one path uses sound class 2 and an output field at `+0x34`. Event dispatch around `0x46C250` distinguishes event and cue kinds. Follow the actual branch taken by the stock action instead of assuming every event in a weapon bank means contact.

The complete audio-request ABI and bank codec are not specified here. Do not cast those addresses to a guessed “play WAV” signature or apply another game's bank decoder solely because the file extension looks familiar.

## Keep identities separate

Maintain a mapping with these columns:

| Identity | Meaning |
| --- | --- |
| Action/animation event | Why playback was requested |
| Event discriminator and cue | Which native branch selected it |
| Bank/resource key | Which resource the engine loads |
| Encoded stream | The actual audio payload within that resource |
| Decoded format | Channels, rate, sample format and duration |

An event index and an extraction tool's stream/subsong index can differ. Resolve the mapping from the native tables or parser rather than adding a guessed constant offset.

## Preserve playback behavior

Keep impact, swing, critical and finishing cues distinct until their triggers are established. Decode an unchanged resource before trimming or replacing it. Preserve loop points and channel layout where the native event expects them.

For replacement audio, retain the native cue's scheduling, category and spatial parameters. For independently added PCM playback, implement a real audio backend and its lifetime explicitly; [Chapter 26](26-making-added-sounds-follow-the-games-sfx-volume.md) covers category gain. No mixer or predecoded asset collection is assumed.

---

[← Previous chapter](24-weapon-animation-and-hit-timing.md) · [Chapter index](../README.md#chapters) · [Next chapter →](26-making-added-sounds-follow-the-games-sfx-volume.md)
