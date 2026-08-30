# External Dataset Discovery Run

Date: `2026-05-08`

## Goal

Find more existing datasets for the people graph, with special attention to:

- Hugging Face datasets
- GitHub repos with committed raw data
- Sourcegraph/code-search style repo discovery
- quote and identity graphs
- podcast/interview transcript corpora
- creator/guru archives
- freshness: repo update date, dataset update date, and content coverage range

## Sourcegraph CLI

Official install guidance says Homebrew can install Sourcegraph CLI with:

```bash
brew install sourcegraph/src-cli/src-cli
```

Homebrew tapped `sourcegraph/src-cli`, but the install stalled while fetching. I then switched to the latest direct GitHub release binary:

- release: `sourcegraph/src-cli` `7.2.1`
- published: `2026-04-30T15:36:48Z`
- asset: `src_darwin_arm64`
- installed: `~/.local/bin/src`
- verified version: `7.2.1`

The first Sourcegraph searches were useful but noisy. Clean saves from this pass:

- `kani3894/nate-jones-transcripts` surfaced through Dario/Sam searches, including a 2026-01-12 Sam Altman/Dario Amodei transcript index entry.
- `progremir/navalmanac` surfaced through Naval searches as a docstore mirror/chunking example.

The Alex Hormozi search was mostly workflow/prompt noise, and the Bob Proctor transcript search returned no clean corpus.

### AI-Focused Follow-up

A later pass focused on recent AI people, podcasts, and transcript archives. Sourcegraph was the main discovery tool, with Hugging Face and GitHub metadata used to verify freshness.

New saves from that pass:

- `kani3894/nate-jones-transcripts` was expanded from one Sam/Dario lead into a broader AI-news transcript archive. Its topic indexes include OpenAI, Anthropic, DeepMind, Nvidia, Microsoft, Google, Meta, xAI, Claude, Gemini, GPT-5, AI agents, and AI strategy. The Nvidia index alone lists 45 episodes from `2024-07-09` to `2026-01-13`, including a `2025-01-07` Jensen Huang/CES keynote episode.
- `willtheorangeguy` Practical AI transcript datasets on Hugging Face cover yearly Practical AI transcript files from `2018` through `2025`. All checked yearly datasets were created/updated on `2026-04-17` with MIT claimed on the cards.
- `K-Dense-AI/mimeo` is a recent MIT repo that generates source maps and agent skills for AI researchers. Output folders include Ilya Sutskever, Demis Hassabis, Andrej Karpathy, Andrew Ng, Fei-Fei Li, Geoffrey Hinton, Yann LeCun, Yoshua Bengio, Jeff Dean, Stuart Russell, and others. It is best used as a source-map layer, not as primary text.
- `filipwx/ted-podcast-finetune` is a recent Hugging Face mixed TED/Lex/Joe transcript fine-tuning dataset with CSV/JSONL files and CC-BY-4.0 claimed on the card.
- `ai-frontier-web-transcript-pages` was added as a curated source cluster for targeted crawling of Lex, Dwarkesh, Singju/Big Technology, Rev, Cheeky Pint, Eye on AI, Podscripts, LifeArchitect, Stanford eCorner, and LessWrong transcript leads.
- `cdubiel08/Earnings-Calls-NLP` was added as an older Jensen/NVIDIA earnings-call format/reference source. It is lower priority than the broader `kurry/sp500_earnings_transcripts` source.

## High-Value New Candidates

### People / Transcript / Belief Graph

- `BeliefEngines/podcast-transcripts`  
  URL: https://huggingface.co/datasets/BeliefEngines/podcast-transcripts  
  Updated: `2026-04-21`  
  Why it matters: small but structurally perfect for us: persons, beliefs, quotes, transcript chunks, embeddings, and episode metadata.  
  Caution: derived belief extraction needs provenance and quality review.

- `kurry/sp500_earnings_transcripts`  
  URL: https://huggingface.co/datasets/kurry/sp500_earnings_transcripts  
  Coverage: `2005-2025`  
  Updated: `2025-05-21`  
  Why it matters: high-value executive corpus for CEO/CFO/company-time edges.  
  Caution: transcript rights and speaker normalization.

- `jan-hq/youtube_transcripts_raw`  
  URL: https://huggingface.co/datasets/jan-hq/youtube_transcripts_raw  
  Updated: `2024-03-13`  
  Why it matters: small AI/tech YouTube transcript seed; sample starts with Jensen Huang Stanford interview.  
  Caution: no visible license and small size.

- `rchiera/podcast-transcripts`  
  URL: https://huggingface.co/datasets/rchiera/podcast-transcripts  
  Updated: `2026-02-13`  
  Why it matters: podcast metadata plus speaker slugs, useful for person-episode graph edges.  
  Caution: finance/Bitcoin niche and some unknown speakers.

- `kani3894/nate-jones-transcripts`  
  URL: https://github.com/kani3894/nate-jones-transcripts  
  Updated: `2026-05-04T22:43:33Z`  
  Why it matters: Sourcegraph found AI transcript indexes, including a 2026-01-12 Sam Altman/Dario Amodei transcript.  
  Caution: no detected license; inspect episode files before text import.

### Founder / Business / Creator Corpora

- `sgoel9/sam_altman_essays`  
  URL: https://huggingface.co/datasets/sgoel9/sam_altman_essays  
  Updated: `2024-04-20`  
  Rows: `112`  
  Why it matters: compact Sam Altman essay corpus with row-level blog dates.

- `sgoel9/paul_graham_essays`  
  URL: https://huggingface.co/datasets/sgoel9/paul_graham_essays  
  Updated: `2024-04-20`  
  Rows: `215`  
  Why it matters: compact Paul Graham essay corpus.

- `evmn/Paul-Graham`  
  URL: https://github.com/evmn/Paul-Graham  
  Updated: `2026-01-30`  
  Why it matters: committed Paul Graham essay archive.  
  Caution: Paul Graham essay copyright/attribution remains external.

- `diogo-cruz/summarizer`  
  URL: https://github.com/diogo-cruz/summarizer  
  Updated: `2026-05-08`  
  Why it matters: mirrored Dwarkesh/Dario/AI interview originals, PDFs, metadata, and summaries.  
  Caution: no detected license; distinguish originals from summaries.

- `nem035/tim.nem.ai`  
  URL: https://github.com/nem035/tim.nem.ai  
  Updated: `2024-08-09`  
  Why it matters: Tim Ferriss transcript app with Naval, Tony Robbins, Warren Buffett-adjacent episodes.  
  Caution: no detected license.

- `lawwu/transcripts`  
  URL: https://github.com/lawwu/transcripts  
  Updated: `2026-04-11`  
  Why it matters: direct Jim Rohn and Tony Robbins transcript files.  
  Caution: limited coverage and no detected license.

- `sos-enxaqueca/aios-squads`  
  URL: https://github.com/sos-enxaqueca/aios-squads  
  Updated: `2026-03-03`  
  Why it matters: structured Naval mind folder and partial Alex Hormozi mind/source inventory.  
  Caution: mixed raw and synthesized artifacts.

### Quote / Identity / Interview Infrastructure

- `Interview Records`  
  URL: https://www.interviewrecords.com/  
  Why it matters: public interview records by person, date, topic, format, transcript status, and rights notes. It advertises a complete `data.bundle.json`.  
  Caution: source index, not transcript owner.

- `Podcast Index`  
  URL: https://podcastindex.org/  
  Why it matters: best podcast/feed discovery layer. Podcasting 2.0 tags can expose transcript/person/license metadata.  
  Caution: metadata does not grant transcript reuse rights.

- `NASA Oral Histories`  
  URL: https://www.nasa.gov/history/history-publications-and-resources/oral-histories/  
  Updated: `2026-03-09`  
  Why it matters: official oral-history archive for aerospace/science figures.  
  Caution: item-level rights and partner materials still need checking.

- `NARA White House Transition Interviews`  
  URL: https://www.archives.gov/presidential-libraries/research/transition-interviews  
  Why it matters: official public-domain oral-history transcripts.  
  Caution: narrow domain, but very clean provenance.

- `Quotebank`  
  URL: https://zenodo.org/records/4277311  
  Coverage: `2008-09` to `2020-04`  
  Why it matters: 235M speaker-attributed quotes from news articles.  
  Caution: huge and model-extracted speaker attribution.

## Existing Candidates Reconfirmed

- `ScribeSalad` remains the best raw Alex Hormozi/YouTube transcript lead.
- `ChatPRD/lennys-podcast-transcripts` remains the cleanest Lenny transcript import.
- `LennysNewsletter/lennys-newsletterpodcastdata` remains the official Lenny starter pack.
- `nmac/lex_fridman_podcast` remains the best timestamped older Lex dataset.
- `Aditya0619/lex-fridman-podcast` remains the broader/newer whole-episode Lex dataset through early 2025.
- Official Lex and Dwarkesh transcript pages remain the best current-source path for frontier AI leaders.
- Wikidata remains the identity spine.
- QuoteKG/Wikiquote remain the quote spine.

## Import Priority

1. `ScribeSalad` Alex Hormozi metadata first, transcript text later after rights/provenance review.
2. `BeliefEngines/podcast-transcripts` for schema inspiration and possible belief/quote/person imports.
3. `sgoel9/sam_altman_essays` and `sgoel9/paul_graham_essays` as compact worldview corpora.
4. `kurry/sp500_earnings_transcripts` for public-company executive speech and company-time edges.
5. `Interview Records` and `Podcast Index` as discovery/metadata layers.
6. `diogo-cruz/summarizer` for Dwarkesh/Dario/AI interview original pages and metadata.
7. `NARA` and `NASA` official oral histories as clean public-domain/official archives.

## Freshness Lesson

Track three clocks separately:

- `observed_at`: when we inspected the dataset.
- `source_last_updated`: when the upstream repo/dataset/page last changed.
- `data_coverage_start/end`: what source-content period the dataset actually covers.

For transcript imports, source-content dates matter more than repo update dates.

## Additional Rolling Sources Logged

Discovered and added after the first registry pass:

- `Podchaser API`  
  URL: https://www.podchaser.com/api  
  Visible volume: `5.5M+` podcasts, `4M+` episode transcripts, `27M+` host/guest/crew credits, `20K+` charts.  
  Why it matters: strong live people/podcast appearance graph for AI leaders, founders, CEOs, and creators.  
  Caution: commercial API; transcript access is not the same as redistribution rights.

- `Podscan API`  
  URL: https://help.podscan.fm/en/article/building-podcast-powered-applications-with-the-podscan-api-13741kz/  
  Visible volume: `4M+` podcasts and `46M+` episodes with transcripts/entities/real-time updates.  
  Why it matters: useful monitoring source for current AI-leader podcast appearances.  
  Caution: paid/API terms and entity extraction quality need review.

- `Listen Notes API`  
  URL: https://www.listennotes.com/api/  
  Visible volume: `3.7M+` podcasts and `192M+` episodes from a third-party source-directory snapshot.  
  Why it matters: broad podcast/feed/episode discovery backstop.  
  Caution: primarily metadata/search, not guaranteed transcripts.

- `Taddy Podcast API`  
  URL: https://taddy.org/developers  
  Visible volume: `4M+` podcasts and `200M+` episodes, with transcript/search/webhook support.  
  Why it matters: rolling feed discovery plus webhooks for new episodes.  
  Caution: validate transcript coverage and storage terms on target podcasts.

- `spoken.md`  
  URL: https://spoken.md/  
  Visible volume: `2,000+` transcripts fetched by developers; on-demand transcript API.  
  Why it matters: cheap targeted transcript fetch path after we discover high-priority episodes.  
  Caution: commercial per-transcript cost; speaker-name detection needs verification.

- `CEOInterviews.AI API`  
  URL: https://ceointerviews.ai/api_docs/  
  Visible volume: `20,000+` CEOs/executives and `1M+` verified quotes/full transcripts from docs/search.  
  Why it matters: direct executive-speech database for public-company leaders.  
  Caution: proprietary/commercial; verify reuse terms and source provenance.

- `Tapesearch API/search`  
  URL: https://www.tapesearch.com/api/tos  
  Visible volume: `4M+` podcast episodes from search-directory snapshot.  
  Why it matters: good search/discovery layer for person/topic appearances.  
  Caution: terms explicitly prohibit harvesting to replicate the database.

- `Podafi`  
  URL: https://podafi.com/  
  Visible volume: `1,159` transcripts, `198` podcasts, `18` categories from prior search snapshot.  
  Why it matters: small browsable transcript directory with daily ranking/monitoring signals.  
  Caution: rights unclear; exact counts should be rechecked because it is live.

- `Podgist`  
  URL: https://www.podgist.com/  
  Visible volume: public page claims thousands of shows/episodes.  
  Why it matters: transcript library with speaker labels, chapters, links to original audio, topics, and entities.  
  Caution: exact count and export rights need inspection.

- `SumBest`  
  URL: https://sum.best/  
  Visible volume: `25` ready catalog episodes in the visible AI/founder shows snapshot.  
  Why it matters: narrow but very relevant AI/founder transcript catalog covering Lenny, All-In, Dwarkesh, No Priors, and 20VC-style shows.  
  Caution: small visible catalog; useful as schema/discovery reference more than a bulk source today.
