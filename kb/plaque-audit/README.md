# Plaque transcription audit (p_291)

One JSONL record per image in `assets/images/plaques/` (151 files).

Fields:
- `image`     filename
- `fact_id`   the KB fact that cites it, or null if none found
- `verdict`   COMPLETE | PARTIAL | UNREAD | NO-NAMES | ILLEGIBLE
- `recorded`  how many names the existing fact carried
- `actual`    how many the plaque carries
- `names`     full transcription where one was made
- `low_conf`  readings held at reduced confidence
- `note`      anything the verdict alone does not carry

Verdicts describe THE FACT, not the plaque: PARTIAL means the fact
under-records what the image shows.

Method note, carried from the errors that produced this task: record what
the paint says and what a person says in separate fields, and never let
either overwrite the other. Alphabetical ordering on these plaques is a
tendency, not a rule -- late additions are appended out of sequence at the
foot of a column. Ordering may suggest a reading of a faint name; it must
not be used to exclude one.
