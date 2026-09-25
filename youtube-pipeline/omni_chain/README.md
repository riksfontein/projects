# Omni Flash chain — gate 2A to the 2-min samples (2026-09-25)

Method (Riks, screen share 2026-09-24): ONE first frame for clip 1 (image-to-video), every next 10 s Omni
Flash clip continues from the last frame of the previous clip (TurboFlow "Continue from last frame").
Prompts are very detailed JSON (ch03 v4 format) with the anti-glitch rules from the v3/v4 chain tests.

## Pipeline
1. **Gate 2A** — `_rx_omni_timing.py --channel ch01 --episode ep19` → `<TAG>_omni_GATE2A.md` (clip worksheet:
   which narration falls in which 10 s clip, on the real voice where a `cuts.json` exists) + `<TAG>_omni_words.json`.
2. **Author** the picture per clip in `<TAG>_omni_plan.json`: environment, cast with exact counts, one camera
   move per scene, timestamped beats, at most one scene change per clip (a camera bridge, never in the last 3 s).
3. **Render** — `_rx_omni_render.py _FLOW/<TAG>_omni_plan.json` → `<TAG>_omni_first_frame.txt`,
   `<TAG>_omni_clips_001-012.txt` (TurboFlow import: one `{...}` block = one prompt), README with settings.
   The renderer adds to every prompt: exact narration per beat, channel look word for word, continuity +
   camera rules, `continue_from`, clean last frame, "no audio", full negative list; and checks beats/changes/words.
4. **Gate 2B** = the 2-min sample (clips 1-12). Approved → next plan chunk (clips 13-24 …) starts from the
   last frame of clip_012, so the sample IS the first 2 minutes of the episode.

## 2-min samples in `_FLOW/` and `ch03/_FLOW/`
| sample | clips | voice timing |
|---|---|---|
| CH01EP19 (Ancient Earth, PETM) | 1-12 | real (sample 1-29 cuts) |
| CH02EP16 (ROKS Cheonan) | 1-12 | real (sample 1-29 cuts) |
| CH02EP17 (USS Pueblo) | 1-12 | ESTIMATE — no narration built yet; re-time before rendering |
| CH03EP10 A photoreal (Unraveling) · B stickfigure painted · C engraving collage · D painted (Night Psalms) · E chibi painted | 1-12 each | ep10 narration 0:00-2:00, spread per clip |

ch03 first-frame prompts are unchanged from `samples_2min/build_prompts.py`, so the existing
`A_start.png … E_start.png` are the start frames.
