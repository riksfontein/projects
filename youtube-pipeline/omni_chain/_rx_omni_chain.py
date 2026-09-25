"""One first frame + chained Omni Flash 10 s clips for a whole episode (Riks, 2026-09-25).

    py -3.12 _rx_omni_chain.py --channel ch01 --episode ep19 [--range 1-6]

New production method (screen share 2026-09-24, TurboFlow playbook section 9): ONE master image is the
start frame of clip 1 (image-to-video); every next clip continues from the last frame of the previous
clip ("Continue from last frame" ON). No per-shot plates, no per-shot Veo clips.

Reads the episode's approved 2A shotlist (same manifest rule as _rx_flow_prompts: newest by mtime) and
cuts the narration into 10 s windows. Each window becomes one JSON prompt in the v4 chain format
(turboflow_chain_v4_narration_prompts.txt): timestamped beats that carry the exact narration they
illustrate, scene changes as continuous camera moves (never cuts), "no audio" (VO + music in post).

Writes into _FLOW/:
  <TAG>_omni_first_frame.txt  the master image prompt (Nano Banana Pro, 16:9, x2 -> Claude picks)
  <TAG>_omni_chain.txt        ONLY the JSON blocks, one {...} block = one prompt, in clip order
  <TAG>_omni_clipmap.json     clip k -> narration window + shots/words it covers (for the assembler)
  <TAG>_omni_README.txt       the exact TurboFlow settings for this episode

Timing: windows follow the shotlist's est_start/est_end. The real voice runs ~4% longer (ep19 shots
1-29: 160.6 s real vs 154.8 s est), so the assembler retimes each clip onto the real narration using
cuts.json. The prompts never need to be regenerated for that.
"""
import argparse, json, pathlib, re, sys

CLIP_S = 10.0

CHANNEL = {
    "ch01": dict(
        folder_word="AncientEarth",
        subject=("the animals, plants and landscape of the current scene with naturalistic anatomy; every "
                 "creature keeps the same species, size, colouring and number of legs while it is on screen; "
                 "no people"),
        motion_style=("natural-history documentary realism: long-lens wildlife cinematography, shallow depth of "
                      "field, soft natural light, subtle film grain, living subjects move naturally and calmly, "
                      "never a CGI, cartoon or game-engine look"),
        bridge="through drifting haze and foliage",
        neg="no people, no cartoon, no illustration, no CGI look, no game-engine look, no deformed animals",
    ),
    "ch02": dict(
        folder_word="ChronicleZero",
        subject=("generic silhouetted or partially obscured sailors, officers and figures, faces never clear, "
                 "no recognizable real people; ships, boats, aircraft and equipment keep their exact shape, "
                 "size and colour while on screen"),
        motion_style=("military-documentary recreation realism: steady cinematic camera, subtle film grain, "
                      "restrained grade, crushed blacks, natural light falloff, never a clean CGI or game look"),
        bridge="through grey sea haze and drifting spray",
        neg=("no recognizable faces, no faces turned to camera, no names or numbers painted on hulls, "
             "no readable flags or insignia, no weapons firing unless the beat says so, no gore"),
    ),
}

COMMON_NEG = ("no text, no letters, no numbers, no subtitles, no captions, no logos, no watermark, no black "
              "bars, no letterbox, no pillarbox, no border, no split-screen, no picture-in-picture, no camera "
              "HUD, no morphing, no flicker, no sudden cuts, no dissolves, no camera stop, no extra limbs, no "
              "duplicated objects")

CONTINUE = ("continue seamlessly from the current frame: same place, same subjects, same lighting, colour "
            "grade and camera speed - no cut, no jump")

PLATE_RE = re.compile(r"^a documentary frame showing:\s*(?P<narr>.*?)"
                      r"(?:\s*Scene context:\s*(?P<scene>.*?))?"
                      r"\s*(?P<style>Photorealistic .*?)\s*(?P<tail>ONE SINGLE FULL-FRAME.*)$", re.S)
SEG_RE = re.compile(r"\d+(?:\.\d+)?s-\d+(?:\.\d+)?s:\s*")
MOVE_TAIL = re.compile(r",?\s*(?:the move |the same move |the action |motion )?"
                       r"(?:beginning gently|begins gently|continues|progressing|decelerat|completes|"
                       r"settles|easing|one continuous unbroken move).*$", re.I)


def parse_plate(s):
    m = PLATE_RE.match(re.sub(r"\s+", " ", s["plate_prompt"]).strip())
    if not m:
        sys.exit(f"shot {s['n']}: plate_prompt not in the expected 'a documentary frame showing:' format")
    return m.group("narr").strip(), (m.group("scene") or "").strip().rstrip("."), m.group("style").strip()


def parse_move(s):
    """The camera move of the old per-shot Veo prompt, without its timing boilerplate."""
    raw = s.get("prompt", "")
    try:
        action = json.loads(raw[raw.index("{"):]).get("action", "")
    except (ValueError, json.JSONDecodeError):
        return "slow steady camera drift"
    for beat in s.get("beats") or []:
        action = action.replace(beat.rstrip(",. ") + ",", "").replace(beat, "")
    for seg in SEG_RE.split(action):
        seg = seg.strip(" .,")
        if not seg or seg.lower().startswith(("hold on", "the same move", "the move", "the action")):
            continue
        seg = MOVE_TAIL.sub("", seg).strip(" .,")
        if seg:
            return seg
    return "slow steady camera drift"


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


def ts(x):
    x = max(0.0, round(x * 2) / 2)  # half-second grid, like the v4 prompts
    m, s = divmod(x, 60)
    return f"{int(m):02d}:{int(s):02d}" + (".5" if s % 1 else "")


def load_shots(shots):
    base, palettes = split_style([parse_plate(s)[2] for s in shots])
    out = []
    for s, pal in zip(shots, palettes):
        narr, scene, _ = parse_plate(s)
        text = s["narration"].strip()
        words = text.split()
        a, b = float(s["est_start"]), float(s["est_end"])
        step = (b - a) / max(1, len(words))
        out.append(dict(n=s["n"], a=a, b=b, text=text, scene=scene, palette=pal, move=parse_move(s),
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


def beats_for(shots, w0, w1):
    beats = []
    for sh in shots:
        lo, hi = max(sh["a"], w0), min(sh["b"], w1)
        if hi - lo <= 0.05:
            continue
        words = [w for w, a, b in sh["words"] if w0 <= (a + b) / 2 < w1]
        beats.append(dict(shot=sh, t0=lo - w0, t1=hi - w0, words=" ".join(words),
                          head=sh["a"] >= w0 - 1e-6, tail=sh["b"] <= w1 + 1e-6))
    return beats


def beat_action(bt, prev_shot, ch):
    """Describe a scene only when it changes; otherwise just the move (the scene is in 'environment')."""
    sh = bt["shot"]
    if not bt["head"]:  # this shot started in an earlier clip
        return f"the same shot continues without a cut: {sh['move']}"
    if prev_shot is None:
        return f"{sh['move']}: {scene_desc(sh['scene'])}"
    if prev_shot["scene"] == sh["scene"]:
        return f"the camera keeps moving in the same scene: {sh['move']}"
    if scene_key(prev_shot["scene"]) == scene_key(sh["scene"]):
        return f"the camera moves on within the same place, {sh['move']}, to show: {scene_desc(sh['scene'])}"
    return (f"without any cut the camera glides on {CHANNEL[ch]['bridge']} and the view opens onto a new "
            f"scene, {sh['move']}: {scene_desc(sh['scene'])}")


def clip_json(k, w0, w1, beats, prev_shot, base_style, ch, first):
    c = CHANNEL[ch]
    d = {}
    if not first:
        d["continue_from"] = CONTINUE
    d["shot"] = {"duration_s": 10, "aspect": "16:9", "resolution": "720p",
                 "camera": ("slow, smooth, continuous camera movement at constant speed in one unbroken take; "
                            "every change of scene is a camera move, never a cut; the camera never stops and is "
                            "still moving in the final frame")}
    d["subject"] = c["subject"]
    scenes = list(dict.fromkeys(scene_desc(bt["shot"]["scene"]) for bt in beats))
    d["action"] = ("illustrate the narration beat by beat in one continuous take"
                   + (f", moving through {len(scenes)} scenes without cuts" if len(scenes) > 1 else ""))
    d["environment"] = " -- then -- ".join(scenes)
    tl, p = [], prev_shot
    for i, bt in enumerate(beats):
        t1 = CLIP_S if i == len(beats) - 1 else bt["t1"]  # last beat always runs to 00:10
        e = {"t": f"{ts(bt['t0'])}-{ts(t1)}"}
        if bt["words"]:
            e["narration"] = bt["words"]
        e["action"] = beat_action(bt, p, ch)
        tl.append(e)
        p = bt["shot"]
    d["timeline"] = tl
    pal = " ".join(dict.fromkeys(bt["shot"]["palette"] for bt in beats if bt["shot"]["palette"]))
    if pal:
        d["lighting"] = pal
    d["style"] = base_style
    d["motion_style"] = c["motion_style"]
    d["audio"] = "no audio"
    d["additional_details"] = ("silent visual scene for a voice-over narration; nobody speaks; the narration "
                               "lines are the story to show, never text on screen; smooth continuous motion "
                               "from the first to the last frame; the final frame is sharp and clean, without "
                               "motion blur, because the next clip continues from it")
    d["negative"] = f"{COMMON_NEG}, {c['neg']}"
    return json.dumps(d, ensure_ascii=False, indent=1)


def image_prompt(raw_shots, shots, base_style, first_clip_shots):
    """The master frame sets the look of the WHOLE video (Riks, 2026-09-24): clip 1's first described
    scene + its palette + the channel style + the approved no-text/no-bars tail of the plate prompts."""
    pick = next(sh for sh in shots if sh["n"] in first_clip_shots)
    tail = PLATE_RE.match(re.sub(r"\s+", " ", raw_shots[pick["n"] - 1]["plate_prompt"]).strip()).group("tail")
    return (f"Cinematic 16:9 film still, the opening frame of a documentary. Scene: {scene_desc(pick['scene']).rstrip('.')}. "
            f"{pick['palette']} {base_style} Generous space around the main subject, everything important "
            f"fully inside the frame, a calm composition the camera can start moving from. {tail}").replace("  ", " ")


def build(raw_shots, ch, rng=None):
    raw_shots = sorted(raw_shots, key=lambda s: s["n"])
    ns = [s["n"] for s in raw_shots]
    if ns != list(range(1, len(ns) + 1)):
        sys.exit("shot numbers are not 1..N without gaps")
    base, shots = load_shots(raw_shots)
    wins = windows(shots)
    lo, hi = rng or (1, len(wins))
    blocks, cmap, prev = [], [], None
    for k, (w0, w1) in enumerate(wins, 1):
        beats = beats_for(shots, w0, w1)
        if lo <= k <= hi:
            blocks.append(clip_json(k, w0, w1, beats, prev, base, ch, first=(k == 1)))
            json.loads(blocks[-1])
        cmap.append({"clip": k, "file": f"clip_{k:03d}.mp4", "est_window": [round(w0, 2), round(w1, 2)],
                     "shots": [{"n": bt["shot"]["n"], "t": [round(bt["t0"], 2), round(bt["t1"], 2)],
                                "words": bt["words"]} for bt in beats]})
        prev = beats[-1]["shot"] if beats else prev
    img = image_prompt(raw_shots, shots, base, {x["n"] for x in cmap[0]["shots"]})
    return img, blocks, cmap, (lo, hi, len(wins))


def readme(tag, ch, ep, lo, hi, n):
    fold = f"{tag.lower()}-omni"
    resume = "" if lo == 1 else (
        f"\nTHIS FILE STARTS AT CLIP {lo}: set the start frame to the LAST frame of clip_{lo - 1:03d}.mp4 "
        f"(not the master image), naming start number {lo}.\n")
    return f"""{tag} - Omni Flash chain ({ch} {ep}) - clips {lo}-{hi} of {n} ({n * 10 // 60} min {n * 10 % 60} s)
{resume}
1. FIRST FRAME  (only for clip 1)
   TurboFlow -> Mode Image -> Nano Banana Pro -> 16:9 -> Images per prompt x2 -> 2K Upscale
   Prompt: {tag}_omni_first_frame.txt    Save folder: {fold}    prefix: ff  sep _  start 1
   Claude looks at ff_001 + ff_001b and picks (reject black bars, borders, burned-in text).

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: the picked first frame (Choose Start Frame -> Upload New)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder {fold} . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: clip  sep _  start number {lo}
   Prompts: import {tag}_omni_chain.txt ({hi - lo + 1} prompts, each {{...}} block = 1 prompt)
   CHECK before Run: Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\\{fold}\\clip_{lo:03d}.mp4 ... clip_{hi:03d}.mp4

3. After a stop / failures: Retry Failed keeps the numbering. A chain that broke mid-way resumes with
   --range K-{n}: its start frame is the last frame of the last good clip.

Clip k covers narration est {tag}_omni_clipmap.json -> est_window; the assembler retimes each clip onto the
real voice (cuts.json), so small drift between estimate and real VO is expected and handled there.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True, choices=sorted(CHANNEL))
    ap.add_argument("--episode", required=True)
    ap.add_argument("--range", help="clip range, e.g. 1-6 for a test run (default: all)")
    ap.add_argument("--manifest", help="use this shotlist json instead of the episode's newest one")
    ap.add_argument("--out", help="output dir (default: _FLOW next to this script)")
    a = ap.parse_args()
    tag = f"{a.channel}{a.episode}".upper()
    if a.manifest:
        raw = json.loads(pathlib.Path(a.manifest).read_text(encoding="utf-8"))
    else:
        from _rx_flow_prompts import manifest
        _, raw = manifest(a.channel, a.episode)
    rng = tuple(int(x) for x in a.range.split("-")) if a.range else None
    img, blocks, cmap, (lo, hi, n) = build(raw, a.channel, rng)
    out = pathlib.Path(a.out) if a.out else pathlib.Path(__file__).resolve().parent / "_FLOW"
    out.mkdir(parents=True, exist_ok=True)
    suf = "" if (lo, hi) == (1, n) else f"_{lo:03d}-{hi:03d}"
    (out / f"{tag}_omni_first_frame.txt").write_text(img + "\n", encoding="utf-8")
    (out / f"{tag}_omni_chain{suf}.txt").write_text("\n".join(blocks) + "\n", encoding="utf-8")
    (out / f"{tag}_omni_clipmap.json").write_text(json.dumps(cmap, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / f"{tag}_omni_README{suf}.txt").write_text(readme(tag, a.channel, a.episode, lo, hi, n), encoding="utf-8")
    print(f"{tag}: {len(raw)} shots -> {n} clips; wrote clips {lo}-{hi} to {out}")


if __name__ == "__main__":
    main()
