# Kendo '84

A retro kendo game in the style of 1980s 8-bit console fighters. Two ippon win the bout.

**▶ Play in your browser: https://r4v3nst3rn.github.io/kendo84/**

Everything is in one HTML file: a 320×180 pixel-art canvas that fills the whole browser window (or the whole screen in fullscreen), chip sounds from the Web Audio API, and embedded fonts. It loads nothing from other servers and also works offline.

## Modes

- **1 Player**: climb the grades from 6th kyu to 8th dan against an increasingly skilled AI.
- **2 Players**: two players on one keyboard.
- **Training**: 14 short lessons with a partner, covering footwork, distance (maai), every cut and the guards.
- **Instructions**: opens a scrollable window over the game with the controls, techniques and rules. Close it with the ✕ in its corner or `Esc`.

## Controls

| Action | Player 1 (Shiro) | Player 2 (Aka) |
|---|---|---|
| Move | `W` `A` `S` `D` | `↑` `←` `↓` `→` |
| Strike | `F` | `K` |
| Do strike | `G` | `L` |
| Guard | hold away (`S` for low guard) | hold away (`↓` for low guard) |

- In single-player mode both key sets control Shiro, and `Space` also strikes.
- `Enter` starts the game. `P` or `Esc` pauses. `Q` in the pause menu returns to the menu. `M` mutes the sound.
- **Touch screens**: d-pad plus **MEN** (works as `F`) and **DO** (works as `G`) buttons. In portrait the picture is centred one third down the screen and the controls two thirds down; in landscape the controls sit over the picture's top corners. The game switches to fullscreen on the first tap where the browser allows it.

## Building from source

```sh
sh src/build.sh   # src/head.part + src/page.part -> index.html (+ test.html for tests)
```

`tests/` contains Playwright (Python) scripts for simulations and screenshots. Build first, then run e.g. `python3 tests/t1.py`.

## License

Copyright © 2026 R4V3NST3RN. All rights reserved.
The source is published so you can read it and play the game. No licence is granted to copy, modify or redistribute it.

The embedded fonts Silkscreen and VT323 are used under the SIL Open Font License 1.1. See [`fonts/OFL.txt`](fonts/OFL.txt).
