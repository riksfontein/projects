"""Omni chain clips -> picture.mp4 on the real narration timeline (Riks, 2026-09-25).

    py -3.12 _rx_omni_assemble.py --channel ch02 --episode ep16 --clips "%USERPROFILE%\\Downloads\\ch02ep16-omni"
        --cuts-then "<ep16>\\_v5\\sample_1-29_vol_level\\cuts.json"
        [--cuts <full-episode cuts.json>] [--narration <narration_full.wav>] [--out <dir>]

--cuts-then MUST be the cuts.json that _rx_omni_timing.py used when the prompts were written (for ep16 and
ep19: the sample_1-29 cuts), or "estimate" if there was none (ep17). Guessing it would shift every beat.

The chain prompts were written on a 10 s grid of the narration as it was known then (real voice where a
cuts.json existed, shotlist estimate after that). Once the full narration is built, its cuts.json gives the
real start of every shot. This script maps each clip's 10 s window onto that real timeline and stretches the
clip to fit (setpts), so every beat lands on its line. Clips are joined in order into ONE continuous
picture.mp4 (no audio) whose length equals the narration; the builder's audio stage then mixes narration +
music (2c/2d picks, two-pass loudnorm) over it as usual. --narration adds a quick preview_with_vo.mp4 for a
timing check only (not the master).

Stretch outside 0.8-1.25x is reported (the picture would look slowed/sped); the report is written to
omni_timeline.json next to picture.mp4.
"""
import argparse, json, pathlib, re, shutil, subprocess, sys

from _rx_omni_timing import CLIP_S, find_cuts, timing

FPS = 30


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found (install it, or: pip install imageio-ffmpeg)")


def duration(ff, path):
    """Container duration via ffmpeg's own banner (works without ffprobe)."""
    out = subprocess.run([ff, "-hide_banner", "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    if not m:
        sys.exit(f"cannot read duration of {path}")
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


def time_map(raw, cuts_then, cuts_now):
    """Piecewise-linear map from the timeline the prompts were written on to the final real timeline."""
    then, now = timing(raw, cuts_then), timing(raw, cuts_now)
    xs = [t[0] for t in then] + [then[-1][2]]
    ys = [t[0] for t in now] + [now[-1][2]]

    def f(x):
        if x <= xs[0]:
            return ys[0] + (x - xs[0])
        for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
            if x <= x1:
                return y0 + (x - x0) * (y1 - y0) / max(1e-6, x1 - x0)
        return ys[-1] + (x - xs[-1])
    return f, xs[-1], ys[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel")
    ap.add_argument("--episode")
    ap.add_argument("--clips", required=True, help="folder with clip_001.mp4 ... (TurboFlow save folder)")
    ap.add_argument("--prefix", default="clip")
    ap.add_argument("--manifest", help="shotlist json (default: the episode's newest)")
    ap.add_argument("--cuts-then",
                    help="the cuts.json the prompts were timed on (ch02 ep16: _v5\\\\sample_1-29_vol_level\\\\cuts.json), or 'estimate'")
    ap.add_argument("--cuts", help="FULL-episode real-voice cuts.json (default: the episode's _v5/*/cuts.json covering most shots)")
    ap.add_argument("--narration", help="narration_full.wav for a quick preview_with_vo.mp4")
    ap.add_argument("--out", help="output folder (default: <episode>/_v5/omni_full)")
    ap.add_argument("--clips-upto", type=int, help="2-min sample: only clips 1..N (needs cuts covering them only)")
    ap.add_argument("--audio", help="finished mix (mp4/wav) to lay under the picture: narration + bed + ducking as "
                                    "picked at gates 2C/2D; trimmed to the picture with a 1.5 s fade-out")
    ap.add_argument("--plain", action="store_true", help="no shotlist (ch03 tests): clips at 10 s each, as generated")
    a = ap.parse_args()
    if a.plain:
        return plain(a)
    if not (a.channel and a.episode and a.cuts_then):
        sys.exit("--channel, --episode and --cuts-then are required (or use --plain for ch03 tests)")
    tag = f"{a.channel}{a.episode}".upper()
    ep_dir = None
    if a.manifest:
        raw = json.loads(pathlib.Path(a.manifest).read_text(encoding="utf-8"))
    else:
        from _rx_flow_prompts import manifest
        ep_dir, raw = manifest(a.channel, a.episode)
    raw = sorted(raw, key=lambda s: s["n"])
    cuts_now = json.loads(pathlib.Path(a.cuts).read_text(encoding="utf-8")) if a.cuts else (find_cuts(ep_dir) or (None, None))[1]
    if not cuts_now or (len(cuts_now) < len(raw) and not a.clips_upto):
        sys.exit(f"{tag}: need the FULL-episode cuts.json ({len(raw)} shots) - build the full narration first")
    cuts_then = None if a.cuts_then == "estimate" else json.loads(pathlib.Path(a.cuts_then).read_text(encoding="utf-8"))
    f, end_then, end_now = time_map(raw, cuts_then, cuts_now)

    ff = ffmpeg()
    src = pathlib.Path(a.clips)
    clips = sorted(src.glob(f"{a.prefix}_[0-9][0-9][0-9].mp4"))
    n_need = int(-(-end_then // CLIP_S))
    if a.clips_upto:
        n_need = min(n_need, a.clips_upto)
        covered = timing(raw, cuts_now)[len(cuts_now) - 1][2]
        if n_need * CLIP_S > timing(raw, cuts_then)[len(cuts_now) - 1][2] or f(n_need * CLIP_S) > covered + 0.5:
            sys.exit(f"{tag}: clips 1-{n_need} run past the real voice in cuts.json ({covered:.0f} s)")
    have = {int(p.stem.split("_")[-1]) for p in clips}
    missing = [k for k in range(1, n_need + 1) if k not in have]
    if missing:
        sys.exit(f"{tag}: missing clips {missing[:10]}{'...' if len(missing) > 10 else ''} in {src}")
    sub = f"omni_sample_1-{n_need}" if a.clips_upto else "omni_full"
    out = pathlib.Path(a.out) if a.out else (ep_dir / "_v5" / sub if ep_dir else pathlib.Path(sub))
    seg_dir = out / "seg"
    seg_dir.mkdir(parents=True, exist_ok=True)

    report, segs = [], []
    for k in range(1, n_need + 1):
        clip = src / f"{a.prefix}_{k:03d}.mp4"
        w0, w1 = (k - 1) * CLIP_S, min(k * CLIP_S, end_then)
        r0, r1 = (0.0 if k == 1 else f(w0)), f(w1)   # the picture starts with the narration file at 0 s
        real = duration(ff, clip)
        used = real * (w1 - w0) / CLIP_S          # the last clip covers only part of its 10 s
        factor = (r1 - r0) / used
        seg = seg_dir / f"seg_{k:03d}.mp4"
        subprocess.run([ff, "-y", "-v", "error", "-t", f"{used:.3f}", "-i", str(clip), "-an",  # -t on the INPUT
                        "-vf", f"setpts=PTS*{factor:.5f},fps={FPS},scale=1920:1080:flags=lanczos,setsar=1",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(seg)],
                       check=True)
        flag = "" if 0.8 <= factor <= 1.25 else "STRETCH"
        report.append({"clip": k, "prompt_window": [round(w0, 2), round(w1, 2)], "real_window": [round(r0, 2), round(r1, 2)],
                       "source_s": round(used, 2), "factor": round(factor, 3), "flag": flag})
        segs.append(seg)
        if flag:
            print(f"  clip {k}: stretch {factor:.2f}x (prompt {w0:.0f}-{w1:.0f}s -> real {r0:.1f}-{r1:.1f}s)")
    lst = seg_dir / "concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    picture = out / "picture.mp4"
    subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)], check=True)
    (out / "omni_timeline.json").write_text(json.dumps({"tag": tag, "narration_s": round(end_now, 2),
                                                        "picture_s": round(duration(ff, picture), 2), "clips": report}, indent=1), encoding="utf-8")
    print(f"{tag}: {len(segs)} clips -> {picture} ({duration(ff, picture):.1f} s, narration {end_now:.1f} s); "
          f"{sum(1 for r in report if r['flag'])} clips outside 0.8-1.25x")
    if a.audio:
        mux(ff, picture, a.audio, out / f"{tag}_{sub}.mp4")
    if a.narration:
        prev = out / "preview_with_vo.mp4"
        subprocess.run([ff, "-y", "-v", "error", "-i", str(picture), "-i", a.narration, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(prev)], check=True)
        print(f"preview (timing check only, not the master): {prev}")


def mux(ff, picture, audio, dst):
    """Picture + an existing finished mix. The mix already carries narration, bed and ducking/level
    (gates 2C/2D), so it is taken as is - only trimmed to the picture with a short fade-out."""
    d = duration(ff, picture)
    subprocess.run([ff, "-y", "-v", "error", "-i", str(picture), "-i", str(audio), "-map", "0:v", "-map", "1:a:0",
                    "-af", f"atrim=0:{d:.3f},afade=t=out:st={max(0, d - 1.5):.3f}:d=1.5",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", str(dst)], check=True)
    print(f"sample with audio: {dst}")


def plain(a):
    """ch03 archetype tests: no shotlist; the clips were written on an even 10 s grid of the narration."""
    ff = ffmpeg()
    src = pathlib.Path(a.clips)
    n = a.clips_upto or len(list(src.glob(f"{a.prefix}_[0-9][0-9][0-9].mp4")))
    out = pathlib.Path(a.out or f"{a.prefix}_sample")
    (out / "seg").mkdir(parents=True, exist_ok=True)
    segs = []
    for k in range(1, n + 1):
        clip = src / f"{a.prefix}_{k:03d}.mp4"
        if not clip.exists():
            sys.exit(f"missing {clip}")
        seg = out / "seg" / f"seg_{k:03d}.mp4"
        subprocess.run([ff, "-y", "-v", "error", "-t", f"{CLIP_S:.3f}", "-i", str(clip), "-an",
                        "-vf", f"fps={FPS},scale=1920:1080:flags=lanczos,setsar=1",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(seg)], check=True)
        segs.append(seg)
    lst = out / "seg" / "concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    picture = out / "picture.mp4"
    subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)], check=True)
    print(f"{a.prefix}: {n} clips -> {picture} ({duration(ff, picture):.1f} s)")
    if a.audio:
        mux(ff, picture, a.audio, out / f"{a.prefix}_sample_2min.mp4")


if __name__ == "__main__":
    main()
