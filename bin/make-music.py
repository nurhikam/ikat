#!/usr/bin/env python3
"""Synthesise the theme's default background piano piece.

    ./bin/make-music.py -o assets/music/forest-lace.mp3

The piece is composed and rendered here, in code, so the audio that ships with
a theme is provably original work — no licence to clear, nothing to strip when
a template is sold. Swap in a client's own licensed track per invitation with
`music.src` in their JSON; this only supplies the default.

Pure standard library plus ffmpeg for the final encode: no numpy, no scipy.
The synthesis is additive — a handful of inharmonic partials under a decaying
envelope — which is not a concert grand, but it is unmistakably a piano at the
volume background music actually plays at.
"""

from __future__ import annotations

import argparse
import array
import math
import os
import struct
import subprocess
import sys
import tempfile

SR = 44100
LUT_BITS = 12
LUT_SIZE = 1 << LUT_BITS
LUT_MASK = LUT_SIZE - 1
LUT = [math.sin(2.0 * math.pi * i / LUT_SIZE) for i in range(LUT_SIZE)]

BPM = 63.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT

# ---------------------------------------------------------------- composition

# Original progression in D major. Each bar: (bass midi, [chord tones]).
PROGRESSION = [
    (38, [50, 54, 57]),   # D      D3 F#3 A3
    (37, [49, 52, 57]),   # A/C#   C#3 E3 A3
    (35, [47, 50, 54]),   # Bm     B2 D3 F#3
    (31, [50, 55, 59]),   # G      D3 G3 B3
    (30, [50, 54, 57]),   # D/F#   D3 F#3 A3
    (31, [50, 55, 59]),   # G      D3 G3 B3
    (33, [49, 52, 57]),   # A      C#3 E3 A3
    (38, [50, 54, 57]),   # D      D3 F#3 A3
]

# (bar, beat, midi, beats, velocity)
MELODY_A = [
    (0, 0.0, 66, 2.0, 0.62), (0, 2.0, 69, 2.0, 0.58),
    (1, 0.0, 64, 2.0, 0.60), (1, 2.0, 61, 2.0, 0.55),
    (2, 0.0, 62, 3.0, 0.62), (2, 3.0, 66, 1.0, 0.52),
    (3, 0.0, 59, 4.0, 0.60),
    (4, 0.0, 57, 2.0, 0.55), (4, 2.0, 62, 2.0, 0.58),
    (5, 0.0, 59, 2.0, 0.56), (5, 2.0, 67, 2.0, 0.62),
    (6, 0.0, 66, 2.0, 0.60), (6, 2.0, 64, 2.0, 0.56),
    (7, 0.0, 62, 4.0, 0.58),
]

# Second pass: the same melody an octave up, thinned out and quieter, so the
# loop develops instead of simply repeating.
MELODY_B = [
    (0, 0.0, 78, 2.0, 0.46), (0, 2.5, 81, 1.5, 0.40),
    (1, 0.0, 76, 2.0, 0.44), (1, 2.0, 73, 2.0, 0.38),
    (2, 0.0, 74, 3.0, 0.46),
    (3, 0.0, 71, 3.0, 0.44), (3, 3.0, 74, 1.0, 0.36),
    (4, 0.0, 69, 2.0, 0.40), (4, 2.0, 74, 2.0, 0.44),
    (5, 0.0, 71, 2.0, 0.42), (5, 2.0, 79, 2.0, 0.48),
    (6, 0.0, 78, 2.0, 0.44), (6, 2.0, 76, 2.0, 0.40),
    (7, 0.0, 74, 4.0, 0.42),
]

# Left-hand arpeggio: eighth notes, index into [bass] + chord tones.
ARPEGGIO = [0, 1, 2, 3, 2, 1, 2, 3]


def midi_to_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69) / 12.0))


def render_note(midi: int, dur: float, partials: int = 8) -> array.array:
    """One piano note: inharmonic partials under a per-partial decay.

    Higher partials die faster than the fundamental, which is most of what
    separates a struck string from an organ."""
    f0 = midi_to_hz(midi)
    n = int((dur + 2.2) * SR)          # tail past the nominal duration
    buf = array.array("d", bytes(8 * n))

    # Lower notes ring longer; B is the string inharmonicity coefficient.
    base_decay = 2.6 + max(0.0, (60 - midi)) * 0.055
    B = 0.0004

    lut = LUT
    for h in range(1, partials + 1):
        fh = f0 * h * math.sqrt(1.0 + B * h * h)
        if fh > SR * 0.45:
            break
        amp = 1.0 / (h ** 1.35)
        decay = base_decay / (1.0 + 0.55 * (h - 1))
        step = fh / SR * LUT_SIZE
        phase = 0.0
        k = -1.0 / (decay * SR)
        env = 1.0
        env_mul = math.exp(k)
        for i in range(n):
            buf[i] += lut[int(phase) & LUT_MASK] * amp * env
            phase += step
            env *= env_mul

    # Hammer attack: a short filtered noise burst, plus a 4 ms fade-in so the
    # onset does not click.
    atk = int(0.004 * SR)
    for i in range(atk):
        buf[i] *= i / atk

    # Release: fade the tail so overlapping notes do not accumulate mud.
    rel_start = int((dur + 1.4) * SR)
    if rel_start < n:
        span = n - rel_start
        for i in range(rel_start, n):
            buf[i] *= 1.0 - (i - rel_start) / span

    return buf


def build_events():
    """Returns [(start_seconds, midi, duration_seconds, velocity)]."""
    ev = []
    for pass_i, melody in enumerate((MELODY_A, MELODY_B)):
        t0 = pass_i * 8 * BAR
        for bar, (bass, chord) in enumerate(PROGRESSION):
            tones = [bass] + chord
            for step, idx in enumerate(ARPEGGIO):
                start = t0 + bar * BAR + step * (BEAT / 2)
                vel = 0.34 if step == 0 else 0.2
                ev.append((start, tones[idx], BEAT * 0.9, vel))
        for bar, beat, midi, beats, vel in melody:
            ev.append((t0 + bar * BAR + beat * BEAT, midi, beats * BEAT, vel))
    return ev


def mix(events):
    total = int(max(s + d for s, _, d, _ in events) + 3.0) * SR
    left = array.array("d", bytes(8 * total))
    right = array.array("d", bytes(8 * total))

    cache = {}
    for start, midi, dur, vel in events:
        key = (midi, round(dur, 3))
        if key not in cache:
            cache[key] = render_note(midi, dur)
        note = cache[key]

        off = int(start * SR)
        # Notes sit across the stereo field by pitch, the way a keyboard does.
        pan = min(1.0, max(0.0, (midi - 36) / 48.0))
        gl = vel * math.cos(pan * math.pi / 2) * 1.06
        gr = vel * math.sin(pan * math.pi / 2) * 1.06
        for i, s in enumerate(note):
            j = off + i
            if j >= total:
                break
            left[j] += s * gl
            right[j] += s * gr
    return left, right, total


def reverb(ch, total, taps, feedback=0.28):
    """Cheap plate stand-in: a few feedback delays. Enough to stop the piece
    sounding like it was recorded inside a phone."""
    out = array.array("d", ch)
    for delay_ms, gain in taps:
        d = int(delay_ms / 1000.0 * SR)
        for i in range(d, total):
            out[i] += out[i - d] * gain * feedback
    return out


def normalise(left, right, total, peak=0.72):
    m = 0.0
    for buf in (left, right):
        for s in buf:
            a = abs(s)
            if a > m:
                m = a
    if m == 0:
        return
    g = peak / m
    for buf in (left, right):
        for i in range(total):
            buf[i] *= g


def write_wav(path, left, right, total):
    frames = bytearray()
    pack = struct.Struct("<hh").pack
    for i in range(total):
        l = max(-1.0, min(1.0, left[i]))
        r = max(-1.0, min(1.0, right[i]))
        frames += pack(int(l * 32767), int(r * 32767))

    data = bytes(frames)
    with open(path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE")
        f.write(b"fmt " + struct.pack("<IHHIIHH", 16, 1, 2, SR, SR * 4, 4, 16))
        f.write(b"data" + struct.pack("<I", len(data)) + data)


def main() -> int:
    p = argparse.ArgumentParser(description="Render the default theme piano loop.")
    p.add_argument("-o", "--out", default="assets/music/forest-lace.mp3")
    p.add_argument("--bitrate", default="96k")
    p.add_argument("--wav", action="store_true", help="keep the intermediate WAV")
    args = p.parse_args()

    print("composing…", file=sys.stderr)
    events = build_events()

    print(f"rendering {len(events)} notes…", file=sys.stderr)
    left, right, total = mix(events)

    print("space…", file=sys.stderr)
    taps = [(63.0, 0.55), (97.0, 0.42), (131.0, 0.31)]
    left = reverb(left, total, taps)
    right = reverb(right, total, [(d * 1.07, g) for d, g in taps])

    normalise(left, right, total)

    tmp = tempfile.mktemp(suffix=".wav")
    write_wav(tmp, left, right, total)
    print(f"  {total / SR:.1f}s rendered", file=sys.stderr)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", tmp,
         "-codec:a", "libmp3lame", "-b:a", args.bitrate, "-ac", "2", args.out],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr)

    if args.wav:
        wav_out = os.path.splitext(args.out)[0] + ".wav"
        os.replace(tmp, wav_out)
        print(f"  {wav_out}", file=sys.stderr)
    else:
        os.remove(tmp)

    kb = os.path.getsize(args.out) / 1024
    print(f"{args.out}  ({kb:.0f} KB, {total / SR:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
