"""Gate 2A for the Omni chain: narration timing + the clip worksheet (Riks, 2026-09-25).

    py -3.12 _rx_omni_timing.py --channel ch01 --episode ep19 [--cuts <cuts.json>]

Method (screen share 2026-09-24): ONE master image = start frame of clip 1, every next 10 s Omni Flash
clip continues from the last frame of the previous one. The picture of every clip is AUTHORED (like the
ch03 samples) in _FLOW/<TAG>_omni_plan.json and rendered by _rx_omni_render.py. This script gives the
author the ground truth: which words fall in which 10 s clip, on the real voice where it exists.

Timing: real narration where a cuts.json covers it (the builder's per-shot cut points on the real voice;
default: the _v5/*/cuts.json that covers the most shots), the shotlist estimate after that, shifted so
the timeline stays continuous. The real voice ran ~4% longer than the estimate on ep19 shots 1-29, so
clips are only final where the voice is real.

Writes into _FLOW/:
  <TAG>_omni_words.json    every narration word with its time on the episode timeline + clip count
  <TAG>_omni_GATE2A.md     clip worksheet: time, narration, shots, the shotlist's chapter + palette
"""
import argparse, json, pathlib, re, sys

CLIP_S = 10.0
SAMPLE_CLIPS = 12  # 12 x 10 s = the 2-min sample (gate 2B)

PLATE_RE = re.compile(r"^a documentary frame showing:\s*(?P<narr>.*?)"
                      r"(?:\s*Scene context:\s*(?P<scene>.*?))?"
                      r"\s*(?P<style>Photorealistic .*?)\s*(?P<tail>ONE SINGLE FULL-FRAME.*)$", re.S)


def parse_plate(s):
    m = PLATE_RE.match(re.sub(r"\s+", " ", s["plate_prompt"]).strip())
    if not m:
        sys.exit(f"shot {s['n']}: plate_prompt not in the expected 'a documentary frame showing:' format")
    return m.group("narr").strip(), (m.group("scene") or "").strip().rstrip("."), m.group("style").strip()


def split_style(styles):
    """Channel base style = the sentences every shot shares; the rest of each shot is its palette."""
    sents = [re.split(r"(?<=\.)\s+", st) for st in styles]
    base = []
    for group in zip(*sents):
        if len(set(group)) != 1:
            break
        base.append(group[0])
    n = len(base)
    return " ".join(base), [" ".join(x[n:]) for x in sents]


def scene_key(scene):
    """Scene contexts start with a label ('the PETM cold open: ...'); same label = same location."""
    return scene.split(":", 1)[0].strip().lower() if ":" in scene else scene.lower()


def scene_desc(scene):
    """The picture without the shotlist's internal label (the label is for us, not for the model)."""
    return scene.split(":", 1)[1].strip() if ":" in scene else scene


def timing(raw, cuts):
    """(start, speech_end, span_end) per shot: real cut points where cuts.json covers the shot, the
    estimate after that, shifted so the timeline continues from the last real shot."""
    real = {c["n"]: c for c in cuts or []}
    out, shift = [], 0.0
    for i, s in enumerate(raw):
        c = real.get(s["n"])
        if c:
            nxt = real.get(s["n"] + 1)
            a, sp = float(c["line_start"]), float(c["cut_after"])
            b = float(nxt["line_start"]) if nxt else sp
            shift = b - float(s["est_end"])
        else:
            a, b = float(s["est_start"]) + shift, float(s["est_end"]) + shift
            sp = b
        out.append((a, max(sp, a + 0.1), max(b, a + 0.1)))
    return out


def load_shots(raw, cuts):
    base, palettes = split_style([parse_plate(s)[2] for s in raw])
    out = []
    for s, pal, (a, sp, b) in zip(raw, palettes, timing(raw, cuts)):
        _, scene, _ = parse_plate(s)
        words = s["narration"].strip().split()
        step = (sp - a) / max(1, len(words))
        out.append(dict(n=s["n"], a=a, b=b, scene=scene, palette=pal,
                        real=bool(cuts and any(c["n"] == s["n"] for c in cuts)),
                        words=[(w, a + i * step, a + (i + 1) * step) for i, w in enumerate(words)]))
    # A shot without a scene context stays in the nearest described scene (previous, else next): in a
    # continuous take the picture cannot jump to "a recreation of <sentence>" and back.
    described = [i for i, sh in enumerate(out) if sh["scene"]]
    for i, sh in enumerate(out):
        if not sh["scene"] and described:
            j = max((d for d in described if d < i), default=None)
            j = j if j is not None else min(d for d in described if d > i)
            sh["scene"], sh["palette"] = out[j]["scene"], sh["palette"] or out[j]["palette"]
    return base, out


def windows(shots):
    end = shots[-1]["b"]
    k, out = 0, []
    while k * CLIP_S < end - 0.25:
        out.append((k * CLIP_S, min((k + 1) * CLIP_S, end)))
        k += 1
    return out


def find_cuts(ep_dir):
    """The builder's real-voice cut points: the cuts.json that covers the most shots, newest first."""
    cands = [p for p in (ep_dir / "_v5").glob("**/cuts.json") if "_superseded" not in str(p)]
    best = None
    for p in sorted(cands, key=lambda p: p.stat().st_mtime, reverse=True):
        c = json.loads(p.read_text(encoding="utf-8"))
        if best is None or len(c) > len(best[1]):
            best = (p, c)
    return best


def worksheet(tag, shots, wins, cuts):
    real_end = max((sh["b"] for sh in shots if sh["real"]), default=0.0)
    out = [f"# {tag} - Gate 2A worksheet (Omni chain)", "",
           f"{len(wins)} clips x 10 s = {len(wins) * 10 // 60} min {len(wins) * 10 % 60} s. Real voice up to "
           f"{real_end:.1f} s ({sum(1 for w in wins if w[1] <= real_end + 1e-6)} clips final), estimate after that.",
           f"The 2-min sample = clips 1-{SAMPLE_CLIPS} (gate 2B). Picture per clip is authored in {tag}_omni_plan.json.",
           "", "| clip | time | narration (words in this clip) | shots | shotlist chapter / palette (new ones only) |",
           "|---|---|---|---|---|"]
    seen = set()
    for k, (w0, w1) in enumerate(wins, 1):
        words, ns, ctx = [], [], []
        for sh in shots:
            ws = [w for w, a, b in sh["words"] if w0 <= (a + b) / 2 < w1]
            if not ws and not (sh["a"] < w1 and sh["b"] > w0):
                continue
            words += ws
            ns.append(str(sh["n"]))
            key = (scene_key(sh["scene"]), sh["palette"][:40])
            if key not in seen:
                seen.add(key)
                ctx.append(f"{scene_desc(sh['scene'])[:120]} / {sh['palette'].split(':')[0] or 'no palette'}")
        m0, s0 = divmod(int(w0), 60)
        m1, s1 = divmod(int(round(w1)), 60)
        out.append(f"| {k:03d} | {m0}:{s0:02d}-{m1}:{s1:02d} | {' '.join(words)} | {','.join(ns)} | "
                   f"{'; '.join(ctx)} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    ap.add_argument("--manifest", help="use this shotlist json instead of the episode's newest one")
    ap.add_argument("--cuts", help="real-voice cuts.json (default: the episode's _v5/*/cuts.json covering most shots)")
    ap.add_argument("--out", help="output dir (default: _FLOW next to this script)")
    a = ap.parse_args()
    tag = f"{a.channel}{a.episode}".upper()
    cuts = json.loads(pathlib.Path(a.cuts).read_text(encoding="utf-8")) if a.cuts else None
    if a.manifest:
        raw = json.loads(pathlib.Path(a.manifest).read_text(encoding="utf-8"))
    else:
        from _rx_flow_prompts import manifest
        ep_dir, raw = manifest(a.channel, a.episode)
        if cuts is None and (found := find_cuts(ep_dir)):
            print(f"real voice timing: {found[0]} ({len(found[1])} shots)")
            cuts = found[1]
    raw = sorted(raw, key=lambda s: s["n"])
    if [s["n"] for s in raw] != list(range(1, len(raw) + 1)):
        sys.exit("shot numbers are not 1..N without gaps")
    _, shots = load_shots(raw, cuts)
    wins = windows(shots)
    out = pathlib.Path(a.out) if a.out else pathlib.Path(__file__).resolve().parent / "_FLOW"
    out.mkdir(parents=True, exist_ok=True)
    words = [[w, round(s, 3), round(e, 3)] for sh in shots for w, s, e in sh["words"]]
    real_end = max((sh["b"] for sh in shots if sh["real"]), default=0.0)
    (out / f"{tag}_omni_words.json").write_text(json.dumps(
        {"tag": tag, "clips": len(wins), "real_until_s": round(real_end, 2), "words": words},
        ensure_ascii=False), encoding="utf-8")
    (out / f"{tag}_omni_GATE2A.md").write_text(worksheet(tag, shots, wins, cuts), encoding="utf-8")
    print(f"{tag}: {len(raw)} shots -> {len(wins)} clips; real voice until {real_end:.1f} s")


if __name__ == "__main__":
    main()
