CH02EP16 - Omni Flash chain, clips 13-112 (16 min 40 s)

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: the LAST frame of clip_012.mp4 (not the master image)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder ch02ep16-omni . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: clip  sep _  start number 13
   Prompts: import CH02EP16_omni_clips_013-112.txt (100 prompts, each {...} block = 1 prompt)
   CHECK before Run: the Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\ch02ep16-omni\clip_013.mp4 ... clip_112.mp4

3. Failures: Retry Failed keeps the numbering. If the chain breaks, render the rest from a new plan chunk
   whose start frame is the last frame of the last good clip.
