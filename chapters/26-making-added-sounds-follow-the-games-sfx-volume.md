# 26. Making added sounds follow the game’s SFX volume

[← Chapter index](../README.md#chapters)

Added playback must follow the correct native volume category. Running audio in the game process does not automatically connect it to the game's sound system.

## Native setting boundary

For the [reference executable](30-native-addresses-and-hook-ownership.md), inspect volume routine `0x2DE290` and the settings pointer at `0x215E6E0`. In the associated settings layout, the SFX value is a WORD at `+0x0A`; music at `+8` and voice at `+0x0C` are separate values. The native volume path caps the setting at 100.

Resolve the pointer using the live module base and confirm the containing object before reading. Do not dereference the preferred VA as an absolute address in an unrelated process.

For an added backend whose gain is defined linearly, the basic conversion is:

```python
def sfx_gain(native_setting):
    return max(0, min(100, int(native_setting))) / 100.0
```

This function only converts an already-read value. It is not a native memory reader or audio player.

## Choose a playback route explicitly

Reusing a native cue preserves the native route's category and other supported behavior when its request is constructed correctly. Adding a separate mixer requires initialization, sound loading, voice ownership and cleanup implemented in the extension. It does not inherit native spatialization, reverb or event timing automatically.

Apply updated gain to currently playing added voices as well as new ones. Do not restart audio merely to change volume. Treat unavailable settings and scene retirement according to an explicit playback policy instead of retaining a dangling settings pointer.

## Asset gain and user gain are different

Use a fixed asset-level adjustment to align a replacement with representative native cues, then apply the user's live setting. Retain headroom for overlapping sounds. A file that does not clip individually can still overload a sum.

For linear amplitude gain, a reduction to 80 percent means multiplication by 0.8, approximately −1.94 dB. Do not confuse percentage amplitude, power and decibels. Trigger a contact cue from the same accepted native event as the associated impact, and ensure a persistent flag cannot replay it every frame.

---

[← Previous chapter](25-resolving-sound-events-to-the-correct-audio-stream.md) · [Chapter index](../README.md#chapters) · [Next chapter →](27-creating-convincing-weapon-surfaces-without-changing-geometry.md)
