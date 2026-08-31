# External Dataset Status

Generated: `2026-05-08`
Datasets tracked: `60`

## Status Counts

- `blocked`: `1`
- `p0_import_candidate`: `25`
- `p1_research_candidate`: `32`
- `p2_reference_only`: `2`

## Source Types

- `ai_podcast_transcript_series`: `1`
- `ai_researcher_source_maps_and_agent_skills`: `1`
- `ai_tech_youtube_transcript_chunks`: `1`
- `author_style_text_dataset`: `1`
- `book_text_dataset`: `1`
- `cc_by_youtube_transcript_corpus`: `1`
- `creator_knowledge_base`: `1`
- `creator_rag_app`: `2`
- `creator_transcription_pipeline`: `1`
- `curated_web_transcript_sources`: `1`
- `distilled_business_book_skills`: `1`
- `distilled_creator_project`: `1`
- `distilled_person_skill`: `1`
- `earnings_call_transcript_archive`: `1`
- `earnings_call_transcript_corpus`: `1`
- `essay_corpus`: `2`
- `executive_interview_quote_transcript_database`: `1`
- `gap_marker`: `1`
- `identity_knowledge_graph`: `1`
- `lex_transcript_app_or_dataset`: `1`
- `media_interview_transcript_corpus`: `1`
- `mixed_ted_lex_joe_rogan_transcript_finetune_dataset`: `1`
- `multi_channel_transcript_archive`: `1`
- `official_oral_history_archive`: `1`
- `official_oral_history_transcripts`: `1`
- `official_starter_pack`: `1`
- `official_transcript_pages`: `2`
- `on_demand_podcast_transcript_api`: `1`
- `person_distillation_toolkit`: `1`
- `person_rag_docstore`: `1`
- `podcast_belief_quote_graph_dataset`: `1`
- `podcast_conversation_dataset`: `1`
- `podcast_metadata_index`: `1`
- `podcast_transcript_archive`: `2`
- `podcast_transcript_corpus`: `1`
- `podcast_transcript_dataset`: `2`
- `podcast_transcript_research_corpus`: `1`
- `podcast_transcript_search_index`: `1`
- `public_domain_book_catalog`: `1`
- `public_interview_index`: `1`
- `quote_corpus`: `1`
- `quote_knowledge_graph`: `1`
- `rolling_ai_podcast_transcript_library`: `1`
- `rolling_podcast_metadata_search_api`: `1`
- `rolling_podcast_metadata_transcript_api`: `1`
- `rolling_podcast_transcript_directory`: `1`
- `rolling_podcast_transcript_people_index`: `1`
- `rolling_podcast_transcript_search_api`: `1`
- `rolling_podcast_transcript_search_index`: `1`
- `rolling_podcast_transcript_summary_library`: `1`
- `transcript_rag_knowledge_graph_app`: `1`
- `web_transcript_archive`: `1`
- `wikiquote_dump_dataset`: `1`
- `youtube_transcript_archive`: `1`
- `youtube_transcript_corpus`: `1`

## P0 Import Candidates

### ScribeSalad

- URL: https://github.com/wa3dbk/ScribeSalad
- Type: `youtube_transcript_corpus`
- Platform: `github`
- License observed: `GPL-3.0`
- Observed at: `2026-05-08`
- Source last updated: `2026-04-13T21:47:38Z`
- Data coverage: `unknown` to `unknown`
- Data volume: `940k+ YouTube transcripts (README claim; import selected channel/person slices only.)`
- Freshness notes: Large corpus appears recently maintained; per-channel/video title lists need per-video publish dates during import.
- Mapped people: alex-hormozi, lex-fridman-adjacent, joe-rogan-adjacent, tim-ferriss-adjacent, y-combinator-adjacent
- Import strategy: Start by importing metadata/title/video-id lists as candidate videos, then selectively mirror transcript files only where present and compatible with our rights policy. Keep GPL contamination risk isolated from core source code and tag imported text with upstream license/provenance.


### ChatPRD/lennys-podcast-transcripts

- URL: https://github.com/ChatPRD/lennys-podcast-transcripts
- Type: `podcast_transcript_archive`
- Platform: `github`
- License observed: `personal_educational_use_in_readme`
- Observed at: `2026-05-08`
- Source last updated: `2026-05-08T05:47:38Z`
- Data coverage: `unknown` to `unknown`
- Data volume: `269 podcast transcripts (README claim for Lenny's Podcast.)`
- Freshness notes: Repo is highly current; episode-level publish dates are available in transcript frontmatter and should be imported.
- Mapped people: lenny-rachitsky, brian-chesky, patrick-collison, claire-hughes-johnson, product-founder-leaders
- Import strategy: Import as podcast episodes where guest matches our registry. Keep transcripts marked rights_review/personal_educational and link back to YouTube/original episode.


### LennysNewsletter/lennys-newsletterpodcastdata

- URL: https://github.com/LennysNewsletter/lennys-newsletterpodcastdata
- Type: `official_starter_pack`
- Platform: `github`
- License observed: `custom_license`
- Observed at: `2026-05-08`
- Source last updated: `2026-05-08T05:12:38Z`
- Data coverage: `unknown` to `unknown`
- Data volume: `60 starter records (10 newsletter posts plus 50 podcast transcripts.)`
- Freshness notes: Official starter pack is current; full paid archive intentionally excludes recent newsletters per README.
- Mapped people: lenny-rachitsky, brian-chesky, patrick-collison, product-founder-leaders
- Import strategy: Import starter metadata first; import content only within custom license terms.

### nmac/lex_fridman_podcast

- URL: https://huggingface.co/datasets/nmac/lex_fridman_podcast
- Type: `podcast_transcript_dataset`
- Platform: `huggingface`
- License observed: `not_observed_in_card`
- Observed at: `2026-05-08`
- Source last updated: `2023-01-31T16:24:07Z`
- Data coverage: `episode_1` to `episode_325`
- Data volume: `803k timestamped transcript entries (Lex episodes 1-325.)`
- Freshness notes: Timestamped but stale for newer Lex episodes; useful for older AI leader interviews.
- Mapped people: demis-hassabis, sam-altman, mark-zuckerberg, elon-musk, geoffrey-hinton, yoshua-bengio, yann-lecun, andrej-karpathy
- Import strategy: Import by guest-name match into normalized transcript YAML with timestamps; keep upstream attribution to Karpathy lexicap and Hugging Face dataset.


### Aditya0619/lex-fridman-podcast

- URL: https://huggingface.co/datasets/Aditya0619/lex-fridman-podcast
- Type: `podcast_transcript_dataset`
- Platform: `huggingface`
- License observed: `MIT_claimed_on_dataset_card`
- Observed at: `2026-05-08`
- Source last updated: `2025-01-20T17:35:51Z`
- Data coverage: `episode_1` to `episode_452_era`
- Data volume: `441 full-episode transcripts (Hugging Face card/preview count.)`
- Freshness notes: Newer than nmac; still misses 2025 episodes after January 20, including Jensen
- Mapped people: dario-amodei, sam-altman, demis-hassabis, andrej-karpathy, ilya-sutskever, ai-researchers-technical-thinkers
- Import strategy: Use as broad whole-episode Lex backfill after rights review. Chunk transcripts locally and map episode titles to registry people.


### Official Lex Fridman transcript pages

- URL: https://lexfridman.com/category/transcripts/
- Type: `official_transcript_pages`
- Platform: `web`
- License observed: `rights_review`
- Observed at: `2026-05-08`
- Source last updated: `rolling_site`
- Data coverage: `unknown` to `current_when_page_exists`
- Data volume: `unknown`
- Freshness notes: Best source for newest Lex transcripts; capture individual page publish/episode dates during scraping.
- Mapped people: dario-amodei, demis-hassabis, jensen-huang, sam-altman, andrej-karpathy, mark-zuckerberg, elon-musk
- Import strategy: Scrape only priority episode transcript pages with provenance and page timestamp anchors; avoid broad crawling unless terms permit.


### Dwarkesh Podcast official pages

- URL: https://www.dwarkesh.com/archive
- Type: `official_transcript_pages`
- Platform: `web`
- License observed: `rights_review`
- Observed at: `2026-05-08`
- Source last updated: `rolling_site`
- Data coverage: `unknown` to `current_when_page_exists`
- Data volume: `unknown`
- Freshness notes: Strong for current frontier-AI interviews; capture episode publish dates from each page/feed.
- Mapped people: ilya-sutskever, dario-amodei, jensen-huang, demis-hassabis, mark-zuckerberg, satya-nadella, andrej-karpathy
- Import strategy: Use targeted page scraping for selected official episode pages, strip boilerplate/sponsor content, and keep episode URL/timestamp provenance.


### PleIAs/YouTube-Commons

- URL: https://huggingface.co/datasets/PleIAs/YouTube-Commons
- Type: `cc_by_youtube_transcript_corpus`
- Platform: `huggingface`
- License observed: `cc-by-4.0`
- Observed at: `2026-05-08`
- Source last updated: `unknown`
- Data coverage: `unknown` to `unknown`
- Data volume: `2M+ video transcripts (CC-BY YouTube transcript corpus.)`
- Freshness notes: Large CC-BY corpus; import must preserve video upload date and dataset snapshot/version.
- Mapped people: ai-researchers-technical-thinkers, frontier-ai-company-leaders, creator-interview-corpus
- Import strategy: Use as rights-clean broad backfill by filtering title/channel/person names. Keep CC-BY attribution fields attached to every imported transcript chunk.


### Wikidata official dumps

- URL: https://www.wikidata.org/wiki/Wikidata:Database_download
- Type: `identity_knowledge_graph`
- Platform: `wikimedia`
- License observed: `CC0`
- Observed at: `2026-05-08`
- Source last updated: `rolling_wikimedia_dumps`
- Data coverage: `unknown` to `current_dump_when_downloaded`
- Data volume: `unknown`
- Freshness notes: Store dump date and revision IDs for every identity import.
- Mapped people: all-registry-people
- Import strategy: Add QID/alias/sitelink/enrichment fields to our people registry and use Wikidata as the resolver for names across quote, podcast, and corpus datasets.


### QuoteKG

- URL: https://quotekg.l3s.uni-hannover.de/
- Type: `quote_knowledge_graph`
- Platform: `web`
- License observed: `wikiquote_derived_cc_by_sa_expected`
- Observed at: `2026-05-08`
- Source last updated: `unknown`
- Data coverage: `unknown` to `unknown`
- Data volume: `1M quotes; 70K persons`
- Freshness notes: Needs dataset release/snapshot date before import; likely less current than live Wikiquote dumps.
- Mapped people: historic-philosophy-fundamental-thinkers, business-wealth-persuasion-self-mastery, strategy-power-history-civilization, writers-sensemakers
- Import strategy: Import quote candidates by linked person where possible, map to Wikidata, and mark quotes as attributed/unverified until source citations are traced.


### Project Gutenberg catalog metadata

- URL: https://www.gutenberg.org/ebooks/offline_catalogs.html
- Type: `public_domain_book_catalog`
- Platform: `project_gutenberg`
- License observed: `public_domain_us_plus_gutenberg_terms`
- Observed at: `2026-05-08`
- Source last updated: `rolling_catalog`
- Data coverage: `public_domain_works` to `current_catalog_when_downloaded`
- Data volume: `unknown`
- Freshness notes: Store catalog snapshot date and ebook release/update date.
- Mapped people: historic-philosophy-fundamental-thinkers, strategy-power-history-civilization, writers-sensemakers
- Import strategy: Import metadata first, then selectively download public-domain texts using our existing raw source ingest path.


### yoonholee/style-eval-corpus

- URL: https://huggingface.co/datasets/yoonholee/style-eval-corpus
- Type: `author_style_text_dataset`
- Platform: `huggingface`
- License observed: `cc0-1.0_dataset_with_source_specific_rights`
- Observed at: `2026-05-08`
- Source last updated: `unknown`
- Data coverage: `unknown` to `unknown`
- Data volume: `52 Naval pieces (about 46K words from navalmanack.com.)`
- Freshness notes: Static Naval Almanack-derived text; source text is not a live transcript archive.
- Mapped people: naval-ravikant
- Import strategy: Filter rows by author == Naval Ravikant and import as written/source-text candidates after checking Navalmanack source license.


### BeliefEngines/podcast-transcripts

- URL: https://huggingface.co/datasets/BeliefEngines/podcast-transcripts
- Type: `podcast_belief_quote_graph_dataset`
- Platform: `huggingface`
- License observed: `MIT_claimed_on_card`
- Observed at: `2026-05-08`
- Source last updated: `2026-04-21`
- Data coverage: `unknown` to `unknown`
- Data volume: `556 rows (includes persons, beliefs, quotes, transcript chunks, embeddings, and episode metadata.)`
- Freshness notes: Recent small dataset; especially interesting because it already has persons, beliefs, quotes, transcript chunks, embeddings, and episode metadata.
- Mapped people: podcast-interview-corpus, bitcoin-finance-thinkers, belief-graph-reference
- Import strategy: Inspect schema first, then use as a model for our own belief/quote/person extraction tables. Import content only after rights review.


### kurry/sp500_earnings_transcripts

- URL: https://huggingface.co/datasets/kurry/sp500_earnings_transcripts
- Type: `earnings_call_transcript_corpus`
- Platform: `huggingface`
- License observed: `MIT_claimed_on_card`
- Observed at: `2026-05-08`
- Source last updated: `2025-05-21`
- Data coverage: `2005` to `2025`
- Data volume: `33,362 rows (S&P 500 earnings-call transcripts.)`
- Freshness notes: Large executive corpus with explicit 2005-2025 coverage; useful for CEO/company-time edges.
- Mapped people: big-tech-platform-ceos, public-company-executives, lisa-su, tim-cook, satya-nadella, sundar-pichai
- Import strategy: Import metadata and speaker/company/date edges first. Use transcript text only after rights review and speaker normalization.


### sgoel9/sam_altman_essays

- URL: https://huggingface.co/datasets/sgoel9/sam_altman_essays
- Type: `essay_corpus`
- Platform: `huggingface`
- License observed: `apache-2.0_card_with_mit_text_inconsistency`
- Observed at: `2026-05-08`
- Source last updated: `2024-04-20`
- Data coverage: `unknown` to `2023-12-21_sample_visible`
- Data volume: `112 essay rows (Sam Altman blog essay corpus.)`
- Freshness notes: Compact Sam Altman essay corpus; row-level blog dates visible and should drive coverage assessment.
- Mapped people: sam-altman
- Import strategy: Import as essay/source candidates with source URL and publication date preserved.

### sgoel9/paul_graham_essays

- URL: https://huggingface.co/datasets/sgoel9/paul_graham_essays
- Type: `essay_corpus`
- Platform: `huggingface`
- License observed: `MIT_claimed_on_card`
- Observed at: `2026-05-08`
- Source last updated: `2024-04-20`
- Data coverage: `unknown` to `unknown`
- Data volume: `215 essay rows (Paul Graham essay corpus.)`
- Freshness notes: Compact Paul Graham essay corpus with row-level essay dates; compare with direct paulgraham.com archive before importing text.
- Mapped people: paul-graham
- Import strategy: Import metadata/date/source URLs first; use content only with rights/attribution review.

### Interview Records

- URL: https://www.interviewrecords.com/
- Type: `public_interview_index`
- Platform: `web`
- License observed: `rights_notes_per_record`
- Observed at: `2026-05-08`
- Source last updated: `rolling_site`
- Data coverage: `unknown` to `current_bundle_when_fetched`
- Data volume: `unknown`
- Freshness notes: Public interview index advertises a data bundle; record-level date/topic/rights fields are the useful freshness signal.
- Mapped people: all-registry-people
- Import strategy: Fetch JSON bundle, import interview metadata/source URLs/transcript availability, and link people to Wikidata.

### Podcast Index

- URL: https://podcastindex.org/
- Type: `podcast_metadata_index`
- Platform: `web_api`
- License observed: `api_terms_plus_podcast_namespace_cc0`
- Observed at: `2026-05-08`
- Source last updated: `rolling_index`
- Data coverage: `unknown` to `current_api_when_queried`
- Data volume: `unknown`
- Freshness notes: Best podcast/feed discovery layer; episode pubDate and transcript/person tags should be stored per record.
- Mapped people: podcast-interview-corpus, all-registry-people
- Import strategy: Use feed/episode metadata and transcript URLs as discovery; use Podcast Index IDs as stable podcast keys.

### NASA Oral Histories

- URL: https://www.nasa.gov/history/history-publications-and-resources/oral-histories/
- Type: `official_oral_history_archive`
- Platform: `web`
- License observed: `us_government_public_domain_expected`
- Observed at: `2026-05-08`
- Source last updated: `2026-03-09`
- Data coverage: `unknown` to `current_archive_when_fetched`
- Data volume: `unknown`
- Freshness notes: Official archive; source item interview dates matter more than page update date.
- Mapped people: aerospace-science-figures, strategy-power-history-civilization
- Import strategy: Import interviewee/interviewer/date/project/transcript URL; link people to Wikidata/OpenAlex.

### NARA White House Transition Interviews

- URL: https://www.archives.gov/presidential-libraries/research/transition-interviews
- Type: `official_oral_history_transcripts`
- Platform: `web`
- License observed: `public_domain_us_government`
- Observed at: `2026-05-08`
- Source last updated: `unknown`
- Data coverage: `unknown` to `unknown`
- Data volume: `unknown`
- Freshness notes: Official public-domain oral history transcript corpus; interview dates should be captured per record.
- Mapped people: strategy-power-history-civilization, public-officials
- Import strategy: Parse interviewee/interviewer/date/administration/library/transcript text and citation.

### kani3894/nate-jones-transcripts

- URL: https://github.com/kani3894/nate-jones-transcripts
- Type: `youtube_transcript_archive`
- Platform: `github`
- License observed: `none_detected`
- Observed at: `2026-05-08`
- Source last updated: `2026-05-04T22:43:33Z`
- Data coverage: `2024-07-09` to `2026-01-13`
- Data volume: `45 Nvidia-indexed AI episodes (broader repo archive also includes OpenAI, Anthropic, DeepMind, Microsoft, Google, Meta, xAI, Claude, Gemini, GPT-5, and agents.)`
- Freshness notes: Sourcegraph found current AI transcript indexes; GitHub metadata shows recent repository activity and index pages expose per-episode dates.
- Mapped people: sam-altman, dario-amodei, jensen-huang, mark-zuckerberg, sundar-pichai, frontier-ai-leaders
- Import strategy: Import metadata and episode dates first; inspect markdown episode frontmatter/body before importing transcript text.

### willtheorangeguy Practical AI transcript datasets

- URL: https://huggingface.co/datasets/willtheorangeguy/2025-Practical-AI-Transcripts
- Type: `ai_podcast_transcript_series`
- Platform: `huggingface`
- License observed: `MIT_claimed_on_card`
- Observed at: `2026-05-08`
- Source last updated: `2026-04-17T01:44:48Z`
- Data coverage: `2018` to `2025`
- Data volume: `343 episode transcripts (Practical AI yearly Hugging Face datasets for 2018-2025; same run also exposes 343 summaries.)`
- Freshness notes: Yearly Hugging Face datasets for Practical AI were all created/updated on 2026-04-17; episode files encode year and title, but episode publish dates should be derived per file/feed.
- Mapped people: ai-researchers-technical-thinkers, frontier-ai-company-leaders, open-source-ai-leaders, ai-engineering-practitioners
- Import strategy: Import yearly dataset metadata first, then resolve guests/speakers from episode title/feed metadata before importing transcript text.

### Frontier AI web transcript pages

- URL: https://lexfridman.com/category/transcripts/
- Type: `curated_web_transcript_sources`
- Platform: `web`
- License observed: `source_specific_rights_review`
- Observed at: `2026-05-08`
- Source last updated: `rolling_sites`
- Data coverage: `2023` to `2026`
- Data volume: `unknown`
- Freshness notes: Web/search and Sourcegraph found multiple current AI interview transcript pages; each page needs its own publish date, modified date, and rights tag.
- Mapped people: dario-amodei, ilya-sutskever, jensen-huang, greg-brockman, sam-altman, demis-hassabis, frontier-ai-company-leaders
- Import strategy: Create a targeted page fetcher that records source URL, page title, publish date, transcript availability, rights notes, and person/entity matches before any text import.

### Podchaser API

- URL: https://www.podchaser.com/api
- Type: `rolling_podcast_transcript_people_index`
- Platform: `web_api`
- License observed: `api_terms`
- Observed at: `2026-05-08`
- Source last updated: `rolling_api`
- Data coverage: `unknown` to `current_api_when_queried`
- Data volume: `4M+ episode transcripts (site also advertises 5.5M+ podcasts, 27M+ host/guest/crew credits, and 20K+ Apple/Spotify charts.)`
- Freshness notes: Live commercial API with podcast, episode, credit, chart, transcript, sponsor, and audience data; store query time and episode publish dates.
- Mapped people: podcast-interview-corpus, frontier-ai-company-leaders, big-tech-platform-ceos, all-registry-people
- Import strategy: Use as a discovery and metadata layer first: people/credit lookup, episode IDs, podcast IDs, publish dates, transcript availability, and source URLs. Import transcript text only under API terms and with original-source provenance.


### spoken.md Podcast Transcript API

- URL: https://spoken.md/
- Type: `on_demand_podcast_transcript_api`
- Platform: `web_api`
- License observed: `commercial_api_terms`
- Observed at: `2026-05-08`
- Source last updated: `2026-05`
- Data coverage: `on_demand` to `current_when_requested`
- Data volume: `2,000+ transcripts fetched (public site metric; supports any podcast episode URL/search when available.)`
- Freshness notes: Current May 2026 service; best for targeted per-episode transcript fetches after discovery from Podchaser/Podcast Index/Listen Notes.
- Mapped people: podcast-interview-corpus, frontier-ai-company-leaders, founder-operators
- Import strategy: Use for paid/on-demand transcript acquisition for high-priority episodes, storing provider, episode URL, fetched_at, credits spent, speaker labels, and confidence.

## Data Volume Inventory

| Dataset | Status | Source type | Data volume | Freshness |
|---|---:|---|---:|---|
| scribesalad | p0_import_candidate | youtube_transcript_corpus | 940k+ YouTube transcripts (README claim; import selected channel/person slices only.) | 2026-04-13T21:47:38Z |
| hormozi-wiki | p1_research_candidate | creator_knowledge_base | unknown | 2026-04-05T04:59:48Z |
| hormozigpt-wombyz | p2_reference_only | creator_rag_app | unknown | 2026-05-07T22:37:52Z |
| harmozigpt-gristle18 | p1_research_candidate | creator_transcription_pipeline | unknown | 2026-05-08T04:51:45Z |
| lenny-podcast-transcripts-chatprd | p0_import_candidate | podcast_transcript_archive | 269 podcast transcripts (README claim for Lenny's Podcast.) | 2026-05-08T05:47:38Z |
| lenny-official-starter | p0_import_candidate | official_starter_pack | 60 starter records (10 newsletter posts plus 50 podcast transcripts.) | 2026-05-08T05:12:38Z |
| lex-fridman-hf-nmac | p0_import_candidate | podcast_transcript_dataset | 803k timestamped transcript entries (Lex episodes 1-325.) | 2023-01-31T16:24:07Z |
| lex-fridman-yassinetb | p1_research_candidate | lex_transcript_app_or_dataset | unknown | 2025-11-14T10:24:21Z |
| lex-fridman-hf-aditya0619 | p0_import_candidate | podcast_transcript_dataset | 441 full-episode transcripts (Hugging Face card/preview count.) | 2025-01-20T17:35:51Z |
| lex-fridman-official-transcripts | p0_import_candidate | official_transcript_pages | unknown | rolling_site |
| dwarkesh-official-pages | p0_import_candidate | official_transcript_pages | unknown | rolling_site |
| youtube-commons-pleias | p0_import_candidate | cc_by_youtube_transcript_corpus | 2M+ video transcripts (CC-BY YouTube transcript corpus.) | unknown |
| huberman-lab-transcripts | p1_research_candidate | podcast_transcript_archive | unknown | 2026-02-22T00:55:44Z |
| lawwu-transcripts | p1_research_candidate | multi_channel_transcript_archive | unknown | 2026-04-11T13:24:00Z |
| tapesearch-alex-hormozi | p1_research_candidate | podcast_transcript_search_index | unknown | rolling_index |
| sozai-alex-hormozi-transcripts | p1_research_candidate | web_transcript_archive | unknown | unknown |
| quote-datasets-wikiquote | p1_research_candidate | quote_corpus | unknown | rolling_wikimedia |
| wikidata-official-dumps | p0_import_candidate | identity_knowledge_graph | unknown | rolling_wikimedia_dumps |
| quotekg | p0_import_candidate | quote_knowledge_graph | 1M quotes; 70K persons | unknown |
| project-gutenberg-catalog | p0_import_candidate | public_domain_book_catalog | unknown | rolling_catalog |
| sporc | p1_research_candidate | podcast_transcript_research_corpus | 1.1M+ podcast episodes (transcripts plus metadata and inferred host/guest roles.) | unknown |
| mediasum | p1_research_candidate | media_interview_transcript_corpus | 463K+ interview transcripts (NPR/CNN interview transcript research corpus.) | unknown |
| naval-style-eval-corpus | p0_import_candidate | author_style_text_dataset | 52 Naval pieces (about 46K words from navalmanack.com.) | unknown |
| naval-gpt-mckaywrigley | p1_research_candidate | creator_rag_app | unknown | 2026-04-16T08:01:07Z |
| naval-skill-alchaincyf | p1_research_candidate | distilled_person_skill | unknown | 2026-05-08T07:23:13Z |
| naval-almanack-hf-harshalmore31 | p1_research_candidate | book_text_dataset | unknown | 2025-03-16T01:26:06Z |
| hormozi-brain-claude-project | p1_research_candidate | distilled_creator_project | unknown | 2026-05-05T19:30:43Z |
| founder-playbook | p1_research_candidate | distilled_business_book_skills | unknown | 2026-05-08T00:02:42Z |
| nuwa-skill | p2_reference_only | person_distillation_toolkit | unknown | 2026-05-08T09:06:39Z |
| readyai-podcast-conversations | p1_research_candidate | podcast_conversation_dataset | 11,888 rows (search result says 5,000 podcast conversations.) | 2025-06-19 |
| beliefengines-podcast-transcripts | p0_import_candidate | podcast_belief_quote_graph_dataset | 556 rows (includes persons, beliefs, quotes, transcript chunks, embeddings, and episode metadata.) | 2026-04-21 |
| kurry-sp500-earnings-transcripts | p0_import_candidate | earnings_call_transcript_corpus | 33,362 rows (S&P 500 earnings-call transcripts.) | 2025-05-21 |
| sgoel9-sam-altman-essays | p0_import_candidate | essay_corpus | 112 essay rows (Sam Altman blog essay corpus.) | 2024-04-20 |
| sgoel9-paul-graham-essays | p0_import_candidate | essay_corpus | 215 essay rows (Paul Graham essay corpus.) | 2024-04-20 |
| jan-hq-youtube-transcripts-raw | p1_research_candidate | ai_tech_youtube_transcript_chunks | 244 transcript rows (small AI tech YouTube transcript seed.) | 2024-03-13 |
| rchiera-podcast-transcripts | p1_research_candidate | podcast_transcript_corpus | 52,334 rows (podcast transcripts with episode metadata and speaker slugs.) | 2026-02-13 |
| interview-records | p0_import_candidate | public_interview_index | unknown | rolling_site |
| podcast-index | p0_import_candidate | podcast_metadata_index | unknown | rolling_index |
| nasa-oral-histories | p0_import_candidate | official_oral_history_archive | unknown | 2026-03-09 |
| nara-transition-interviews | p0_import_candidate | official_oral_history_transcripts | unknown | unknown |
| bigscience-roots-en-wikiquote | p1_research_candidate | wikiquote_dump_dataset | unknown | 2022-12-12T11:03:08Z |
| lennyhub-rag | p1_research_candidate | transcript_rag_knowledge_graph_app | 297 transcript files (Lenny Podcast transcript RAG corpus.) | 2026-05-04T00:09:15Z |
| nate-jones-transcripts | p0_import_candidate | youtube_transcript_archive | 45 Nvidia-indexed AI episodes (broader repo archive also includes OpenAI, Anthropic, DeepMind, Microsoft, Google, Meta, xAI, Claude, Gemini, GPT-5, and agents.) | 2026-05-04T22:43:33Z |
| practical-ai-transcripts-willtheorangeguy | p0_import_candidate | ai_podcast_transcript_series | 343 episode transcripts (Practical AI yearly Hugging Face datasets for 2018-2025; same run also exposes 343 summaries.) | 2026-04-17T01:44:48Z |
| k-dense-mimeo-ai-researcher-skills | p1_research_candidate | ai_researcher_source_maps_and_agent_skills | 20 AI researcher source-map folders (source maps for major AI researchers and leaders.) | 2026-05-08T04:29:15Z |
| filipwx-ted-podcast-finetune | p1_research_candidate | mixed_ted_lex_joe_rogan_transcript_finetune_dataset | unknown | 2026-04-05T16:56:55Z |
| ai-frontier-web-transcript-pages | p0_import_candidate | curated_web_transcript_sources | unknown | rolling_sites |
| earnings-calls-nlp-cdubiel08 | p1_research_candidate | earnings_call_transcript_archive | unknown | 2026-04-21T03:51:08Z |
| navalmanac-chatbot-docstore | p1_research_candidate | person_rag_docstore | unknown | 2026-04-16T08:00:56Z |
| podchaser-api | p0_import_candidate | rolling_podcast_transcript_people_index | 4M+ episode transcripts (site also advertises 5.5M+ podcasts, 27M+ host/guest/crew credits, and 20K+ Apple/Spotify charts.) | rolling_api |
| podscan-api | p1_research_candidate | rolling_podcast_transcript_search_api | 46M+ episodes (help page says 4M+ podcasts with full transcripts, entities, demographics, and real-time updates.) | rolling_api |
| listen-notes-api | p1_research_candidate | rolling_podcast_metadata_search_api | 3.7M+ podcasts (third-party source directory reports 192M+ episodes; verify exact live counts during API onboarding.) | rolling_api |
| taddy-podcast-api | p1_research_candidate | rolling_podcast_metadata_transcript_api | 200M+ episodes (developer page advertises 4M+ podcasts, episode transcripts, search, and real-time webhooks.) | rolling_api |
| spoken-md-transcript-api | p0_import_candidate | on_demand_podcast_transcript_api | 2,000+ transcripts fetched (public site metric; supports any podcast episode URL/search when available.) | 2026-05 |
| ceointerviews-ai-api | p1_research_candidate | executive_interview_quote_transcript_database | 20,000+ CEOs/executives (Sourcegraph/web docs also describe 1M+ verified quotes and full transcripts.) | rolling_api |
| tapesearch-podcast-transcript-search | p1_research_candidate | rolling_podcast_transcript_search_index | 4M+ podcast episodes (third-party directory/search result; terms explicitly prohibit harvesting to replicate the database.) | rolling_index |
| podafi-podcast-transcript-directory | p1_research_candidate | rolling_podcast_transcript_directory | 1,159 transcripts (prior search snapshot also showed 198 podcasts and 18 categories; site advertises daily chart updates.) | rolling_site |
| podgist-transcript-library | p1_research_candidate | rolling_podcast_transcript_summary_library | thousands shows and episodes (public page claim; exact count needs catalog/API inspection.) | rolling_site |
| sumbest-ai-podcast-library | p1_research_candidate | rolling_ai_podcast_transcript_library | 25 ready catalog episodes (visible search snapshot across 20VC, Lenny, All-In, Dwarkesh, No Priors, and related shows; user-added feeds can expand it.) | rolling_site |
| bob-proctor-public-corpus-gap | blocked | gap_marker | unknown | not_applicable |

## Gaps

- `bob-proctor-public-corpus-gap`: Subagent did not find a clean GitHub/Hugging Face Bob Proctor transcript dataset.
