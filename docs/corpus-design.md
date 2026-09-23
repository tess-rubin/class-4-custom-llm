# Extension teaching material

The user selected **opposites and negation** before training. These are original,
AI-assisted teaching sentences composed for this assignment, using invented
people and ordinary situations. They are not quotations from books, web pages,
personal records, or the evaluation suite. They may be shared with the project.
The student's independent authorship or understanding is not being claimed.

- `corpus/expanded/opposites.txt`: 120 distinct passages, eight contextual
  examples for each of 15 contrasts: hot/cold, empty/full, noisy/quiet,
  heavy/light, fast/slow, soft/hard, wet/dry, clean/dirty, long/short,
  high/low, wide/narrow, early/late, bright/dim, smooth/rough, near/far.
- `corpus/expanded/negation.txt`: 120 distinct passages using not, no, never,
  instead, rather than, refusal, absence, and unchanged states in school,
  travel, food, household, healthcare, and workplace situations.

Opposites are taught through contrasting properties in context, rather than
copied test prefixes followed by their answers. Negation is taught through
explicit events and alternatives rather than renamed versions of the test
stories. These patterns are absent from the narrow starter templates. Teaching
them is a plausible experiment, not a promise that the model will learn the
suite's wording or have every word required to score its cases.

Each line is one sentence so the supplied sentence-based loader keeps its
contrast together. Semicolons and conjunctions connect negation and its
consequence without splitting them into separate documents. Every passage has
at most 19 word/punctuation tokens, below the 47-token limit.

Before training, incidental vocabulary was simplified while retaining the
240 distinct examples. This was based on the corpus's vocabulary size, not
measured evaluation scores or insertion of test-only words. A final typo was
corrected before the first expanded run. The final source text, extraction
counts, hashes, and vocabulary are preserved in the artifacts; no post-score
corpus tuning is part of this experiment.

The fixed tests were read for separation review. All 240 teaching passages and
all 48 test cases were reviewed for copied stories, close story paraphrases,
answer lists, and reserved prefixes. No such copies were identified. Ordinary
words and underlying facts such as hot/cold necessarily overlap. The supplied
normalized-prefix guard also finds no exact prompt matches. This check is not
a semantic proof, so the sources are published for inspection.

Only these two UTF-8 text files enter the expanded import folder. This document,
the eval suite, generated responses, result files, and learning notes remain
outside the corpus. There are no PDFs or OCR claims; the loader reports no
extraction warnings. The starter import folder remains empty.
