CH02EP16 - Omni Flash chain, clips 1-112 (18 min 40 s)

1. FIRST FRAME  (made by Claude, not in TurboFlow)
   AI33 image model at the highest quality (gpt-image-2, 4K, quality high - or the newer top model if AI33
   lists one), 16:9, 2 variants from CH02EP16_omni_first_frame.txt. Claude looks at both and picks
   (no black bars, borders, burned-in text, extra limbs) and delivers CH02EP16_first_frame.png.

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: CH02EP16_first_frame.png (the picked AI33 master image)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder ch02ep16-omni . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: clip  sep _  start number 1
   Prompts: import CH02EP16_omni_clips_001-112.txt (112 prompts, each {...} block = 1 prompt)
   CHECK before Run: the Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\ch02ep16-omni\clip_001.mp4 ... clip_112.mp4

3. Failures: Retry Failed keeps the numbering. If the chain breaks, render the rest from a new plan chunk
   whose start frame is the last frame of the last good clip.
