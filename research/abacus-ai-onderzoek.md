# Abacus.AI — diepgaand onderzoek

**Datum onderzoek:** 20 september 2026
**Scope:** bedrijf, productportfolio, Agent Swarms, modellen, pricing, API, beperkingen, en bruikbaarheid voor eigen projecten.

> **Bronwaarschuwing vooraf.** De domeinen `abacus.ai`, `chatllm.abacus.ai` en `deepagent.abacus.ai`
> zijn in deze omgeving geblokkeerd door de egress-policy (403 van de proxy). Alle onderstaande
> informatie komt daarom uit zoekresultaten en secundaire bronnen (reviews, prijsvergelijkers,
> Trustpilot, docs-samenvattingen), niet uit een directe lezing van Abacus' eigen pagina's.
> Prijzen en modellijsten bij Abacus veranderen zeer snel — **verifieer alles op de prijspagina
> zelf voordat je betaalt.** Waar bronnen elkaar tegenspreken staat dat expliciet vermeld.

---

## 1. Het bedrijf in het kort

| | |
|---|---|
| Naam | Abacus.AI (oorspronkelijk RealityEngines.AI) |
| Opgericht | 2019, San Francisco |
| CEO / oprichter | Bindu Reddy |
| Funding | ca. $85–90 mln over 3 rondes |
| Investeerders | Index Ventures (Mike Volpi), Eric Schmidt, Ram Shriram, Coatue, Khosla Ventures, Tiger Global |
| Geschatte waardering | ~$400 mln (niet officieel bevestigd) |
| Omzet | ~$30 mln ARR (Getlatka-schatting) |
| Medewerkers | ~185 (2026), was 123 in 2023 |

Abacus begon als klassiek enterprise-ML-platform (AutoML, feature store, forecasting) en is
daarna volledig gedraaid naar "AI super assistant" voor consumenten/professionals. Die twee
levens bestaan nog steeds naast elkaar — dat verklaart waarom het productaanbod zo breed en
soms verwarrend is.

---

## 2. Productportfolio — wat zit er allemaal in

Abacus is geen één product maar een stapel. Belangrijk: **bijna alles hieronder zit in één
abonnement van $10–$20 per maand.** Dat is de kern van hun propositie.

### 2.1 ChatLLM (Teams) — de multi-model chat
De voordeur. Eén interface met alle grote modellen, plus:
- chat, voice, documentanalyse, websearch
- eigen custom chatbots en AI-agents bouwen ("AI Engineer")
- documenten uploaden, RAG over je eigen data
- integraties: Slack, Teams, Confluence, Google Drive, OneDrive, SharePoint, Gmail, Google Calendar, GitHub
- **MCP-ondersteuning** (Model Context Protocol) — relevant, want dan kun je je eigen MCP-servers eraan hangen
- team-workspace: gedeelde chats, docs, prompts

### 2.2 Abacus AI Agent (voorheen DeepAgent) — de autonome agent
De ster van het aanbod. Een general-purpose agent die:
- full-stack web- en mobiele apps bouwt **en deployt**
- echte software-engineering op bestaande codebases doet
- presentaties (PPTX, Google Slides), onderzoeksrapporten (PDF), Excel-analyses maakt
- **computer use**: bestuurt een echte browser/desktop — klikken, typen, formulieren invullen, sites scrapen waar geen API is
- koppelt aan Gmail, Slack, GitHub, Jira, databases en honderden MCP-integraties
- draait op schema's en triggers (scheduled/recurring tasks)

### 2.3 Agent Swarms — het multi-agent systeem
Uitgebreid gelanceerd in de **april 2026 platform-update**. Zie hoofdstuk 3, dit is waar je
specifiek naar vroeg.

### 2.4 Abacus AI Desktop / CodeLLM — de coding-omgeving
- desktop-app met **CLI, code-editor, "Listener" en "CoWork" modes**
- VS Code-extensie, GitHub-synchronisatie, autocomplete, debugging, scaffolding
- Abacus claimt dat hun CLI Claude Code en Codex verslaat op benchmarks — *dat is een
  vendor-claim, niet onafhankelijk geverifieerd*
- techniek erachter: ze combineren modellen (bv. coding-prompts naar het sterkste code-model,
  computer-use-taken naar een ander model) in plaats van één model voor alles

### 2.5 Abacus Claw — always-on persoonlijke agent
- gehoste versie van **OpenClaw** (open-source agent-framework)
- draait 24/7, met **persistent geheugen over sessies en kanalen heen**
- aanwezig op WhatsApp, Telegram en Slack tegelijk
- eigen cloud-computer: terminal, browser, persistente bestandsopslag
- achtergrond-automatisering via herhalende taken
- eigen persoonlijkheid/toon instelbaar

### 2.6 Abacus SuperComputer — always-on cloud-VM
- permanente Linux-VM in de cloud, inbegrepen bij het abonnement
- database, persistente storage, terminal, **inbound HTTPS**, GitHub- en SSH-toegang
- 100+ AI-modellen lokaal beschikbaar voor je apps
- je beschrijft in gewone taal wat je wil; een agent bouwt, deployt en houdt het draaiend op een publieke URL
- gebruikt voor: self-hosted LLM-chatinterfaces, games, social platforms met live database, 24/7 streaming apps, API's, workflows

### 2.7 Abacus Studio — media-generatie
- **beeld:** GPT Image 1.5/2, Nano Banana 2 en Pro, Seedream 4.5, Midjourney, Grok Imagine, FLUX.2 [Pro], Hunyuan Image 3.0, Wan 2.7, Imagen 4, Recraft SVG, Ideogram 3.0, Magnific Upscaler, plus edit-varianten (GPT Image Edit, Qwen Image Edit)
- **video:** Sora 2, Veo 3.1 en Veo 3.1 Lite, Kling AI v3 / O3 / v2.6 Motion Control, Seedance 2.0 en 2.5, Seedance 1.5 Pro, Wan 2.5, Hailuo 2, Luma Labs, Grok Imagine Video, Gemini Omni Flash
- **spraak/TTS** eveneens inbegrepen
- dit valt binnen dezelfde credit-pool — **dit is waar credits het hardst verdwijnen**

### 2.8 AppLLM — prompt-to-app builder
- app bouwen vanuit een prompt, met **ingebouwde database zonder setup**
- deployen naar een gratis Abacus-domein óf een eigen custom domain
- DNS via nameservers (aanbevolen voor GoDaddy, Squarespace, Porkbun, Hostinger) of via losse records
- Apps Console met database-export en analytics

### 2.9 RouteLLM API — de developer-API
Zie hoofdstuk 5. Dit is waarschijnlijk het onderschatte deel voor jouw situatie.

### 2.10 Enterprise ML-platform (het "oude" Abacus)
Nog steeds actief, los van het consumentenspoor:
- AutoML: automatische pipeline-bouw en modelselectie
- production-grade **Feature Store** met lage latency
- **Vector Store**: chunken, embedden, opslaan, retrieven van documenten/posts/images voor RAG
- use cases: personalisatie, forecasting, planning, anomaliedetectie, NLP, fraude/security, vision AI
- On-prem variant ("AbacusOS") en data-sovereignty-aanbod voor o.a. banken

---

## 3. Agent Swarms — waar je specifiek naar vroeg

### 3.1 Architectuur: master–worker

**Master Agent** (de coördinator):
1. leest je prompt en bepaalt de volledige scope
2. hakt het project in deeltaken
3. bepaalt de **afhankelijkheden** tussen die deeltaken
4. wijst elke taak toe aan een worker
5. bewaakt voortgang
6. geeft output van de ene worker door als input aan de andere
7. voegt de losse resultaten samen tot één eindresultaat

**Worker Agents** (de specialisten):
- elke worker is **een volwaardige, onafhankelijke Abacus AI Agent** — geen afgeknepen sub-proces
- één worker = één taak: een app bouwen, een presentatie maken, een researchrapport schrijven
- workers draaien **parallel** waar het kan, **sequentieel** waar afhankelijkheden dat afdwingen

Dit is het echte verschil met "één agent die stap voor stap werkt": de swarm verdeelt het
project in onafhankelijke brokken en werkt daar tegelijk aan.

### 3.2 Browser Swarm
De interessantste variant: workers die **allemaal een eigen echte browser besturen**. Je geeft
één doel en tientallen browser-agents gaan tegelijk het web op — sites doorklikken, formulieren
invullen, gestructureerde data verzamelen, terugrapporteren.

Gedemonstreerd voorbeeld: meerdere providers vinden, hun sales-contactpaden lokaliseren,
formulieren indienen en een schoon rapport teruggeven — inclusief de notitie dat één provider
door bot-detectie werd geblokkeerd terwijl de rest doorkwam. Dat laatste detail is een goed
teken: de swarm rapporteert eerlijk over gefaalde workers.

### 3.3 Wanneer het werkt (en wanneer niet)
**Bedoeld voor** projecten die te groot zijn voor één agent om samenhang te bewaren:
- een platform met meerdere gekoppelde componenten (web-app + mobiele app + dashboard)
- research die meerdere onafhankelijke domeinen synthetiseert
- gestructureerde rapportage over veel bronnen
- parallelle code-taken

**Gemeten resultaat:** een 3-app-project ging van ~4 uur naar ~90 minuten. De parallellisatie is
echt, niet cosmetisch.

**Niet bedoeld voor** simpele taken — daar wegen de extra credits niet op tegen de winst.

### 3.4 Effort Levels — de kostenknop
Ook uit de april 2026-update. Je kunt per taak de kwaliteit/kosten-afweging instellen:

| Level | Wat het doet |
|---|---|
| **xLow** | snelle, goedkope open-source modellen (o.a. GLM 5.2, Kimi 2.7 Code) |
| Low / Medium | tussenliggende routering |
| High / xHigh | routeert naar capabelere, duurdere modellen |
| **Max** | zwaarste modus — coding-prompts naar Fable 5.1, computer-use naar GPT 6 Astra |

**Max verbruikt verreweg de meeste credits.** Bewaar het voor taken waar kwaliteit echt telt.

### 3.5 Credits en swarms
- een swarm draait meerdere agents parallel en kost dus **substantieel meer** dan één agent-chat
- officiële richtlijn: een *typische* agent-taak kost **~500–1.000 credits**
- complexiteit, modelkeuze, effort level, mediageneratie en aantal revisies veranderen dat sterk
- reken dus ruwweg: een swarm van 5 workers op medium effort = al snel enkele duizenden credits
- met 30.000 credits op Pro kom je daarmee in de orde van **enkele tientallen serieuze
  swarm-runs per maand** — niet honderden

### 3.6 Praktijkbeperkingen (eerlijk)
Onafhankelijke gebruikersfeedback is verdeeld:
- **positief:** bruikbare researchsamenvattingen, werkende prototypes, echte tijdwinst
- **negatief:** herhalende loops, onvolledige resultaten, contextverlies halverwege een run,
  en — de pijnlijkste — **credits die opgaan tijdens mislukte runs**
- resultaat hangt sterk af van promptkwaliteit, taakcomplexiteit en "de dagvorm van de agent"

---

## 4. Modellen

Abacus claimt **100+ tot 160+ modellen**, bijgewerkt **24–48 uur na release** van een nieuw model.

### 4.1 Tekstmodellen (stand ~medio/eind 2026)
GPT-6 Astra · GPT-5.6 Sol · Claude Opus 5 · Claude Sonnet 5 · Claude Fable 5.1 ·
Gemini 3.1 Pro · Gemini 3.8 Flash · Grok 4.6 · Qwen 3.8 Max · DeepSeek v4.1 · Kimi K3 ·
GLM 5.3 — plus ca. 20 andere closed- en open-source modellen in de hoofdselectie.

> **Let op:** oudere reviews (begin 2026) noemen GPT-5.5, Opus 4.8, Grok 4.3, DeepSeek v4.
> De roster rouleert continu. Ga uit van "alles wat nieuw is, is er binnen twee dagen",
> niet van een vaste lijst.

### 4.2 Wat je hiermee koopt
Het echte argument is **consolidatie**: in plaats van ChatGPT Plus ($20) + Claude ($20) +
Gemini ($20) + een beeldgenerator + een videogenerator, betaal je $10–$20 totaal. Bij
correct gebruik is dat een factor 5–8 goedkoper.

Het echte tegenargument: je krijgt die modellen **via Abacus' eigen wrapper**, niet via de
officiële apps. Geen Projects van ChatGPT, geen Claude Code-integratie zoals je die nu hebt,
geen garantie dat elke model-feature (bv. extended thinking, specifieke tool-modi) doorgegeven
wordt. En je zit vast aan hun credit-meter.

---

## 5. Pricing — het belangrijkste hoofdstuk

### 5.1 Zelfbedieningsabonnementen

| | **Basic** | **Pro** |
|---|---|---|
| Prijs | **$10 / gebruiker / maand** | **$20 / gebruiker / maand** |
| Eerste maand | **$7** (alleen nieuwe klanten, alleen eerste abonnement) | geen korting |
| Credits | **20.000 / maand** | **30.000 / maand** |
| AI Agent | **slechts 3 agent-conversaties per maand** | **onbeperkt** (zolang er credits zijn) |
| Studio (media) | beperkt, max **2.500 credits per conversatie** | onbeperkt zolang credits |
| Coding Agent / CLI | beperkt | inbegrepen |
| SuperComputer | beperkt | inbegrepen |
| Abacus Claw | beperkt | inbegrepen |
| RouteLLM API | inbegrepen | inbegrepen |
| Gratis tier | **bestaat niet** | bestaat niet |
| Jaarabonnement/korting | **geen gevonden** in de bronnen | idem |

**De belangrijkste regel in deze tabel:** op Basic krijg je **3 agent-conversaties per maand**.
Wil je serieus met Agent of Agent Swarms werken, dan is Basic praktisch nutteloos en is
**Pro ($20) het echte instapniveau**.

### 5.2 Teams
ChatLLM Teams factureert **per gebruiker**: $7 eerste maand, daarna $10/gebruiker/maand,
**geen limiet op teamgrootte**. Let op: gebruikers die je ná de eerste inschrijving uitnodigt
worden **direct tegen het volle $10-tarief** gefactureerd — de $7-korting geldt alleen voor het
initiële abonnement.

### 5.3 Enterprise
- geen lijstprijs; alles op offerte na "gratis expert-consult"
- genoemde startpunten: **$5.000** als instappunt, en een range van **$2.000–$5.000+ per maand**
  afhankelijk van aantal gebruikers, datavolume, private VPC-deployment, SLA's en supportniveau
- **volledige API-toegang voor serieuze bedrijfsintegratie zit op dit niveau** (let op: dit geldt
  voor het enterprise-platform; RouteLLM is wél beschikbaar op het $10-abonnement — zie 5.5)
- contact: `sales@abacus.ai` / `support@abacus.ai`

### 5.4 Het creditsysteem — hier zit het addertje

**Hoe het werkt:**
- elke request trekt credits af op basis van **gekozen model + lengte van input en output**
- credits zijn **geen tokens** en er is **geen gepubliceerde per-model-tarieventabel**
- credit-verbruik is proportioneel aan de werkelijke kosten van de LLM-call
- premium modellen (Opus, GPT-6) verbranden veel sneller dan lichte modellen
- lichte modellen (in oudere docs: GPT-4.1-Mini, Gemini 2.0 Flash) draaien effectief "onbeperkt"
- tekstchat is grotendeels ongemeten; **beeld- en videogeneratie vreten de pool**

**Rollover:**
- **subscription-credits rollen NIET door** — ze verlopen aan het eind van je factuurcyclus
- **bijgekochte credits rollen WEL door** naar de volgende maand
- bijkopen via Profile → Profile & Billing → Buy Credits

**De 75%-throttle — het meest gerapporteerde probleem:**
Meerdere bronnen melden dat je op Basic bij **15.000 van de 20.000 credits (75%)** wordt
teruggezet naar gratis/lichte modellen voor de rest van de maand; de laatste 5.000 credits
worden in reserve gehouden tot de laatste week. En: **ook die "gratis" modellen blijven credits
verbruiken.** Dit staat niet prominent in de marketing.

**Schatting van kosten in credits:**
| Actie | Ruwe schatting |
|---|---|
| Tekstchat lichte modellen | verwaarloosbaar / effectief onbeperkt |
| Tekstchat premium model | laag tot matig, afhankelijk van lengte |
| Typische agent-taak | **500–1.000 credits** |
| Agent Swarm (meerdere workers) | veelvoud daarvan — duizenden |
| Beeldgeneratie | matig |
| Videogeneratie | **hoog — dit is de grootste credit-slurper** |

Met 30.000 Pro-credits: grofweg **30–60 gewone agent-taken**, of **enkele tientallen swarm-runs**,
of aanzienlijk minder als je video genereert.

### 5.5 RouteLLM API — pricing (belangrijk voor developers)
- **Vereist een ChatLLM Teams-abonnement** ($7 eerste maand, daarna $10/maand) — dat abonnement
  dekt zowel de API als de volledige ChatLLM-workspace
- **OpenAI-compatible endpoint**, één API voor 160+ modellen
- automatische routering naar het beste model per prompt, óf expliciet model aanroepen op naam
- **automatische failover** voor closed-source modellen
- **Closed-source modellen: exact provider-tarief.** Abacus stelt expliciet dat ze niet meer
  rekenen dan OpenAI/Anthropic/Google zelf
- **Open-source modellen: "beste prijs ter wereld"** volgens Abacus — dit is hun echte marge-punt
- één gevonden concreet tarief (waarschijnlijk voor een premium-route): **$3,00 per 1M input-tokens
  en $15,00 per 1M output-tokens** — dat is Sonnet-achtige prijsstelling, dus dit is duidelijk
  niet "het" tarief maar één model
- actuele modellijst + prijzen programmatisch op te halen via **`/v1/models`**
- API-verbruik trekt van **dezelfde credit-pool** als je abonnement

### 5.6 Prijsvergelijking

| Optie | Prijs/maand | Wat je krijgt |
|---|---|---|
| Abacus Basic | $10 | alle modellen, 20k credits, 3 agent-runs |
| **Abacus Pro** | **$20** | alle modellen, 30k credits, onbeperkt agent/CLI/SuperComputer/Claw |
| ChatGPT Plus | $20 | alleen OpenAI-modellen |
| Claude Pro/Max | $20–$100+ | alleen Anthropic-modellen |
| Poe | ~$20 | multi-model, ook puntensysteem |
| OpenRouter | pay-per-token | multi-model API, geen agents/UI-laag |

Op papier wint Abacus Pro dit met grote marge. In de praktijk hangt het af van of het
creditsysteem je niet halverwege de maand stilzet.

---

## 6. Security & compliance

Volgens Abacus' eigen security-materiaal:
- **SOC 2 Type II, ISO/IEC 27001, HIPAA, GDPR, CCPA**
- zakelijke data wordt **niet gebruikt om modellen te trainen**
- modeltraining in geïsoleerde omgevingen; data van klant A verbetert nooit modellen voor klant B
- **zero data retention na sessie-einde**
- persoonlijke data wordt niet verkocht aan derden
- least-privilege toegang, alle toegang gelogd en periodiek geaudit
- **Enterprise/on-prem (AbacusOS):** jij houdt elke encryptiesleutel, Abacus heeft geen masterkey,
  geen backdoor, geen mogelijkheid je data te ontsleutelen; data verlaat je infrastructuur niet —
  niet voor verwerking, niet voor training, niet voor logging

Dit zijn vendor-claims uit hun eigen documentatie. Het certificeringsprofiel is wel serieus
(SOC 2 Type II + ISO 27001 + HIPAA is niet triviaal om te halen).

---

## 7. De schaduwkant — wat je moet weten vóór je betaalt

Dit komt uit Trustpilot, Reddit en kritische reviews. Het is consistent genoeg om serieus te nemen.

1. **Het creditsysteem is ondoorzichtig.** Gebruikers noemen het "onduidelijk, verwarrend en
   misleidend". Er is geen gepubliceerd per-model-tarief, dus **je kunt je maandverbruik niet
   vooraf berekenen.** Verhalen over credits die "zonder waarschuwing verdwijnen".
2. **De 75%-lockout.** Buitengesloten van geavanceerde modellen na ~15.000 credits, zonder
   duidelijke waarschuwing vooraf.
3. **Credits worden ook bij falen afgeschreven.** De agent rekent af per response, óók als het
   systeem in een loop zit of niets bruikbaars levert. Dat is de meest genoemde klacht.
4. **Klantenservice.** Meerdere gebruikers melden **nul reactie** op supportverzoeken, soms
   wekenlang; copy-paste antwoorden; en dat support stopt met reageren zodra je een refund vraagt.
5. **Refunds.** Gerapporteerd: annulering wordt bevestigd, het refund-verzoek wordt genegeerd.
6. **Stabiliteit.** Loops, vastlopers, contextverlies, hallucinaties bij websearch en complexe runs.
7. **Conclusie van kritische reviewers:** prima als flexibele AI-werkbank om mee te
   experimenteren, **niet geschikt voor bedrijfskritische processen** waar voorspelbaarheid telt —
   tenzij je eerst je eigen workloads test en de support-afspraken schriftelijk vastlegt.

**Praktisch advies:** betaal maandelijks, nooit vooruit voor een jaar. Gebruik een
betaalmethode die je makkelijk kunt stopzetten. Test in maand één met je eigen echte workload
en kijk hoeveel credits die daadwerkelijk kost, vóór je er iets van afhankelijk maakt.

---

## 8. Wat is hier bruikbaar voor jouw projecten

Concreet, met jouw setup (YouTube-pipeline met faceless kanalen, Shopify, micro-apps,
Claude Code + veel MCP-servers) in gedachten.

### 8.1 Sterk de moeite waard om te testen
- **RouteLLM API voor $10/maand.** Eén OpenAI-compatible endpoint naar 160+ modellen, met
  automatische failover. Als je in je pipelines nu losse API-keys per provider beheert, is dit
  een echte vereenvoudiging. Closed-source tegen providerprijs betekent dat je er niets op
  verliest; open-source is goedkoper. **Dit is waarschijnlijk het beste stuk van het hele aanbod
  voor jouw situatie.**
- **Studio voor thumbnails en video-assets.** Nano Banana Pro, Seedream, FLUX.2, Midjourney,
  plus Veo 3.1 / Kling v3 / Sora 2 — allemaal in één abonnement in plaats van vijf losse.
  Voor een faceless-kanalenpipeline die continu thumbnails en b-roll nodig heeft is dat
  potentieel een forse besparing. **Maar:** video is precies waar credits het snelst verdwijnen,
  dus reken dit door op je echte volume voordat je bestaande tools opzegt.
- **Browser Swarm voor research.** Parallel tientallen browsers die concurrentiekanalen,
  trending formats of productpagina's uitkammen en gestructureerd terugrapporteren. Dat is
  precies het soort werk waar jouw NexLev/vidIQ/Subscribr-stack aan de datakant zit — een
  swarm kan de gaten vullen waar geen API is.

### 8.2 Met voorzichtigheid
- **Agent Swarms voor content-productie.** Aantrekkelijk idee: één prompt → script, thumbnail,
  metadata en upload-voorbereiding parallel per kanaal. Maar: credits verdwijnen ook bij
  mislukte runs, en je hebt al een werkende pipeline. Test het naast je bestaande flow, vervang
  hem er niet mee.
- **AppLLM / SuperComputer voor micro-apps.** Always-on VM met database, storage en publieke
  HTTPS voor $20/maand is scherp geprijsd tegenover VPS + hosting + database apart. Goed voor
  MVP's, interne tools en automatiseringsbots. Niet voor iets waar uptime bedrijfskritisch is.

### 8.3 Waarschijnlijk niet vervangend
- **CodeLLM/CLI in plaats van Claude Code.** De benchmark-claims komen van Abacus zelf. Je hebt
  een werkende Claude Code-opstelling met je eigen skills, MCP-servers en routines. Dat
  vervangen op basis van een vendor-claim is geen goede ruil.
- **Abacus als bedrijfskritische automatiseringslaag.** Zie hoofdstuk 7.

### 8.4 Aanbevolen aanpak
1. Neem **Pro, $20, maandelijks** — niet Basic (3 agent-runs is niets).
2. Draai in de eerste maand drie concrete tests: één Browser Swarm research-run, één batch
   thumbnails/video in Studio, en één RouteLLM-integratie in een bestaand script.
3. **Houd het creditverbruik per test bij.** Dat getal is je echte prijs, niet de $20.
4. Beslis daarna per onderdeel of het iets vervangt — niet in één keer overstappen.

---

## 9. Openstaande vragen (niet te beantwoorden uit publieke bronnen)

- Exact credit-tarief per model — niet gepubliceerd; alleen meetbaar door zelf te testen.
- Maximum aantal worker agents per swarm — niet gevonden in enige bron.
- Of Agent Swarms expliciet Pro vereisen, of dat het onder de 3 Basic-agent-conversaties valt.
- Of er een jaarabonnement met korting bestaat — nergens gevonden, mogelijk bestaat het niet.
- Hoe credits precies verdeeld worden tussen chat, API-calls en CLI-gebruik.
- Of de 75%-throttle ook op Pro geldt of alleen op Basic (bronnen noemen alleen Basic).

---

## 10. Bronnen

**Officieel (niet direct leesbaar vanuit deze omgeving, wel via zoekindex):**
- https://abacus.ai/ — hoofdsite
- https://abacus.ai/help/chatllm-ai-super-assistant/agent-swarms — Agent Swarms how-to
- https://abacus.ai/help/chatllm-ai-super-assistant/deepagent — Abacus AI Agent how-to
- https://abacus.ai/help/platform-updates/2026-04-01-platform-update — april 2026 update
- https://abacus.ai/help/chatllm-ai-super-assistant/faqs/billing — billing FAQ
- https://abacus.ai/help/chatllm-ai-super-assistant/faqs/data-security — data security FAQ
- https://abacus.ai/help/chatllm-ai-super-assistant/computer-use-and-automation
- https://abacus.ai/help/chatllm-ai-super-assistant/abacus-claw
- https://abacus.ai/help/developer-platform/route-llm/ — RouteLLM API reference
- https://routellm-apis.abacus.ai/ — RouteLLM
- https://deepagent.abacus.ai/ , https://agent.abacus.ai/ — Agent
- https://studio.abacus.ai/faq — Studio FAQ
- https://supercomputer.abacus.ai/ — SuperComputer
- https://appllm.abacus.ai/ — AppLLM
- https://desktop.abacus.ai/ — Abacus AI Desktop
- https://claw.abacus.ai/ — Abacus Claw
- https://abacus.ai/security — security policy
- https://github.com/abacusai/codellm-releases — desktop releases

**Reviews en analyses:**
- https://www.kdnuggets.com/2026/08/abacus/honest-abacus-ai-review
- https://www.kdnuggets.com/2026/09/abacus/abacus-ai-candid-review/
- https://www.kdnuggets.com/2026/05/abacus/abacus-ai-review
- https://www.eesel.ai/blog/abacus-ai-pricing
- https://www.eesel.ai/blog/abacus-ai-reviews
- https://www.eesel.ai/blog/abacus-ai-alternatives
- https://www.revolutioninai.com/2026/04/how-does-abacus-ai-agent-swarm-work-explained.html
- https://roboticsandautomationnews.com/2026/08/24/abacus-ai-complete-guide-chatllm-personal-agents-supercomputer-and-studio-explained/104435/
- https://www.mindstudio.ai/blog/abacus-ai-supercomputer-always-on-agents
- https://myclaw.ai/blog/abacus-ai-agent-review
- https://krater.ai/blog/abacus-ai-chatllm-alternative
- https://www.trustpilot.com/review/abacus.ai — gebruikersklachten
- https://www.trustpilot.com/review/chatllm.abacus.ai

**Bedrijfsdata:**
- https://getlatka.com/companies/abacus.ai
- https://pitchbook.com/profiles/company/268042-42
- https://www.crunchbase.com/organization/realityengines
- https://tracxn.com/d/companies/abacusai/
