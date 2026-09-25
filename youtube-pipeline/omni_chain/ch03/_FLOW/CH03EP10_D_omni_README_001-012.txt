CH03EP10_D - Omni Flash chain, clips 1-12 (2 min 0 s)

1. FIRST FRAME
   TurboFlow -> Mode Image -> Nano Banana Pro -> 16:9 -> Images per prompt x2 -> 2K Upscale
   Prompt: CH03EP10_D_omni_first_frame.txt    Save folder: ch03-samples    prefix: ff  sep _  start 1
   Claude looks at both and picks (reject black bars, borders, burned-in text, extra limbs).

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: the picked master image (ff_001 or ff_001b)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder ch03-samples . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: ch03-D  sep _  start number 1
   Prompts: import CH03EP10_D_omni_clips_001-012.txt (12 prompts, each {...} block = 1 prompt)
   CHECK before Run: the Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\ch03-samples\ch03-D_001.mp4 ... ch03-D_012.mp4

3. Failures: Retry Failed keeps the numbering. If the chain breaks, render the rest from a new plan chunk
   whose start frame is the last frame of the last good clip.
