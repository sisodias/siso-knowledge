# External People Dataset Search

Generated: `2026-05-08`

## Short Answer

Yes: there are already useful public repositories and datasets for exactly this kind of work. The best hits are not one universal "people graph" database, but a patchwork of transcript archives, creator-specific RAG apps, public starter packs, podcast datasets, quote corpora, and source indexes.

The immediate highest-value targets are:

- `wa3dbk/ScribeSalad` for broad YouTube transcript/video metadata, including Alex Hormozi metadata.
- `ChatPRD/lennys-podcast-transcripts` for product/founder/operator interviews with clean markdown/frontmatter.
- `LennysNewsletter/lennys-newsletterpodcastdata` for an official Lenny starter dataset.
- `nmac/lex_fridman_podcast` for timestamped Lex Fridman transcripts that cover many AI leaders.
- `Aditya0619/lex-fridman-podcast` for newer whole-episode Lex transcripts through early 2025.
- official Lex and Dwarkesh transcript pages for the newest priority AI leader interviews.
- `Wikidata` plus `QuoteKG` for the identity/quote spine.
- `PleIAs/YouTube-Commons` for a rights-clean CC-BY broad YouTube transcript backfill.
- `cdeistopened/hormozi-wiki` as a secondary Hormozi framework/knowledge-base lead.

## Search Notes

Sourcegraph CLI is installed at `~/.local/bin/src` and verified at version `7.2.1`. Homebrew stalled while fetching, so the direct GitHub release asset was used. Sourcegraph added two save-worthy leads (`kani3894/nate-jones-transcripts` and `progremir/navalmanac`) but also returned a lot of workflow/prompt noise for creator searches. Firecrawl is available as a search skill but still requires authentication in this workspace, so it remains a later accelerator once credentials are configured.

## Ranked Candidates

### P0 Import Candidates

1. **ScribeSalad**  
   URL: https://github.com/wa3dbk/ScribeSalad  
   Why it matters: broad YouTube transcript corpus. GitHub metadata says it is a collection of YouTube video transcripts across podcasts, lectures, and many topics. The repo has GPL-3.0 metadata and includes Alex Hormozi title/video-id metadata under `meta/titles/en/AlexHormozi.en.lst` and `meta/videos_ids/en/AlexHormozi.en.lst`.  
   Import idea: ingest metadata first as candidate videos. Selectively import transcript files only after checking person/channel paths and tagging upstream license/provenance.  
   Caution: transcript rights are separate from repo license; isolate imported data from code.

2. **ChatPRD/lennys-podcast-transcripts**  
   URL: https://github.com/ChatPRD/lennys-podcast-transcripts  
   Why it matters: README states 269 Lenny's Podcast transcripts. Each episode has YAML frontmatter including guest, title, YouTube URL, video ID, publish date, description, duration, view count, and channel.  
   Import idea: guest-name match against our registry and import episodes for Brian Chesky, Patrick Collison, Claire Hughes Johnson, product/founder people, and other operators.  
   Caution: README says transcripts are for educational/research purposes and content belongs to creators.

3. **LennysNewsletter/lennys-newsletterpodcastdata**  
   URL: https://github.com/LennysNewsletter/lennys-newsletterpodcastdata  
   Why it matters: official public starter pack. README states 10 newsletter posts and 50 podcast transcripts, with `index.json` for titles, dates, word counts, guests, descriptions.  
   Import idea: metadata import first; content import only within custom license terms.  
   Caution: custom license; full archive is paid/private.

4. **nmac/lex_fridman_podcast**  
   URL: https://huggingface.co/datasets/nmac/lex_fridman_podcast  
   Why it matters: dataset card says Lex Fridman Podcast episodes 1-325, about 803K transcript entries, with fields for guest, title, text, start, and end timestamps. It points to Andrej Karpathy's lexicap as source data.  
   Import idea: map by guest to AI leaders such as Demis Hassabis, Sam Altman, Mark Zuckerberg, Elon Musk, Geoffrey Hinton, Yoshua Bengio, Yann LeCun, Andrej Karpathy.  
   Caution: license not obvious in the initial card; Whisper transcript quality needs review.

5. **Aditya0619/lex-fridman-podcast**  
   URL: https://huggingface.co/datasets/Aditya0619/lex-fridman-podcast  
   Why it matters: subagent found 441 full-episode Lex transcripts with newer coverage than the nmac timestamped dataset, including Dario Amodei episode 452.  
   Import idea: use for whole-episode backfill, then chunk locally.  
   Caution: MIT claim on dataset packaging may not clear underlying transcript rights.

6. **Official Lex transcript pages**  
   URL: https://lexfridman.com/category/transcripts/  
   Why it matters: strongest source for newest priority interviews such as Jensen Huang, newer Demis Hassabis, Dario Amodei, Sam Altman, and Andrej Karpathy.  
   Import idea: targeted page-level scraping with timestamp anchors.  
   Caution: public page does not imply broad bulk-data license.

7. **Dwarkesh official pages**  
   URL: https://www.dwarkesh.com/archive  
   Why it matters: directly covers Ilya Sutskever, Dario Amodei, Jensen Huang, and many AI/company people.  
   Import idea: targeted import by episode page.  
   Caution: strip sponsor/subscription boilerplate and verify transcript availability.

8. **Wikidata official dumps**  
   URL: https://www.wikidata.org/wiki/Wikidata:Database_download  
   Why it matters: best people identity spine. Facts/IDs are CC0 and can resolve names across all other datasets.  
   Import idea: add `wikidata_qid`, aliases, occupations, dates, sitelinks, identifiers, and sameAs links to the registry.  
   Caution: huge dump; media and sensitive living-person claims require separate policy.

9. **QuoteKG**  
   URL: https://quotekg.l3s.uni-hannover.de/  
   Why it matters: quote knowledge graph with nearly 1M quotes and nearly 70K persons, derived from Wikiquote.  
   Import idea: attributed quote candidates linked to people; map through Wikidata where possible.  
   Caution: Wikiquote licensing, quote-level copyright, and misattribution issues remain.

10. **PleIAs/YouTube-Commons**  
    URL: https://huggingface.co/datasets/PleIAs/YouTube-Commons  
    Why it matters: subagent found a 2M+ video transcript corpus from CC-BY YouTube videos with provenance.  
    Import idea: broad rights-aware backfill by person/channel/title filter.  
    Caution: only CC-BY videos, not standard-license podcast channels.

### P1 Research Candidates

11. **cdeistopened/hormozi-wiki**  
   URL: https://github.com/cdeistopened/hormozi-wiki  
   Why it matters: an Ask Hormozi creator-archive plugin with framework markdown files, including CLOSER, value equation, grand slam offers, pricing psychology, lead magnets, and outreach.  
   Import idea: treat as distilled framework leads. Trace each framework back to primary Hormozi source before promoting to graph claims.  
   Caution: no license observed and likely derivative summaries.

12. **Gristle18/HarmoziGPT**  
   URL: https://github.com/Gristle18/HarmoziGPT  
   Why it matters: repo description says it is trained on Alex Hormozi content and includes Whisper transcription plus speaker diarization.  
   Import idea: inspect for reusable pipeline/manifests.  
   Caution: no license observed; need verify if actual data is present.

13. **Tapesearch Alex Hormozi index**  
   URL: https://app.tapesearch.com/person/alex-hormozi  
   Why it matters: web search indicated it indexes multiple Alex Hormozi podcast transcripts with snippets and timestamps.  
   Import idea: discovery only; collect original episode sources separately.  
   Caution: terms/rights review required.

14. **lord-denning/Huberman-Lab-Podcast-Transcripts**  
   URL: https://github.com/lord-denning/Huberman-Lab-Podcast-Transcripts  
   Why it matters: README says Markdown/Word transcripts for most Huberman episodes 1-30.  
   Import idea: import format example; low priority unless Huberman/guests enter the people graph.  
   Caution: no license observed and limited coverage.

15. **lawwu/transcripts**  
   URL: https://github.com/lawwu/transcripts  
   Why it matters: repo description says various YouTube channel transcripts inspired by Karpathy's lexicap.  
   Import idea: inspect channel coverage for AI/founder overlap.  
   Caution: no license observed.

### P2 Reference / Product Shape

10. **wombyz/HormoziGPT**  
    URL: https://github.com/wombyz/HormoziGPT  
    Why it matters: popular Alex Hormozi GPT app.  
    Import idea: product/interface reference, not a direct corpus source until data is found.  
    Caution: no license observed and visible root looked like app code/prompts rather than transcript files.

11. **Lenny knowledge graph/RAG ecosystem**  
    URLs named in ChatPRD README include Lenny MCP, Lennyhub RAG, Ask Lenny, Lenny's Knowledge Graph, Lenny's Frameworks, and other downstream projects.  
    Why it matters: this is a working market map for what our people graph could become: transcript archive -> topic index -> skills/frameworks -> RAG/MCP/knowledge graph.  
    Import idea: product inspiration and possible code references.  
    Caution: treat downstream generated insights as secondary until source-linked.

## Recommended Next Build

Add an importer for `external_datasets.yaml` that can:

- validate candidate dataset metadata,
- create per-dataset import tasks,
- import video IDs/title lists into the existing YouTube candidate queue,
- import markdown transcripts with frontmatter into normalized transcript YAML,
- mark each imported object with `upstream_url`, `license_observed`, `rights_status`, and `imported_at`,
- keep GPL/custom/unknown-license text out of redistributable generated artifacts unless explicitly approved.
- emit the richer freshness/provenance manifest described in `external_dataset_freshness_schema.md`.

First practical import:

1. Import ScribeSalad Alex Hormozi metadata as candidate videos.
2. Import Lenny podcast metadata for registry-matched guests.
3. Import Lex Fridman Hugging Face rows for registry-matched guests after license review.
4. Use `hormozi-wiki` only as a framework lead list until source trace is done.
