"""ch03 archetype test, v2: 5 styles x (1 first frame + 12 chained Omni prompts) = five 2-min samples.

    py -3.12 ch03_samples_v2.py            (writes 5 plans + renders them with _rx_omni_render.py)

Same story beats as samples_2min/build_prompts.py (ep10 "Enoch Saw Them", narration.wav 0:00-2:00,
voice clone_2610497 @0.95, 10 s per clip). The first-frame image prompts are UNCHANGED, so the start
images made on 2026-09-24 (samples_2min/A..E_start.png) stay valid.

What v2 adds (anti-glitch, from the v3/v4 chain tests):
  - exact counts per clip (2 figures -> 4 archangels -> 6 -> 7), no "more angels" without a number;
  - the path -> high ledge jump (clip 6 -> 7) is now a camera bridge, never a cut;
  - a stability block per style (outlines never boil, brush texture never swims, engraving never crawls);
  - style A (photoreal): the Watchers are rigid carved stone statues that never move (v3 moving Watchers
    lost their wings / glitched); faces of archangels stay lost in glare; Enoch's face never shown;
  - the narration is split over the timestamped beats; camera never stops (anti end-of-clip glitch);
  - everything the renderer adds to every prompt: continuity rules, full negative list, clean last frame.
"""
import json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
RENDER = HERE.parent / "_rx_omni_render.py"

STYLES = {
    "A_photoreal_unraveling": dict(
        prefix="ch03-A",
        lens="40 mm anamorphic lens, shallow depth of field",
        style=("photoreal cinematic biblical epic, desaturated grey-blue grade with warm golden light where the "
               "archangels appear, deep atmospheric haze, fine 35mm film grain, anamorphic lens look, shallow "
               "depth of field, monumental scale, uncanny stillness"),
        enoch=("Enoch: an old prophet with long grey hair and a long grey beard, rough undyed grey-beige wool robe "
               "with a frayed hem and a rope belt, barefoot, one tall plain wooden staff in his right hand, seen "
               "from behind or from the side, his face never turned to the camera"),
        angels=("archangels: very tall figures of warm light in pale white robes with huge white feathered wings, "
                "their faces lost in a soft bright glare; fallen angels (Watchers): huge hooded figures in dark grey "
                "robes with dark feathered wings, faces hidden in their hoods, carved from grey stone like statues"),
        motion="realistic, slow and weighty motion; the camera always glides smoothly at constant speed",
        stability=("the Watchers are carved grey stone statues: completely rigid, they never move - no heads "
                   "turning, no hoods shifting, no wings moving, no hands moving; statues passing the frame edges "
                   "keep their exact shape; Enoch carries one solid straight staff"),
        neg=("no visible angel faces, no face of Enoch turned to camera, no cartoon look, no fast motion, no moving "
             "statues, no birds, nothing flying except fine embers or snow"),
        watchers_rigid=True,
        intro=("Photorealistic cinematic film still from an ancient biblical epic, 16:9, 40mm anamorphic lens, low "
               "camera behind two figures, shallow depth of field."),
    ),
    "B_stickfigure_painted_bernard": dict(
        prefix="ch03-B",
        lens="flat 2D cartoon framing, no lens distortion",
        style=("2D cartoon illustration: simple round-head stick figures (plain white round heads with small dot "
               "eyes and simple line mouths, thin clean black stick bodies and limbs) placed on richly painted, "
               "painterly digital backgrounds with visible brush texture and atmospheric colour; the figures stay "
               "flat and clean, the backgrounds are painted; comedic history-explainer look"),
        enoch=("Enoch: a round-head stick figure with a plain white round head, dot eyes, a long white beard drawn as "
               "one simple shape, a simple flat brown robe over the stick body, a tall brown wooden staff in his "
               "right hand"),
        angels=("archangels: round-head stick figures in simple glowing white robes with flat white feathered wings "
                "and thin gold halo rings; fallen angels (Watchers): round-head stick figures with grey heads, sad "
                "faces and flat dark-grey wings"),
        motion=("simple cartoon motion, clean lines that never wobble or redraw; the camera pans and drifts slowly "
                "across the painted backgrounds"),
        stability=("clean black outlines never wobble, boil or redraw; round heads stay perfectly round; the flat "
                   "figures stay flat and the painted background texture never flickers; mouths stay closed"),
        neg="no 3D, no photoreal people, no talking, no lip movement, no speech bubbles",
        intro="2D cartoon illustration, 16:9 wide shot: round-head stick figures on a richly painted, painterly digital background.",
    ),
    "C_engraving_collage_hochelaga": dict(
        prefix="ch03-C",
        lens="flat printed-page framing, no lens effects",
        style=("animated collage in the style of 19th-century steel engravings and Gustave Dore woodcut Bible "
               "illustrations: fine black cross-hatched line art on aged parchment tones, combined with gold-leaf "
               "Byzantine icon elements and flat black silhouette shapes; limited palette of parchment, sepia, "
               "black and burnished gold; subtle paper grain; moves like a slow living engraving"),
        enoch="Enoch: an old bearded prophet drawn in fine engraved cross-hatching, long robe and mantle, tall staff in his right hand",
        angels=("archangels: tall engraved angels with great feathered wings and gold-leaf icon halos, calm solemn "
                "faces in the Byzantine icon manner; fallen angels (Watchers): dark engraved hooded winged figures, "
                "partly flat black silhouettes"),
        motion=("slow, solemn motion; engraved lines stay crisp and stable, hatching never flickers; the camera "
                "drifts slowly like a pan across a printed page"),
        stability=("engraved lines and cross-hatching stay crisp and fixed, they never crawl, shimmer or flicker; "
                   "gold leaf stays in place; figures move only slowly and minimally"),
        neg="no photoreal look, no bright saturated colours, no 3D, no cartoon faces",
        intro=("Old master engraving illustration, 16:9, in the style of a 19th-century Gustave Dore Bible woodcut "
               "combined with gold-leaf Byzantine icon elements, on aged parchment."),
    ),
    "D_painted_nightpsalms": dict(
        prefix="ch03-D",
        lens="painterly framing, soft focus falloff",
        style=("luminous digital oil painting in the manner of classical religious painting: rich visible "
               "brushwork, glowing golden divine light against deep night blue, dramatic chiaroscuro, heavenly light "
               "rays, soft painterly edges, reverent and calm"),
        enoch=("Enoch: an old prophet with a long white beard and flowing white hair, simple earth-brown and blue "
               "robes, a tall wooden staff in his right hand, painted in soft oil brushwork"),
        angels=("archangels: radiant angels in flowing white and gold robes with great luminous white wings, soft "
                "glowing light around them; fallen angels (Watchers): dark hooded winged figures in shadow"),
        motion="gentle, dreamlike slow motion like a living painting; brush texture stays stable; the camera drifts slowly",
        stability=("the brush texture is stable and never swims, crawls or boils; soft painterly edges stay "
                   "constant; figures move only slowly and gently"),
        neg="no photoreal skin, no cartoon look, no harsh fast motion",
        intro=("Luminous digital oil painting in a classical religious style, 16:9, rich brushwork, glowing golden "
               "light against deep night blue."),
    ),
    "E_chibi_painted_historically": dict(
        prefix="ch03-E",
        lens="flat 2D animation framing, no lens distortion",
        style=("2D animated cartoon: cute chibi characters with big round heads, small bodies, simple expressive "
               "faces, clean dark outlines and soft cel shading, placed on richly painted, detailed backgrounds; "
               "polished history-explainer animation look with moody atmospheric colour"),
        enoch=("Enoch: a chibi old man with a big round head, a long fluffy white beard, kind worried eyes, a simple "
               "brown robe and a tall wooden staff in his right hand"),
        angels=("archangels: chibi angels with big round heads, calm faces, glowing white robes, big fluffy white "
                "wings and golden halo rings; fallen angels (Watchers): chibi hooded figures with sad faces and dark "
                "grey wings"),
        motion=("smooth, bouncy cartoon motion with clean stable outlines; the camera pans and drifts slowly across "
                "the painted backgrounds"),
        stability=("clean outlines stay stable and never boil; big round heads keep their shape; mouths stay "
                   "closed; the painted background never flickers"),
        neg="no photoreal people, no 3D render, no talking, no lip movement, no speech bubbles",
        intro="2D animated cartoon still, 16:9 wide shot: cute chibi characters with big round heads on a richly painted, detailed background.",
    ),
}

# 12 clips x 10 s. {W:...|...} = Watchers wording: first = moving (B-E), second = rigid statues (A).
CLIPS = [
    dict(n=("This place is the prison of the angels, and here they will be imprisoned for ever. Those are the "
            "words Uriel spoke when he showed Enoch the darkest place"),
         env=("the rim of a colossal dark chasm at the edge of the world; far below, faint red fire glows and bound "
              "winged fallen angels hang in chains on rocky ledges; cold mist drifts over the edge"),
         cast=("exactly two figures in the foreground: Enoch and the archangel Uriel, both seen from behind; far "
               "below, small distant bound fallen angels that stay still"),
         action="Enoch and the archangel Uriel stand at the rim of the vast prison chasm and look down into it",
         camera="slow push-in over the shoulders of Enoch and Uriel standing at the rim",
         beats=[("00:00-00:05", "slow push-in over the shoulders of Enoch and Uriel standing still at the rim; embers drift slowly up from the depth"),
                ("00:05-00:10", "Uriel slowly lifts his arm and points down into the chasm; Enoch leans forward and grips his staff; the camera keeps gliding forward")]),
    dict(n=("outside Eden. Stay with this video. You will learn three things. You will see what waits beyond the "
            "corner-stone of the earth,"),
         env=("the prison chasm seen from above: layer after layer of rocky ledges with chained fallen angels, red "
              "fire deep below; on the far rim a colossal carved corner-stone block rests at the edge of the world"),
         cast=("Enoch and Uriel leave the frame behind the camera in the first seconds; then only small distant "
               "chained fallen angels that stay still, and one colossal corner-stone"),
         action="the camera glides out over the chasm and reveals its depth and the corner-stone of the earth",
         camera="a glide past Enoch and Uriel out over the edge, a slow tilt down into the depth, then a slow pan up to the far rim",
         rigid="the chained figures and the corner-stone never move",
         beats=[("00:00-00:06", "the camera glides past Enoch and Uriel out over the edge and tilts down into the depth: chains, bound winged figures, rising embers"),
                ("00:06-00:10", "the camera pans slowly up to the far rim, where the enormous carved corner-stone of the earth comes into view")]),
    dict(n=("why stars can be bound for missing their appointed time, and what the text actually says apart from "
            "Dante and the internet. Before Enoch saw the prison, he pleaded"),
         env=("a deep night sky above the chasm; seven bright stars hang in the sky, each bound by thin glowing chains "
              "of light; below, the rim of the chasm where Enoch and Uriel stand"),
         cast=("exactly seven bound stars; then exactly two figures on the rim: Enoch and Uriel"),
         action="the camera tilts up to seven stars bound in chains of light, then sweeps back down to Enoch",
         camera="a slow tilt up from the corner-stone to the sky, then a smooth sweep back down and around to Enoch",
         rigid="exactly seven stars, they never multiply or move; their chains of light stay fixed",
         beats=[("00:00-00:06", "the camera tilts up from the corner-stone to the sky: seven stars flicker softly, each wrapped in thin chains of light"),
                ("00:06-00:10", "the camera sweeps smoothly back down and around to Enoch as he turns away from the edge, Uriel beside him")]),
    dict(n=("for the Watchers. Chapters twelve through sixteen record that plea. The angels who descended to earth, "
            "who took human wives,"),
         env=("a stone path leading away from the chasm, lined on both sides with kneeling hooded fallen angels (the "
              "Watchers) with dark folded wings, their hands raised toward Enoch; the path ahead is empty"),
         cast=("exactly one walking figure: Enoch (Uriel stays behind, out of frame); on both sides a row of kneeling "
               "Watchers, about five on each side"),
         action="Enoch walks back along a path lined with kneeling fallen Watchers who plead with him",
         camera="slow tracking beside Enoch at walking pace",
         beats=[("00:00-00:05", "Enoch walks slowly along the path; the camera tracks beside him at walking pace"),
                ("00:05-00:10", "{W:on both sides the kneeling Watchers slowly raise their hands toward him in a silent plea|on both sides the kneeling Watchers hold their carved stone hands raised toward him in a frozen plea, completely still}; Enoch keeps walking")]),
    dict(n=("who taught war and metalwork and cosmetics, had asked Enoch to speak for them. He did so, and when the "
            "prayer was finished,"),
         env=("the path of kneeling Watchers; three of them hold objects: a bronze sword, a smith's hammer over a "
              "glowing ingot, a small alabaster jar of cosmetics"),
         cast=("exactly one figure standing, then kneeling: Enoch; the kneeling Watchers along the path, three of "
               "them holding exactly one object each: a sword, a hammer over a glowing ingot, an alabaster jar"),
         action="the camera passes three Watchers holding what they taught; Enoch kneels and prays for them",
         camera="a slow lateral glide past the three Watchers, then a slow circle around Enoch",
         beats=[("00:00-00:05", "the camera glides past the three Watchers one by one: {W:the sword, the hammer over the glowing ingot, the alabaster jar|carved stone hands holding a sword, a hammer over a faintly glowing ingot, and an alabaster jar, all perfectly still}"),
                ("00:05-00:10", "Enoch kneels in the middle of the path and raises both open hands toward the sky in prayer; the camera slowly circles him")]),
    dict(n=("the angels who had not fallen took him by the hand. Uriel was there, and Raphael stood with him, and "
            "Michael was present, and Gabriel was at his side."),
         env="the same path of kneeling Watchers; a warm golden light pours down from above into the grey scene",
         cast=("Enoch; then archangels arriving one by one until there are exactly four archangels: Uriel, Raphael, "
               "Michael and Gabriel"),
         action="warm light breaks through; four archangels of light arrive one by one and one takes Enoch by the hand",
         camera="a slow continuous drift around the group",
         rigid="exactly four archangels at the end, never more; the Watchers stay where they are",
         beats=[("00:00-00:03", "warm light pours down; Uriel steps out of the light and takes Enoch by the hand, lifting him to his feet"),
                ("00:03-00:05.5", "a second archangel of light steps out of the glow and stands at Enoch's side"),
                ("00:05.5-00:08", "a third archangel steps out of the glow and joins them"),
                ("00:08-00:10", "a fourth archangel steps out of the glow; exactly four archangels now stand with Enoch; the camera keeps drifting slowly")]),
    dict(n=("Chapter twenty names them and gives their posts. Uriel stands over the world and over Tartarus. "
            "Raphael over the spirits of men. Michael over the people."),
         env=("the path of kneeling Watchers -- then -- a high rocky ledge above the world; below, the dark chasm of "
              "Tartarus on one side and a distant valley with the tiny lamps of a human city on the other"),
         cast="exactly five figures: Enoch and the four archangels Uriel, Raphael, Michael and Gabriel",
         action="the archangels stand around Enoch on a high ledge and each gestures toward the domain he rules",
         camera="a slow rise through the warm glow, then a slow arc around the group",
         change_at=0.0,
         beats=[("00:00-00:01.5", "without any cut the camera rises through the warm glow around the group; as the glow thins, the five figures stand on a high rocky ledge above the world"),
                ("00:01.5-00:04", "the camera arcs slowly around the four archangels standing in a semicircle around Enoch"),
                ("00:04-00:07", "Uriel gestures down toward the dark chasm; Raphael opens his hands and small soft lights like spirits rise gently around him"),
                ("00:07-00:10", "Michael gestures toward the distant valley where the lamps of a human city glow")]),
    dict(n=("Gabriel over paradise and the serpents and the cherubim. Raguel takes vengeance on the world for the "
            "luminaries. Sariel"),
         env=("the same high ledge; far away on a mountain top a glowing green garden of paradise, guarded by winged "
              "cherubim of flame-like light"),
         cast="Enoch and four archangels; then two more archangels descend: exactly six archangels at the end",
         action="Gabriel points to the distant paradise; two more archangels arrive",
         camera="a slow continuous drift along the ledge",
         rigid="exactly six archangels at the end, never more",
         beats=[("00:00-00:04", "Gabriel raises his hand toward the distant glowing garden on the mountain, guarded by cherubim of fiery light"),
                ("00:04-00:07", "a fifth archangel of light descends gently onto the ledge and joins the group"),
                ("00:07-00:10", "a sixth archangel of light descends and joins them; the camera keeps drifting slowly")]),
    dict(n=("is set over the spirits of mankind who sin in the spirit. Remiel over those who rise. These are not "
            "anonymous voices in a dream. They are named authorities"),
         env="the same high ledge above the world, clouds drifting below",
         cast="Enoch and six archangels; then the seventh arrives: exactly seven archangels in one row with Enoch in the middle",
         action="the seventh archangel arrives and the seven stand in a row with Enoch",
         camera="a slow continuous drift that turns into a slow rise",
         rigid="exactly seven archangels, never more; they stand still once in the row",
         beats=[("00:00-00:04", "a seventh archangel of light descends and lands at the end of the row"),
                ("00:04-00:10", "the seven archangels stand in a solemn row with Enoch in the middle; the camera rises slowly, revealing the height of the ledge above the clouds")]),
    dict(n=("with assigned territories, and they lead Enoch past the edge of the known world. The text doesn't say "
            "Enoch fell asleep. It says he was shown."),
         env=("the ledge ends at the edge of the world; beyond it a path of soft light stretches out over an ocean of "
              "cloud under the stars"),
         cast="exactly eight figures: Enoch and the seven archangels, walking together",
         action="the archangels lead Enoch along a path of light past the edge of the world",
         camera="the rise turns into a slow follow behind the group at walking pace",
         beats=[("00:00-00:06", "the archangels walk with Enoch onto the path of light, leaving the edge of the world behind; the ground falls away into cloud"),
                ("00:06-00:10", "the camera follows behind them as they walk out into the open sky; Enoch looks around in awe")]),
    dict(n=("He saw the treasuries of all the winds, and how God had furnished the whole creation with them. He saw "
            "the corner-stone of the earth."),
         env=("enormous stone gates standing in the clouds, the treasuries of the winds, with swirling winds and "
              "clouds moving inside them; far below, the colossal corner-stone of the earth"),
         cast="Enoch and the seven archangels walking past; exactly four giant stone gates",
         action="they pass the colossal storehouses of the winds and the corner-stone of the earth",
         camera="a slow glide alongside the group, then a slow tilt down",
         rigid="the stone gates are rigid; only the winds and clouds inside them move",
         beats=[("00:00-00:07", "the group walks past the giant stone gates; inside each gate winds swirl like living storms; the camera glides alongside"),
                ("00:07-00:10", "the camera tilts down to the colossal corner-stone of the earth far below")]),
    dict(n=("He saw the four winds that bear up the earth and the firmament of heaven. He saw the pillars of heaven, "
            "and the winds that turn the sky and bring the sun and all the stars to their setting."),
         env=("four enormous pillars rise from the earth and hold up the dome of the sky; winds spiral around them; "
              "the sun and all the stars move across the sky toward their setting"),
         cast="Enoch and the seven archangels, small; exactly four colossal pillars",
         action="the final cosmic reveal: four pillars hold up the firmament while the sun and stars wheel to their setting",
         camera="a slow rise and pull-back into a wide monumental view",
         rigid="exactly four pillars, rigid; the figures stay small and still",
         beats=[("00:00-00:05", "the camera rises and pulls back: four colossal pillars hold up the firmament, winds spiralling around them"),
                ("00:05-00:10", "the sun and the stars wheel slowly across the sky toward their setting; Enoch and the archangels stand small before the pillars; wide monumental final frame")]),
]


def watchers(text, rigid):
    out = text
    while "{W:" in out:
        a = out.index("{W:")
        b = out.index("}", a)
        moving, still = out[a + 3:b].split("|")
        out = out[:a] + (still if rigid else moving) + out[b + 1:]
    return out


def image_prompt(s):
    """Unchanged from build_prompts.py so the 2026-09-24 start images stay valid."""
    b = CLIPS[0]
    uriel = s["angels"].split(";")[0].replace("archangels: ", "")
    enoch = s["enoch"] if s["prefix"] != "ch03-A" else (
        "Enoch: an old prophet with long grey hair and a long grey beard, rough undyed grey-beige wool robe with a "
        "frayed hem and a rope belt, barefoot, one tall plain wooden staff in his right hand")
    return (f"{s['intro']} Scene: {b['env']}. At the rim stand two figures seen from behind and slightly from the side: "
            f"{enoch}; beside him the archangel Uriel, one of the {uriel}. Uriel is about to point down into the chasm. "
            f"Style: {s['style']}. Both figures fully visible, generous space around them, the depth of the chasm clearly readable. "
            "No text, no letters, no numbers, no captions, no watermark, no signature, no logo, no border, no frame, no black bars.")


def main():
    out = HERE / "_FLOW"
    out.mkdir(exist_ok=True)
    for key, s in STYLES.items():
        rigid = s.get("watchers_rigid", False)
        clips = []
        for c in CLIPS:
            clip = {k: c[k] for k in ("env", "cast", "action", "camera") if k in c}
            clip["narration"] = c["n"]
            clip["beats"] = [[t, watchers(a, rigid)] for t, a in c["beats"]]
            for k in ("change_at", "rigid"):
                if k in c:
                    clip[k] = c[k]
            clips.append(clip)
        tag = f"CH03EP10_{key.split('_')[0]}"
        plan = {"tag": tag, "start": 1, "folder": "ch03-samples", "prefix": s["prefix"],
                "first_frame": image_prompt(s),
                "look": {"lens": s["lens"], "style": s["style"], "motion_style": s["motion"],
                         "subject": f"{s['enoch']}; {s['angels']} - identical designs, sizes and colours throughout",
                         "continuity": s["stability"], "neg": s["neg"]},
                "clips": clips}
        p = out / f"{tag}_omni_plan.json"
        p.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
        subprocess.run([sys.executable, str(RENDER), str(p)], check=True)


if __name__ == "__main__":
    main()
