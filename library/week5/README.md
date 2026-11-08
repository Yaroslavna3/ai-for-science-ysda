# Week 5 literature corpus

The corpus contains 31 OpenAlex records with abstracts, selected from the 54 DOI
references in `../simonenko_et_al_2022_co3o4.pdf`. One JSONL record is one search
document: title plus abstract. These are not full-text PDFs.

- `corpus.jsonl`: searchable records with DOI, OpenAlex ID, source reference number,
  title, abstract, author list, year, and citation count.
- `provenance.json`: source and retrieval method/date.
- `pdf_availability.csv`: DOI-by-DOI match, OpenAlex OA flag, and local PDF status.
- `pdfs/`: verified, openly licensed PDF copies actually available locally.
- `pdf_sources.md`: attribution and license notes for local PDFs.

OpenAlex had a title/abstract for 31 of the 54 DOI records on 2026-10-23. Missing
abstracts were not reconstructed or invented. The OA flag is metadata, not a guarantee
that a direct download will succeed; consult the availability table before assuming a
local copy exists.
