CH03EP10_A - Omni Flash chain, clips 1-12 (2 min 0 s)

1. FIRST FRAME  (made by Claude, not in TurboFlow - nothing to generate here)
   ch03\samples_2min\A_start.png
   Made by Claude on 2026-09-24 from CH03EP10_A_omni_first_frame.txt (prompt unchanged), variants
   looked at and picked (no black bars, borders, burned-in text, extra limbs). Upload it as the Start frame.

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: ch03\samples_2min\A_start.png (the master image Claude made and picked)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder ch03-samples . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: ch03-A  sep _  start number 1
   Prompts: import CH03EP10_A_omni_clips_001-012.txt (12 prompts, each {...} block = 1 prompt)
   CHECK before Run: the Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\ch03-samples\ch03-A_001.mp4 ... ch03-A_012.mp4

3. Failures: Retry Failed keeps the numbering. If the chain breaks, render the rest from a new plan chunk
   whose start frame is the last frame of the last good clip.
