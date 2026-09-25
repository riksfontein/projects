"""Authored Omni clip plan -> TurboFlow chain prompts (Riks, 2026-09-25).

    py -3.12 _rx_omni_render.py _FLOW/CH01EP19_omni_plan.json

The picture of every 10 s clip is AUTHORED in a plan json (environment, cast with exact counts, camera
plan, timestamped beats); this script adds everything that must be identical in every prompt and that
glitch tests taught us, so no prompt can forget it:
  - the exact narration each beat illustrates, cut from the real voice (<TAG>_omni_words.json from
    _rx_omni_timing.py) or, for ch03 test passages, spread over the clip from the plan's narration text;
  - the channel look (lens, style, motion style, subject lock) word for word in every clip;
  - continuity rules: exact shapes and counts, rigid background, frame edges keep their shape, nothing
    appears from nowhere, constant light;
  - camera rules: start gently, one constant speed, never stop or settle, still moving in the final
    frame (v3/v4 glitch scan: glitches clustered in end-of-clip slow-downs and crane starts);
  - chaining: clip 1 starts on the master image, every next clip "continue_from" the current frame;
    the final frame is a clean frame of ONE scene because the next clip starts from it;
  - "no audio" (voice-over + music in post) and the full negative list.
Checks: beats run 00:00-00:10 without gaps, a scene change ("change_at") never starts in the last 3 s,
every narration word lands in exactly one beat.

Plan json:
  {"tag": "CH01EP19", "look": "ch01" | {...}, "start": 1, "first_frame": "...",
   "clips": [{"env": "...", "cast": "...", "action": "...", "camera": "...", "lighting": "...",
              "change_at": 5.5, "rigid": "...", "neg": "...", "narration": "(ch03 only)",
              "beats": [["00:00-00:04", "..."], ...]}]}
Writes next to the plan: <TAG>_omni_first_frame.txt, <TAG>_omni_clips_<lo>-<hi>.txt (JSON blocks only,
one {...} block = one TurboFlow prompt) and <TAG>_omni_README_<lo>-<hi>.txt.
"""
import argparse, json, pathlib, re, sys

CLIP_S = 10.0
NO_CHANGE_TAIL_S = 3.0

LOOKS = {
    "ch01": dict(
        lens=("cinema camera with natural-history lenses: long lens on animals, wide lens on landscapes, "
              "shallow depth of field on close subjects"),
        style=("Photorealistic natural-history documentary recreation, BBC/NatGeo grade, never cartoon, never "
               "illustration. Naturalistic animal anatomy and behaviour, shallow depth of field, subtle film "
               "grain, restrained cinematic grade."),
        motion_style=("natural-history documentary realism: long-lens wildlife cinematography, soft natural "
                      "light, living subjects move naturally and calmly with a correct gait, never a CGI, cartoon "
                      "or game-engine look"),
        subject=("every animal has naturalistic anatomy and keeps the same species, size, colouring, markings "
                 "and number of legs for the whole clip; no people"),
        continuity=("animals walk with a correct, steady gait and never grow, shrink, change species or change "
                    "the number of legs; fossils, bones and rocks are rigid; plants sway only gently"),
        neg=("no people, no cartoon, no illustration, no CGI look, no game-engine look, no deformed or melting "
             "animals, no extra legs, no two-headed animals, no animal changing size"),
    ),
    "ch02": dict(
        lens="documentary cinema camera, 35-50 mm lens, deep focus, natural documentary contrast",
        style=("Photorealistic simulated-footage military-documentary recreation, never cartoon. Generic "
               "silhouetted or partially obscured figures only, faces never clear, no recognizable real people. "
               "Subtle film grain, restrained cinematic grade, crushed blacks."),
        motion_style=("military-documentary recreation realism: steady cinematic camera, restrained grade, "
                      "natural light falloff, figures move slowly and naturally, never a clean CGI or game look"),
        subject=("figures are generic silhouettes or seen from behind, faces never visible, no recognizable real "
                 "people; ships, boats and equipment keep their exact shape, size, colour and number for the "
                 "whole clip"),
        continuity=("ships stay on the water at a steady heading and speed unless a beat says otherwise; hulls, "
                    "masts and antennas never bend, merge or duplicate; water, spray and silt behave physically; "
                    "figures never change clothing or turn their faces to the camera"),
        neg=("no recognizable faces, no face turned to camera, no names or numbers painted on hulls, no readable "
             "flags, insignia, labels or documents, no weapons firing, no fire, no gore, no bodies"),
    ),
}

CONTINUITY = ("every object, figure, animal and vehicle keeps its exact shape, size, colour and count for the "
              "whole clip; things passing the frame edges keep their exact shape as they leave; background "
              "structures and scenery are rigid and never deform; nothing appears out of thin air or vanishes; "
              "nothing floats unless it floats in reality; light direction and colour grade stay constant")

CAMERA_RULES = ("one smooth continuous move in one unbroken take: it starts gently, then keeps one constant "
                "speed - no sudden acceleration, no stop, no slow-down or settle at the end; the camera is still "
                "moving in the final frame")

COMMON_NEG = ("no text, no letters, no numbers, no subtitles, no captions, no logos, no watermark, no black bars, "
              "no letterbox, no pillarbox, no border, no split-screen, no picture-in-picture, no camera HUD, no "
              "timestamp, no cuts, no dissolves, no morphing, no warping, no melting, no flicker, no strobing, no "
              "sudden lighting change, no camera stop, no camera shake, no sudden acceleration, no floating "
              "objects, no objects appearing from nowhere, no extra limbs, no duplicated objects, no motion blur "
              "on the last frame")

CONTINUE = ("continue seamlessly from the current frame: same place, same subjects in the same positions, same "
            "lighting, colour grade, camera direction and camera speed - no cut, no jump")

LAST_FRAME = ("silent visual scene for a voice-over narration; nobody speaks and no mouth moves; the narration "
              "lines are the story to show, never text on screen; the final frame is a sharp, clean frame of one "
              "scene with the main subject fully visible, because the next clip starts from it")

T_RE = re.compile(r"^(\d\d):(\d\d(?:\.\d+)?)-(\d\d):(\d\d(?:\.\d+)?)$")


def secs(t):
    m = T_RE.match(t)
    if not m:
        sys.exit(f"bad beat time {t!r} (use 00:00-00:04.5)")
    return int(m[1]) * 60 + float(m[2]), int(m[3]) * 60 + float(m[4])


def beat_words(clip, k, words):
    """Narration per beat. Episode: words on the real timeline. ch03: the clip's text spread evenly."""
    if words is not None:
        w0 = (k - 1) * CLIP_S
        return [" ".join(w for w, s, e in words if w0 + a <= (s + e) / 2 < w0 + b) for a, b in
                (secs(t) for t, _ in clip["beats"])]
    toks = clip.get("narration", "").split()
    v0, v1 = clip.get("voice", [0.0, CLIP_S])
    step = (v1 - v0) / max(1, len(toks))
    out = []
    for a, b in (secs(t) for t, _ in clip["beats"]):
        out.append(" ".join(w for i, w in enumerate(toks) if a <= v0 + (i + 0.5) * step < b))
    return out


def check(clip, k):
    spans = [secs(t) for t, _ in clip["beats"]]
    if spans[0][0] != 0 or abs(spans[-1][1] - CLIP_S) > 1e-6:
        sys.exit(f"clip {k}: beats must run 00:00-00:10")
    for (a0, a1), (b0, b1) in zip(spans, spans[1:]):
        if abs(a1 - b0) > 1e-6 or a1 <= a0:
            sys.exit(f"clip {k}: beats have a gap or overlap at {a1}/{b0}")
    ca = clip.get("change_at")
    if ca is not None and ca > CLIP_S - NO_CHANGE_TAIL_S:
        sys.exit(f"clip {k}: scene change at {ca}s falls in the last 3 s - move it to the next clip")
    for f in ("env", "cast", "camera", "action"):
        if not clip.get(f):
            sys.exit(f"clip {k}: '{f}' is missing")


def render(clip, k, look, narr, first):
    d = {}
    if not first:
        d["continue_from"] = CONTINUE
    d["shot"] = {"duration_s": 10, "aspect": "16:9", "resolution": "720p", "lens": look["lens"],
                 "camera": f"{clip['camera']}; {CAMERA_RULES}",
                 "framing": clip.get("framing", ("start exactly on the first frame" if first else
                                                 "start exactly on the current frame")
                                     + "; the main subject stays fully inside the frame")}
    d["subject"] = f"{look['subject']}; in this clip: {clip['cast']}"
    d["action"] = clip["action"]
    d["environment"] = clip["env"]
    tl = []
    for (t, act), words in zip(clip["beats"], narr):
        e = {"t": t}
        if words:
            e["narration"] = words
        e["action"] = act
        tl.append(e)
    tl[-1]["action"] = tl[-1]["action"].rstrip(". ") + "; the camera is still moving in the final frame"
    d["timeline"] = tl
    if clip.get("lighting"):
        d["lighting"] = clip["lighting"]
    d["style"] = look["style"]
    d["motion_style"] = look["motion_style"]
    d["continuity"] = "; ".join(x for x in (CONTINUITY, look["continuity"], clip.get("rigid")) if x)
    d["audio"] = "no audio"
    d["additional_details"] = LAST_FRAME
    d["negative"] = ", ".join(x for x in (COMMON_NEG, look["neg"], clip.get("neg")) if x)
    return json.dumps(d, ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--words", help="<TAG>_omni_words.json (default: next to the plan)")
    a = ap.parse_args()
    plan_p = pathlib.Path(a.plan)
    plan = json.loads(plan_p.read_text(encoding="utf-8"))
    tag, start, clips = plan["tag"], plan.get("start", 1), plan["clips"]
    look = dict(LOOKS[plan["look"]]) if isinstance(plan["look"], str) else plan["look"]
    look.update(plan.get("look_extra", {}))
    words = None
    if not all("narration" in c for c in clips):
        wp = pathlib.Path(a.words) if a.words else plan_p.with_name(f"{tag}_omni_words.json")
        wj = json.loads(wp.read_text(encoding="utf-8"))
        words, real_until = wj["words"], wj["real_until_s"]
        end = (start - 1 + len(clips)) * CLIP_S
        if end > real_until + 0.5:
            print(f"WARNING {tag}: clips end at {end:.0f} s but the real voice ends at {real_until:.0f} s - "
                  f"re-run _rx_omni_timing.py once the narration is built; beats on the estimate may drift")
    blocks, used = [], 0
    for i, clip in enumerate(clips):
        k = start + i
        check(clip, k)
        narr = beat_words(clip, k, words)
        used += sum(len(x.split()) for x in narr)
        blocks.append(render(clip, k, look, narr, first=(k == 1)))
        json.loads(blocks[-1])
    if words is not None:
        w0, w1 = (start - 1) * CLIP_S, (start - 1 + len(clips)) * CLIP_S
        want = sum(1 for w, s, e in words if w0 <= (s + e) / 2 < w1)
        if want != used:
            sys.exit(f"{tag}: {want} narration words in clips {start}-{k} but {used} placed in beats")
    lo, hi = start, start + len(clips) - 1
    out = plan_p.parent
    if start == 1:
        (out / f"{tag}_omni_first_frame.txt").write_text(plan["first_frame"].strip() + "\n", encoding="utf-8")
    (out / f"{tag}_omni_clips_{lo:03d}-{hi:03d}.txt").write_text("\n".join(blocks) + "\n", encoding="utf-8")
    fold = plan.get("folder", f"{tag.lower()}-omni")
    prefix = plan.get("prefix", "clip")
    image = plan.get("start_image", f"_FLOW\\first_frames\\{tag}_first_frame.jpg")
    start_frame = (f"{image} (the master image Claude made and picked)" if lo == 1 else
                   f"the LAST frame of {prefix}_{lo - 1:03d}.mp4 (not the master image)")
    first = ("" if lo != 1 else f"""1. FIRST FRAME  (made by Claude, not in TurboFlow - nothing to generate here)
   {image}
   {plan.get("start_note", f"Made by Claude at the highest image quality (4K, 16:9) from {tag}_omni_first_frame.txt, variants")}
   looked at and picked (no black bars, borders, burned-in text, extra limbs). Upload it as the Start frame.

""")
    (out / f"{tag}_omni_README_{lo:03d}-{hi:03d}.txt").write_text(f"""{tag} - Omni Flash chain, clips {lo}-{hi} ({len(clips) * 10 // 60} min {len(clips) * 10 % 60} s)

{first}2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: {start_frame}
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder {fold} . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: {prefix}  sep _  start number {lo}
   Prompts: import {tag}_omni_clips_{lo:03d}-{hi:03d}.txt ({len(clips)} prompts, each {{...}} block = 1 prompt)
   CHECK before Run: the Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\\{fold}\\{prefix}_{lo:03d}.mp4 ... {prefix}_{hi:03d}.mp4

3. Failures: Retry Failed keeps the numbering. If the chain breaks, render the rest from a new plan chunk
   whose start frame is the last frame of the last good clip.
""", encoding="utf-8")
    print(f"{tag}: rendered clips {lo}-{hi} -> {out}")


if __name__ == "__main__":
    main()
