CH01EP19 - Omni Flash chain (ch01 ep19) - clips 1-156 of 156 (26 min 0 s)

1. FIRST FRAME  (only for clip 1)
   TurboFlow -> Mode Image -> Nano Banana Pro -> 16:9 -> Images per prompt x2 -> 2K Upscale
   Prompt: CH01EP19_omni_first_frame.txt    Save folder: ch01ep19-omni    prefix: ff  sep _  start 1
   Claude looks at ff_001 + ff_001b and picks (reject black bars, borders, burned-in text).

2. CHAIN
   TurboFlow -> Mode Video -> Omni Flash -> 16:9 -> x1 -> Duration 10s -> Video mode Start -> 360p OFF
   Start frame: the picked first frame (Choose Start Frame -> Upload New)
   Continue from last frame: ON   (never "Different for Each" with chaining)
   Settings: Save folder ch01ep19-omni . Auto-download videos . Video quality 1080p Upscale
             File naming custom prefix: clip  sep _  start number 1
   Prompts: import CH01EP19_omni_chain.txt (156 prompts, each {...} block = 1 prompt)
   CHECK before Run: Queue tab row shows the "continuous" tag. No tag = not chained.
   Output: Downloads\ch01ep19-omni\clip_001.mp4 ... clip_156.mp4

3. After a stop / failures: Retry Failed keeps the numbering. A chain that broke mid-way resumes with
   --range K-156: its start frame is the last frame of the last good clip.

Clip k covers narration est CH01EP19_omni_clipmap.json -> est_window; the assembler retimes each clip onto the
real voice (cuts.json), so small drift between estimate and real VO is expected and handled there.
