# Marcus Aurelius Source Plan

- Slug: `marcus-aurelius`
- Status: `approved`
- Tier: `S`
- Collection mode: `corpus-first`
- Source strategy: `corpus`
- Next source action: `collect_corpus_sources`

## Source Targets

- `Project Gutenberg / canonical_text` Meditations
  - URL: https://www.gutenberg.org/ebooks/2680
  - Rights: `public_domain_source`
  - Notes: Public-domain translation suitable for full-text ingestion.
- `Wikisource / translation_index` Meditations translation index
  - URL: https://en.wikisource.org/wiki/Meditations
  - Rights: `translation_rights_review`
  - Notes: Pick a public-domain translation before ingestion; preserve translator metadata.
- `Project Gutenberg / archive_search` Marcus Aurelius source search
  - URL: https://www.gutenberg.org/ebooks/search/?query=Marcus+Aurelius
  - Rights: `public_domain_or_translation_review`
  - Notes: Discovery target; select item-level texts and preserve edition/translator metadata.
- `Wikisource / archive_search` Marcus Aurelius source search
  - URL: https://en.wikisource.org/w/index.php?search=Marcus+Aurelius
  - Rights: `public_domain_or_translation_review`
  - Notes: Discovery target; select item-level texts and preserve edition/translator metadata.
- `Internet Archive / archive_search` Marcus Aurelius source search
  - URL: https://archive.org/search?query=Marcus+Aurelius
  - Rights: `public_domain_or_translation_review`
  - Notes: Discovery target; select item-level texts and preserve edition/translator metadata.
- `Open Library / archive_search` Marcus Aurelius source search
  - URL: https://openlibrary.org/search?q=Marcus+Aurelius
  - Rights: `public_domain_or_translation_review`
  - Notes: Discovery target; select item-level texts and preserve edition/translator metadata.
- `Perseus / archive_search` Marcus Aurelius source search
  - URL: https://www.perseus.tufts.edu/hopper/searchresults?q=Marcus+Aurelius
  - Rights: `public_domain_or_translation_review`
  - Notes: Discovery target; select item-level texts and preserve edition/translator metadata.

## Discovery URLs

- https://www.gutenberg.org/ebooks/search/?query=Marcus+Aurelius
- https://en.wikisource.org/w/index.php?search=Marcus+Aurelius
- https://archive.org/search?query=Marcus+Aurelius
- https://openlibrary.org/search?q=Marcus+Aurelius
- https://www.perseus.tufts.edu/hopper/searchresults?q=Marcus+Aurelius
