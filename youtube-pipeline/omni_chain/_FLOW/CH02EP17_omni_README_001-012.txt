CH02EP17 - Omni Flash chain, clips 1-12 (2 min 0 s)

1. FIRST FRAME  (made by Claude, not in TurboFlow - nothing to generate here)
   _FLOW\first_frames\CH02EP17_first_frame.jpg
   Made by Claude at the highest image quality (4K, 16:9) from CH02EP17_omni_first_frame.txt, variants
   looked at and picked (no black bars, borders, burned-in text, extra limbs). Upload it as the Start frame.

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: _FLOW\first_frames\CH02EP17_first_frame.jpg (the master image Claude made and picked)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder ch02ep17-omni . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: clip  sep _  start number 1
   Prompts: import CH02EP17_omni_clips_001-012.txt (12 prompts, each {...} block = 1 prompt)
   CHECK before Run: the Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\ch02ep17-omni\clip_001.mp4 ... clip_012.mp4

3. Failures: Retry Failed keeps the numbering. If the chain breaks, render the rest from a new plan chunk
   whose start frame is the last frame of the last good clip.
