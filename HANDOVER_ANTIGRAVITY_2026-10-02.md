# HANDOVER to Antigravity - YouTube Pipeline (14 faceless channels) - written Fri 2 Oct 2026, ~22:00 NL

Owner: Riks. Everything below was read from the project's own handover files on Google Drive
(`G:\My Drive\_RXClaude\Youtube Pipeline\...`), not from memory. Where something is a proposal, it says PROPOSED.
Where I could not verify something, it says UNVERIFIED. Nothing here is a secret; no keys or passwords are included.

---------------------------------------------------------------------------------------------------------
## 0. PASTE THIS AS THE FIRST MESSAGE IN EACH ANTIGRAVITY CHAT

> You are continuing Riks' YouTube Pipeline project from Claude Code. Read `HANDOVER_ANTIGRAVITY_2026-10-02.md`
> (sections 1-3 plus your chat's section), then read the files it names under
> `G:\My Drive\_RXClaude\Youtube Pipeline\`. Check live state first (`py -3.12 _rx_whatsrunning.py`,
> `py -3.12 _rx_render_queue.py status`, `py -3.12 _rx_gates.py --show`) - never trust numbers in a handover.
> Reply in plain English: short summary, then your first action, then ONE check question. Stop at every gate that
> needs Riks. Do not upload anything, change anything on Subscribr, or spend money outside the rules in section 3.

Chat to open -> section to read:
- **RSCH / orchestrator chat** -> section 4
- **Channel 1 chat** -> section 5
- **Channel 2 chat** -> section 6
Everyone also reads section 7 (3-voice previews), section 8 (new lanes / Claude downgrade) and section 9 (porting limits).

---------------------------------------------------------------------------------------------------------
## 1. The project in 10 lines
- 14 faceless YouTube channels (ch01-ch14), built with AI video. Each episode = copy ONE proven outlier video's structure in our own words, own look.
- Gate ladder (every gate = a mail to Riks, he approves by mail reply OR chat; there is NO autonomy):
  1A outlier + 2-min previews in 3 mimic styles -> 1B full script + our fact-check + Gem 1 -> 2A 3 voice samples -> 2B ONE full narration take
  -> 2C shotlist (Gem 2) -> 2D/2E/2F cuts, 2 music beds, 2 volumes -> 3A 5-min sample = his definite style choice -> 3B full package -> he says "approve" -> upload.
- Video is rendered on SnapGen free Veo lanes (4 accounts x 5 lanes: riks, rix1, rix2, croki; ~400 free clips/account/UTC day, reset 02:00 NL; only the Studio "FREE" banner counts).
- Voice = AI33 (TTS + Voice Changer). Thumbnails = AI33 Nano Banana Pro. Research = Nexlev. Scripts/pools = Subscribr. Titles = vidIQ (out of credits right now).
- Fact-check: our own check first (WRONG only with 5+ sources), then Gem 1 (Gemini Gem), then Gem 2 builds the shotlist JSON.
- Presenters and talking characters now WORK on free Veo (Dex test 29 Sep; ch09 test 2 Oct: Veo said every word in 4/4 clips, Omni dropped 5 words).
- New intro on every ch01/ch02 episode (and every sample): cold-open hook, "Welcome to <channel>" + logo scene by 0:25-0:34, 1.0 s black pre-roll, picture fade-in 0.8 s, audio fade-in 0.3 s, chapters/captions +1.0 s.
- Slots: ch02 ships Tue/Thu/Sat 15:00 NL.
- Metrics page for all outliers: https://claude.ai/artifact/D23xpHzFwV7nqNY91AhpGg

---------------------------------------------------------------------------------------------------------
## 2. How Riks wants you to talk (read first, applies to all three chats)
- Plain talk. No session ids, no jargon. Summary, up to 3 vertical options, ONE recommendation with the argument, one short check question.
- English by default; Dutch is fine if he writes Dutch.
- Every gate mail: right after sending, start `py -3.12 _rx_wait_for_decision.py --channel chNN --episode epNN [--gate G..]` in the background so you notice the moment his reply lands. He was upset twice when sessions only noticed when he said so.
- A chat answer closes the gate mail (no reminders). Record it: `py -3.12 _rx_gates.py --clean --note "Riks in chat"`.
- Mispronounced names are acceptable if the CAPTIONS spell them right (Riks, 2 Oct). Do not re-voice unless he asks.
- Pass everything you learn to the other chats AND to `_FINDINGS_LIVE.md`.

---------------------------------------------------------------------------------------------------------
## 3. Hard rules that are AGREED (break none)
1. Upload only when Riks says so for that specific episode. Upload holds stay until he has SEEN the new intro.
2. Video renders on the free Veo lanes ONLY. Never SnapGen API / Omni credits for video (AGENTS.md, 2 Oct). If Veo refuses a clip: reword and retry on Veo (max 3 tries per clip).
3. Credits for everything else (AI33 TTS/voice changer, images) are free to spend to finish an episode. Do not ask or mail about a spend; mail only when a balance is too low. AI33 on 2 Oct: riks ~654k, croki ~162k. Log spends in `_AI33_COST_<ep>.md`. Price AI33 before running.
4. Every Subscribr write needs Riks' explicit yes (pool changes, save_template, voice profile commit, Thumbnail Board).
5. Veo prompts: no on-screen text/letters/numbers, never name a brand/broadcaster/channel/YouTuber, no narration text inside the prompt, avoid medical/gore/weapon filter words, no minors, no speaking officials at lecterns (show an empty lectern).
6. Never touch another channel's files, the shared tools (`_rx_*.py`, `_build_ch02_gen.py`), or other jobs in `_sessions\render_queue.json`. Never start/stop `_rx_veo_pool.py` unless the 15-minute guard in the ch01/ch02 kickoff STEP 0 says it is safe. Never taskkill the pool or Chrome.
7. Every shell command touching `G:` starts with `timeout N bash -c '...'` (N <= 590). Exit 124 = Drive hung: report, never loop. No recursive scans of `_FLOW` or channel roots.
8. LOOK at every generated image/clip yourself. No vidIQ MCP (credits). Always `py -3.12` (not plain `python`; only 3.12 has faster-whisper).
9. Outlier-adaptation rule: on established ch01/ch02 mimic topic, hook and pacing but keep our visual DNA. A presenter/dialogue format there may only be an explicitly branded sub-series, never silently inside the main run.
10. Dialogue pacing rule (Riks, 2 Oct): never cut on the last syllable. Hold the shot ~1 s after the last word, then ~0.7 s of ambience before the narrator resumes. Use `assemble_paced.py`, not `assemble.py`.

---------------------------------------------------------------------------------------------------------
## 4. CHAT 1 - RSCH / ORCHESTRATOR (session 862fc475-30f3-483f-aa62-649bd2b2c4f1, "RESEARCH v4 / gate-run chat")

**Read:** `_KICKOFF_GATES_CH03_CH13_2026-10-02.md` (it has the live STATUS table), `_research_v3_2026-09-29\PHASE_B_CHANNEL_PROMPTS.md`,
`_FLOW\_DIALOGUE_IN_PREVIEWS_HOWTO.md`, `_FLOW\GATE1A_SAMPLES_RECIPE.md`.

**Job:** run every gate up to 3A, one channel at a time, in this order: **ch03 -> ch04 -> ch05 -> ch06 -> ch07 -> ch09 -> ch10 -> ch11 -> ch12 -> ch13.**
Finish a channel through 3A before starting the next. ch08 and ch14 run in their own chats. After a channel's 3A is decided, Riks opens a DEDICATED chat for it
(paste prompts are in PHASE_B_CHANNEL_PROMPTS.md): full Subscribr setup -> first full episode = the 1A outlier -> 3B -> ship.

**Where it stands (2 Oct evening):**
| Ch | Outlier (1A) | State | Next |
|---|---|---|---|
| ch03 Bible mysteries | Chronicles of Enoch `0zZgD9g5PQ8` | Previews done in 3 styles (S1 Bible Stories-Movies, S2 Unraveling, S3 Enoch Unsealed). 1A mail RE-SENT ~20:35 with 3 spoken lines in every 2-min preview (Semyaza, a Watcher, Enoch; whisper-checked; mail 01a0fde1). Recommendation: keep styles 1+2. | Wait for Riks' 1A reply -> 1B script (narrator + Enoch/angel/Noah lines) |
| ch04 Elite Chronicles | Untouchable Sisters `aXT3v4WIlBU` | Previews done (FINAiUS / Old Line Power / Mythic Women) | Send 1A mail when ch03 reaches 3A |
| **ch05 Digital Dread** | AI Takeover `Gw_hnD7m00M` | S1 + S3 done. **S2 = the on-camera PRESENTER preview must be redone on free Veo** (overnight run had refusals) | Redo S2, then send 1A mail |
| ch06 AI Agent | Agent Harness `1a1VXDdIyrk` | Previews done | - |
| ch07 AI Anatomy | Every Deadly Disease `LQ_6OG7-xmA` | Previews done | - |
| **ch09 Ancient Archives** | 4000 Years of Chinese History `wuhnBi8jNl0` | S1 + S2 done. **S3 = the PRESENTER preview must be redone on free Veo** (the 2 Oct ch09 test proves Veo does it) | Redo S3, then send 1A mail |
| ch10 | Most Guarded Places `yMwWSX_cvrc` | Previews done | - |
| ch11 | Old Money Mindset `avWK82b0fUU` | Previews done. ch11 ep06 is a SEPARATE running episode - do not touch | - |
| ch12 | Renting vs Buying `nkT_K8l1rEw` | Previews done | - |
| ch13 | Doritos `3v5rU97gyoc` | Previews done | - |

**Important - conflicting notes:** a 16:50 note says "Veo refuses realistic presenters (ch05 S2, ch09 S3) -> paid Omni only". The later 2 Oct note (and the ch09 test in
`_FLOW\CH09PRES_TEST\`) overrides it: presenters work on free Veo, and the hard rule is video on free Veo only. Follow the later note.

**Rule that carries forward:** dialogue in a 1A preview carries into the 3A 5-minute sample. Recipe for ch04-ch13: `_FLOW\_DIALOGUE_IN_PREVIEWS_HOWTO.md`
(3 spoken beats per 2-min preview, lines <= 2 words/s of the clip span, whisper-check every clip, trim head silence, assemble with the paced script).
Riks deleted the first round of 1A mails on 2 Oct; each channel's 1A mail is sent again when its turn comes (update its `REC.json` first: presenters/dialogue are now allowed in every style).

**Also on this chat's plate**
- Voice previews for ch03 (and then each channel in order) per section 7.
- `competitor-scout-monthly` keeps Subscribr pools fresh for FINISHED channels (first real run 1 Nov 2026). When a channel's first episode is scheduled, its dedicated chat moves it from `not_finished` to `channels` in `_COMPETITOR_SCOUT.json`. ch01 + ch02 are in; ch03 is next.
- ch08 and ch14 still need their full Subscribr setup in their own chats. ch14 ep05 (`MA1tQ64dJho`, Sat 3 Oct 01:00 NL) and ep06 (`CoYIMcQgXS4`, Sun 4 Oct 01:00 NL) are scheduled.

---------------------------------------------------------------------------------------------------------
## 5. CHAT 2 - CHANNEL 1 "Ancient Earth Cinema" (extinct-animal / BBC-photoreal look; mimic target ExtinctZoo)

**Read (newest first):** `_sessions\2026-10-02_ch01_ep20_ep18_shipped_ep21_gem2.md`, `_sessions\HANDOVER_CH01_session1_2026-10-02.md` (session 013bcd8f; older, parts superseded),
`_KICKOFF_ch01_2026-10-01.md`, `01 Ancient Earth Cinema\_CHANNEL_TEMPLATE.md`, `01 Ancient Earth Cinema\_SHIPPED_ep20_ep18_2026-10-02.md`.

**State (as of 2 Oct ~21:50):**
- ep19 shipped `bqIsC9iq2mU` (public Fri 2 Oct 01:00 NL): check its A/B/C test is running.
- **ep20 Kem Kem shipped** `brAoLR1TKh4` (publishes Sun 4 Oct 01:00 NL). **ep18 Laschamp shipped** `VbS426XYDSM` (publishes Mon 5 Oct 01:00 NL). Both 3B pick = option 1. After they go public: A/B/C tests Ineligible -> running; check thumbnail order.
- **ep21 Messel Pit** ("What really killed the animals of Messel?" mystery, v2): own fact-check v2 (125 claims, 0 wrong), Gem 1 reconciled (Gem was wrong on bats: 6.3-9.5 bats per YEAR, Smith et al. 2024), full narration take 21:37 (~25,000 AI33 credits), Gem 2 JSON validated PASS (195 clips, 170/170 cuts on word starts), plan `_FLOW\CH01EP21_gem\plan.json`.
  **Open: the gate 3A 2-minute preview was being built by a sub-agent. Next: Riks APPROVE -> full plan into render queue (free lanes) -> master -> pack -> 3B.**
- Open housekeeping: ep11 `qNGJPhknnuU` and ep12 `UUVIT171l-8` have been PRIVATE with no schedule since 30 Sep (seen on the API). Ask Riks what to do.
- Presenter/dialogue check (2 Oct, research only): **ch01 = KEEP LOCKED.** Nexlev found no on-camera-presenter or character-dialogue channel in the niche within 180 days; faceless AI dominates. UNVERIFIED caveat: Nexlev may under-index presenter channels. If Riks wants certainty, do a manual YouTube search. A topic lead worth a later decision (not a change): the "extinct animals frozen / still alive" listicle angle is trending (Bestias Miticas, Fossil Fruw) - usable as a TOPIC inside our BBC look.
- Style stays locked: BBC/photoreal look, existing voice, cut rate, bed level (see `_CHANNEL_TEMPLATE.md`).

**Voice task for this chat:** 3 voice previews at the pace of the mimic channel - section 7.

---------------------------------------------------------------------------------------------------------
## 6. CHAT 3 - CHANNEL 2 "Chronicle Zero News and Documentaries" (declassified military look; mimic target The Battlefield Show)

**Read:** `_KICKOFF_ch02_ep19_2026-10-02.md` (paste: `/rx-pickup YouTube Pipeline - read _KICKOFF_ch02_ep19_2026-10-02.md and do it`, i.e. in Antigravity: "read that file and do it"),
`02 Chronicle Zero...\_CHANNEL_TEMPLATE.md`, `_FLOW\CH02EP19_BIBLE.md`, `ep19_Pokhran_II\ch02_ep19_shotlist_gem_check.md`. The old session 00143a4f is full: start fresh from the kickoff.

**State:**
- **ep18 BRP Sierra Madre: SCHEDULED**, video `O4BkCJxJ_mc`, private, publishAt Sat 3 Oct 15:00 NL (= 2026-10-03T13:00:00Z). Title 1, new-intro master, AI disclosure Yes, English subtitles inserted via API. **TODO Sat 3 Oct after 15:05 NL:** API shows public; A/B test now RUNNING in Studio; captions still serving; AI flag Yes in Studio. Confirm the Studio tab is on "Chronicle Zero Documentaries" (a tab once sat on the wrong channel; vidIQ overlay hangs the Chrome extension).
- **ep19 Pokhran-II**, target **Tue 6 Oct 15:00 NL**. Done: 1A (outlier `h13tLj5mGH0`), script (1,938 words, FINAL), fact-check (none wrong), Gem 1 reconciled (20 correct / 16 formatting-only / 0 wrong; 8 Gem-inserted sentences rejected), narration take approved (809.5 s, 15,334 AI33 credits, welcome line at 31.23 s), Gem 2 JSON parsed (119 clips, 114/114 cuts on word starts) with ONE error: clip 1 starts 0.00 but first word is 0.11 -> snap.
- **Next steps in order:** (1) snap clip 1 to 0.11, re-check, `py -3.12 _rx_gem_reply.py plan --channel ch02 --episode ep19`; fix prompts for clips 13, 26, 27, 31 (text/letter risk), 18, 48 (newspaper), 49 ("planet Earth" -> "the curved horizon of the Earth from orbit"). (2) First frames per chain (`_rx_first_frame_snapgen.py`), brand/logo clip n=900. (3) Render via `_rx_render_queue.py add --job ch02-ep19 --plan <plan.json>` (~25-40 min for 119 clips). (4) 3A 5-min sample with the new intro -> mail -> wait tool. (5) Master (pattern `_FLOW\_session_scripts_2026-10-02\full_newintro18.py`; video = narration + 1.0 s; -14 LUFS; contact sheet every 8 s). (6) 3B package in `ChronicleZero_ep19_final\` (working title: "America Thought Its Spy Satellites Saw Everything... Then India Did THIS" - NOT "Billion-Dollar", no source; vidIQ unscored, say so). (7) Ship only after his APPROVE n.
- Presenter/dialogue check: **ch02 = KEEP LOCKED** (nothing beat Battlefield Show; no presenter outlier found; same UNVERIFIED caveat as ch01). Presenter/dialogue only ever as a branded sub-series.
- Pronunciation: AI33 dictionary 421 (GET first, append, PUT the FULL rules list) + `_pronounce.json`. Ep19 additions: Pokhran, Vajpayee, Atal, Bihari, Rajasthan, Thar, Chagai, Balochistan, Kalam, Trishul, Nawaz, Sharif.

**Voice task for this chat:** ep19's voice is already approved, so the 3-voice preview applies to the channel TEMPLATE / future episodes (ep20+). Do not re-voice ep19.
For reference ep19's pace = 1,938 words / 809.5 s = **~143.6 words per minute** (my calculation).

---------------------------------------------------------------------------------------------------------
## 7. THE 3-VOICE PREVIEW (gate 2A) - for ch03 (in progress), ch01 and ch02 (new request)

What Riks asked on 2 Oct: hear a preview of THREE voices, for ch03 and also for ch01 and ch02, **at the speaking pace of the mimic channel**.
Existing rule: memory `match-competitor-voice-wpm`; gate 2A = "3 voice samples; show competitor WPM vs ours".

How to do it (same recipe for all three channels):
1. Measure the mimic channel's words-per-minute from a real transcript of its outlier (Nexlev `get_video_transcript` or Subscribr transcript; words / audio minutes). Mimic targets: ch01 = ExtinctZoo, ch02 = The Battlefield Show, ch03 = the style channel Riks keeps at 1A (Bible Stories - Movies / Unraveling the Scriptures / Enoch Unsealed).
   ExtinctZoo and Battlefield Show WPM are NOT recorded in any file I read - UNVERIFIED, measure them; do not guess.
2. Take ONE 60-90 s passage of the channel's own current script (same text for all three voices, same words).
3. Render 3 different voices on AI33, each speed-tuned so the delivered WPM matches the mimic's WPM (report the mimic's WPM, ours before tuning, and ours after).
4. Whisper-check names and numbers; send as ONE gate-2A mail with the three audio files attached and your recommendation.
5. Riks picks one -> that voice becomes the channel voice -> carries into 2B (the ONE full narration take) and the 3A sample.
For channels with speaking characters: the narrator voice is separate; characters get one consistent voice each via AI33 Voice Changer.
Known voices in use: ch11 = ElevenLabs premade Brian (narration + presenter). Placeholders in 1A samples: ch06 `elevenlabs_nPczCjzI2devNBz1zQrb`, ch05 `elevenlabs_VMCgCMbBs53ElBxVD4VB`.

---------------------------------------------------------------------------------------------------------
## 8. NEW: cheaper lanes + the Claude downgrade (NOT YET AGREED - these are PROPOSALS for Riks to confirm)

### 8a. Google Flow credits from Google AI Ultra
- Riks' new fact (2 Oct): Google AI Ultra includes Google Flow with **25,000 credits per month**. I could not verify this figure or what one Veo clip costs in Flow credits; treat as UNVERIFIED until a test clip is priced.
- Flow is not new to the project: it was "Line B" (Google Flow / TurboFlow, Veo 3.1 Lite Lower Priority at 0 credits, 8 s, 16:9). ch02 ep17 clips 1-33 were made in Flow Omni Flash until credits ran out; ch01 ep20 part B was packed for Flow (`_FLOW\CH01EP20B_TF\`) and the Flow collector is `_rx_turboflow_collect.py`. The memory said Flow had no credits and "Riks buys a new account later" - Ultra solves that.
- Why it matters NOW: the free SnapGen Veo Max plans for riks/rix1/rix2 **expire Sat 10 Oct** (croki's Veo expired 20 Sep; Image Max until 13/14 Oct). Renewal mail is planned for 9 Oct. Riks adds +1 Veo Max account per week. A Flow lane on Ultra is the continuity/backup lane if SnapGen is not renewed, or an extra lane on top.
- PROPOSED plan: (1) price ONE Flow clip in credits and compute episodes/month (e.g. 119 clips for ch02 ep19, 195 for ch01 ep21); (2) run one test clip with a presenter line; (3) only then decide the split. **Rule 2 in section 3 is written about SnapGen API/Omni credits - using Flow credits for video is a change that Riks must approve explicitly. Do not start it on your own.**
- Rule from the ledger still applies: a clip is rendered on ONE line only. Before moving a job to Flow, `_rx_render_queue.py leave` it from the pool; before giving Flow clips back, check what the collector already has.

### 8b. Claude Max (EUR 100) -> possibly Claude Pro ($20)
- Riks may stop the EUR 100 Claude subscription and maybe continue on Claude Pro ($20). Antigravity + Google AI Ultra becomes the main workhorse.
- PROPOSED split: Antigravity (Gemini, Ultra) = orchestration, render queue, mail gates, whisper checks, assembly, uploads-prep. Claude Pro = judgement-only (fact-check reconciliation when sources conflict, script rewrites, anything where a wrong claim is expensive). Claude Pro's usage limits are far smaller than Max: I did not look up the exact limits - UNVERIFIED; check before relying on it. Existing house rule already says "workers on Sonnet, judgement on Opus"; on Pro, Opus use will burn the allowance quickly, so default to Sonnet.
- Do not downgrade before the section 9 checklist is done, or the project loses its skills, memory and scheduled tasks.

---------------------------------------------------------------------------------------------------------
## 9. PORTING REALITY CHECK - what does NOT come over automatically
Everything the pipeline runs lives in Python scripts and files on Riks' laptop (`G:\My Drive\_RXClaude\Youtube Pipeline\`, `py -3.12`). Antigravity must be run ON that laptop with `G:` mounted, or none of it works.
These live inside Claude, not in the files, and must be exported or replaced:
1. **Claude skills**: `yt-pipeline-rules`, `rx-pickup`, `rx-ship`, `rx-sync`, `rx-handover`, `rx-generate`, `subscribr-api`, `youtube-production`. Antigravity will not load them. Export their text to plain markdown rules (AGENTS.md is the closest equivalent - it already holds the hard rules; check it is complete).
2. **Claude memory entries** (e.g. `one-outlier-three-mimic-styles`, `match-competitor-voice-wpm`, `new-intro-all-ch01-ch02-episodes`, `ch02-engine-runbook`, `competitor-scout-monthly-routine`, `veo-max-account-added-weekly`, `full-gate-ladder-all-channels-no-autonomy`). Location on disk UNVERIFIED. Export to one markdown file in the project root.
3. **Claude scheduled tasks**: `competitor-scout-monthly` (cron `0 9 1-3 * *`, first real run 1 Nov; dry-run switch = file `_competitor_scout\DRYRUN`), `rx-engine` (ch02 template engine), `rx-gate-runner` (processes gate replies). If Claude is downgraded or cancelled these stop. Find out which are plain scripts (re-schedule with Windows Task Scheduler) and which need an LLM. UNVERIFIED which is which.
4. **MCP connections**: Subscribr, Nexlev, vidIQ, Gmail, Google Drive, Airtable are connected to Claude. Antigravity needs its own connections or the equivalent via the Subscribr REST API / Nexlev API / YouTube API scripts. Gate mail is sent by the project's own scripts (Resend sender `onboarding@resend.dev`, may land in Spam) - those keep working.
5. **Chrome extension** used for YouTube Studio passes (language, AI-disclosure flag, A/B/C test, playlist, schedule). Antigravity's browser control is a different tool; the Studio pass is the fragile step - test it on a throwaway private video first.
6. **Session transcripts** (`...\.claude\projects\G--My-Drive--RXClaude\*.jsonl`) stay greppable for detail; `claude --resume <id>` only works while Claude Code is installed.
7. **Models**: Antigravity's models will behave differently. Rules that were learned the hard way: "NEVER stop an ordered render on your own reading of a new idea", Gem answers can arrive as PDF and may INSERT sentences (never accept unsourced ones), Whisper word-start times are +-0.7 s unreliable (use the speech-band envelope for cuts).
Offer: I can do the export of items 1-2 into plain markdown files on Drive if you want - say so.

---------------------------------------------------------------------------------------------------------
## 10. OPEN DECISIONS FOR RIKS (the first thing each chat should ask, one at a time)
1. Orchestrator: your 1A reply for ch03 (keep styles 1+2?). Then confirm: redo ch05 S2 and ch09 S3 presenter previews now on free Veo?
2. ch01: ep21 3A preview ready -> approve? And what to do with ep11/ep12 (private, unscheduled)?
3. ch02: any corrections to the ep19 plan before the 119-clip render? ep18 Saturday check after 15:05.
4. Voices: confirm the 3-voice preview recipe (section 7) for ch03/ch01/ch02, and whether ch01/ch02 changes apply only to future episodes.
5. Flow on Ultra: approve a one-clip price test? Allowed to use Flow credits for video at all (changes rule 2)?
6. Claude: when exactly do you downgrade? Do the section 9 export first?
7. Veo Max renewal for riks/rix1/rix2 before 10 Oct (mail planned 9 Oct) - renew, or move video to Flow?

---------------------------------------------------------------------------------------------------------
## 11. Key paths and ids (all under `G:\My Drive\_RXClaude\Youtube Pipeline\` unless stated)
- Live state: `_sessions\ACTIVE_WORK.md`, `_sessions\LAST_HANDOVER.md`, `_FINDINGS_LIVE.md`, `_KICKOFF_INDEX_2026-10-01.md`, `AGENTS.md`
- Gate ledger: `py -3.12 _rx_gates.py --show`; mail tools `_rx_gate_mail.py`, `_rx_gate1a_mail.py`; wait tool `_rx_wait_for_decision.py`
- Render: `_rx_render_queue.py`, `_rx_veo_pool.py` (log `_sessions\VEO_POOL.log`), `_rx_veo_budget.py` (overstates free clips: trust the pool's `billing_stop`), `_rx_balances.py`
- Session scripts of 2 Oct: `_FLOW\_session_scripts_2026-10-02\`
- Research: `_research_v3_2026-09-29\` (scorecards, `outlier_metrics_chNN.json`, `PHASE_B_CHANNEL_PROMPTS.md`, `verdict_chNN.md`)
- Per-channel kickoffs: `_KICKOFF_chNN_CONTINUE.md`; 1A previews: `<channel folder>\_gate1A_2026-10-01\`
- Subscribr pools: ch01 60043 (Ancient Earth Cinema), ch02 59974 (Chronicle Zero Documentaries), ch03 60019, ch04 60005, ch05 60040, ch06 60042, ch07 60039, ch09 60024, ch10 60017, ch11 59977, ch12 59980, ch13 59979
- Claude sessions (for grepping transcripts only): orchestrator 862fc475-30f3-483f-aa62-649bd2b2c4f1; ch02 00143a4f-3a66-4c20-abd5-01bc19bc138f; ch01 session 1 013bcd8f-05f5-45c5-8835-97fb37adfa34 (a second ch01 session wrote the evening note; its id is UNVERIFIED)
- SnapGen accounts: croki, riks, rix1, rix2 (re-auth: login at snapgen.ai, F12 console `copy(localStorage.getItem('authStore'))`, then `py -3.12 _sg_reauth.py --profile <acct> --file <json>`)

## 12. What I could NOT see (so you know the limits of this handover)
- I did not read the three live chats themselves, only the handover files they wrote to Drive. Anything said in those chats after ~21:50 on 2 Oct is not here.
- Section 7's "ch03 voice preview" status and the exact wording Riks used in the RSCH chat for the 3-voice request come from his message to me, not from a file.
- Files modified after ~21:50 on 2 Oct, the ledger, the queue and the YouTube API were not queried.
