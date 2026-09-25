# Omni Flash chain — ch01 ep19, ch02 ep16, ch02 ep17 (2026-09-25)

New method (Riks, screen share 2026-09-24): ONE first-frame image for clip 1 (image-to-video), every next
10 s Omni Flash clip continues from the last frame of the previous clip (TurboFlow "Continue from last frame").

`_rx_omni_chain.py` turns an episode's approved 2A shotlist into TurboFlow inputs. On the laptop it lives
next to `_rx_flow_prompts.py` in the Youtube Pipeline root and writes to `_FLOW\`:

    py -3.12 _rx_omni_chain.py --channel ch02 --episode ep17
    py -3.12 _rx_omni_chain.py --channel ch02 --episode ep16
    py -3.12 _rx_omni_chain.py --channel ch01 --episode ep19

`_FLOW/` here holds the same output, generated from the current manifests
(ep19_shots001-324, ep16_shots001-216, ep17_shots001-190):

| episode | shots | clips | runtime (est.) |
|---|---|---|---|
| CH01EP19 | 324 | 156 | 26:00 |
| CH02EP16 | 216 | 112 | 18:40 |
| CH02EP17 | 190 | 102 | 17:00 |

Per episode: `_omni_first_frame.txt` (image prompt), `_omni_chain.txt` (JSON prompts only, import into
TurboFlow), `_omni_README.txt` (exact settings), `_omni_clipmap.json` (clip -> narration window, for assembly).
