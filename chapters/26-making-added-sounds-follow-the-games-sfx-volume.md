# 26. Making added sounds follow the game’s SFX volume

[← Chapter index](../README.md#chapters)

Put playback in the game process, follow the right category and compare perceived level.

## Read the same category as native sound effects
The native volume routine at `0x2DE290` caps the setting at 100. The settings object is reached through `0x215E6E0`: SFX is the word at `+0x0A`, category 2, scaled by `/100`. Music at `+8` and voice at `+0x0C` are different categories.

Resolve addresses with ASLR and verify the build. The implemented reader falls silent while the configuration is unavailable. A roughly 15 ms update changes the master gain of currently playing added voices as well as new voices, without restarting their PCM.

An XAudio2 mixer inside the game process supports game-process audio capture. It is still a custom mixer: it does not automatically inherit native SEAD bank routing, spatialization or reverb. Likewise, a world/HUD renderer executing inside the game addresses a different capture boundary from an external transparent desktop window. Validate actual capture mode instead of treating all overlays as equivalent.

## Normalize an asset, then apply the live slider
Compare integrated loudness, the loudest short window and true peak. For short impacts, full-clip RMS can hide a sharp transient followed by silence; include a short-window measurement and oversampled true peak. Apply asset gain without changing pitch, duration, EQ or dynamics unless that change is intended.

Choose gain against representative native effects and allow headroom for overlapping casts. Do not reuse a prior clip's loudness target as a universal standard; individually unclipped files can still overload the combined mix.

```text
source PCM → measured asset gain → per-event/user trim → live SFX slider
                                                        → in-process mixer
```

A linear 20% volume reduction is a gain of 0.8, approximately −1.94 dB; it is not a 20 dB reduction. Trigger contact audio once from the same accepted collision as damage. Cancel or retire owned voices on scene change and avoid replaying every frame while a hit flag remains set.

---

[← Previous chapter](25-resolving-sound-events-to-the-correct-audio-stream.md) · [Chapter index](../README.md#chapters) · [Next chapter →](27-creating-convincing-weapon-surfaces-without-changing-geometry.md)
