# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

All three work on 300-word chunks with 50 words of overlap (`p2.toml`), and a document scores its best chunk.

- `dense` embeds every chunk with bge-small-en-v1.5 and scores it by cosine similarity with the embedded query (a dot product, since the vectors have length 1).
  The model is set in `[dense] model` in `p2.toml`, defaulting to bge-small; I did not try potion-retrieval-32M.
- `hybrid` is reciprocal rank fusion of `bm25` and `dense` with k = 60, so a document scores the sum of 1/(60 + rank) over the two rankings.
  I fuse the full rankings of all 2,484 documents and not the top 10, so a document that is 11th in both can still reach the top 10.
- `rerank` takes `hybrid`'s top 20 documents and makes one `claude -p` call per query (Sonnet), showing them as numbered passages cut to 200 words.
  The reply is forced into an order of the numbers 1 to 20 (each between 1 and 20), and a reply that is not each number once keeps `hybrid`'s order.
  The documents below the top 20 keep their `hybrid` order underneath.
  For `p2 answer` it does the same over `hybrid`'s top 20 chunks.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.443 |
| rerank | 0.758 | 0.800 | 0.759 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.152 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.202 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.714 | 0.626 | 0.966 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.037 | [-0.178, +0.083] | 0.192 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.092 | [-0.306, +0.109] | 0.301 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.200, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.100, +0.358] | 0.340 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.043, +0.533] | 0.353 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.241 | [+0.014, +0.459] | 0.323 | rerank higher |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.367] | 0.224 | rerank higher |
| rerank minus dense | MRR@10 | +0.237 | [+0.083, +0.408] | 0.239 | rerank higher |
| rerank minus dense | nDCG@10 | +0.279 | [+0.141, +0.434] | 0.214 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | 0.166 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | 0.247 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.316 | [+0.189, +0.445] | 0.185 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

**What is distinguishable.**
`rerank` is higher than all three other systems on MRR@10 and nDCG@10, and its interval excludes zero each time: +0.293 [+0.043, +0.533] over `bm25` on MRR@10, +0.237 [+0.083, +0.408] over `dense`, and +0.329 [+0.164, +0.504] over `hybrid`.
Its recall@10 is distinguishable from `dense` and `hybrid` but not from `bm25` (+0.133 [-0.100, +0.358]).
Among `bm25`, `dense` and `hybrid`, no difference is distinguishable on any of the three scores.

**What 20 queries cannot see.**
The minimum detectable difference on MRR@10 runs from 0.19 to 0.41 depending on the pair.
The gap of `rerank` over `bm25` (+0.293) is below its MDD of 0.353, so that result is real on this gold set but fragile: its interval's lower end is only +0.043.
The gaps among `bm25`, `dense` and `hybrid` (0.04 to 0.09 on MRR@10) are far below their MDDs, so they are invisible here, not absent.
I cannot say `dense` and `bm25` are equal, only that 20 queries cannot separate them.

**By class.**
Seven queries per class is too few for an interval, so I read these only as a pattern.
`bm25` finds all seven identifier queries' answers (recall@10 1.000) and none of the seven paraphrase ones (0.000).
`dense` is the reverse: 0.214 on identifiers and 0.595 on paraphrases.
That supports the claim that no one retriever wins everywhere, but on 7 queries per class.

**`hybrid` did not help.**
I expected fusion to take the better of the two, and it came in below both on MRR@10 (0.471, against 0.507 for `bm25` and 0.562 for `dense`), though not distinguishably.
By class it is in between: identifiers 0.514 against `bm25`'s 0.810, paraphrases 0.152 against `dense`'s 0.714.
My first guess was that `bm25`'s zero-score padding (documents with no query word, ranked by id) added noise to the fusion.
I tested that by dropping the zero-score documents from `bm25`'s ranking before fusing, and the MRR@10 stayed at 0.471, so that was not the cause.
My remaining guess is that fusing with equal weights lets the weak system's ranking pull a strong system's answer down, but I did not test it.

**What stays open.**
`rerank` is one run of a nondeterministic step, so I cannot yet say whether its gain survives run-to-run variation; section 9 is for that.
The 40 test queries are scored by the course, and nothing here claims anything about them.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 11 of 11 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

**Which system and prompt.**
`rerank` answered, because it was the best system on the practice queries (MRR@10 0.800) and so gave Claude the best five chunks to cite.
It costs two Claude calls per question, one to rerank and one to answer.
I did not change `prompts/answer.txt`, so I have no before-and-after for the verified or declined share.
The result is 8 of 8 in-corpus questions verified and 4 of 4 unanswerable ones declined, with Wilson intervals of [0.676, 1.000] and [0.510, 1.000]: the best the data can show is still wide at these counts.

**Three-answer audit** (I opened each cited chunk in `corpora/shared/docs/`).

- **a01, minutes to notify MSHA after a fatal accident.**
  The answer says 15 minutes, and the quote from `cfr30-50.10#0` says to call "within 15 minutes ... once the operator knows or should know that an accident has occurred involving:".
  The sentence ends in a colon, and item (a), "A death of an individual at the mine", is the next line in the document and is not in the quote.
  So the quote supports the 15 minutes, and the death condition the claim states comes from the line after it.
  The claim is correct, but the quote alone does not carry all of it.
- **a02, minimum incombustible content of the dust.**
  Claim one says 80 percent, and its quote says "not less than 80 percent", so it is supported.
  Claim two says the percentage is increased "only" where methane is present, and its quote says that where methane is present the percentage "shall be increased 0.4 percent for each 0.1 percent of methane".
  The quote supports the increase with methane, but it does not say "only"; that word is the model's inference from the 80 percent baseline.
  This is a small overreach that the verifier passed, because it checks that the quote is real and cannot check that the claim says no more than the quote.
- **a03, how long a self-rescue device must protect a miner.**
  The claim says each miner who goes underground must be given a device adequate for 1 hour or longer.
  `cfr30-75.1714#0` says "(a) Each operator shall make available to each miner who goes underground ... an approved self-rescue device or devices which is adequate to protect such person for 1 hour or longer.", so it is fully supported.

- **a04, evacuation drill frequency.**
  Both claims are supported: "At least once every six months, mine evacuation drills shall be held" and "Be held for each shift at some time other than a shift change and involve all persons underground" are both in `cfr30-57.4361#0`.
- **a05, hours of training for a new underground miner.**
  The quote, "no less than 40 hours of training ... before such miner is assigned to work duties", is real and supports the 40 hours.
  The claim goes past the quote by adding that training is conducted in conditions that duplicate actual underground conditions, which is the next sentence of 48.5(a) and is not in the quote.
  The answer text also says section 48.25 sets 24 hours with at least 8 before assignment, and hedges that the chunks do not say who it covers.
  That 48.25 statement has no claim or quote behind it, so the verifier never checked it.
- **a06, noise permissible exposure level.**
  Supported: the quote is the definition "A TWA8 of 90 dBA or equivalently a dose of 100% of that permitted by the standard", from `cfr30-62.101#1`.
- **a07, berm or guardrail height.**
  Both claims are supported, and the two quotes are word for word the same sentence from `cfr30-56.9300#0` and `cfr30-57.9300#0`.
  That fits the brief's point that the same rule is written once for each part, and it means the two claims are two true citations of one rule and not two independent findings.
- **a08, hours of breathable air in a refuge alternative.**
  Supported: "The breathable air sustains each person for 96 hours" is in `cfr30-7.506#0`.
  The answer text adds in parentheses that under 75.1507 the stocking requirement can be met for 48 hours with advance arrangements.
  That is in the retrieved `cfr30-75.1507` chunks, but it concerns food and water in paragraph (d)(1) and not breathable air, and it has no claim or quote behind it.

**What the audit shows.**
I read all 11 claims of the eight in-corpus answers against their chunks.
All 11 quotes are real, and 8 of the 11 claims are fully supported by their quotes.
Three claims say a little more than their quote: a01 (the death condition is on the next line), a02 (the word "only") and a05 (the underground-conditions clause).
In none of them is the core number wrong.
Separately, two answers (a05 and a08) put extra statements in the answer text with no claim or quote behind them, so the verifier never checks that text.
"8 of 8 verified" is therefore accurate about the quotes, and it overstates how closely every sentence of every answer is checked.
For the four declined questions I checked only that `not_found` was set, and not that the chunks really lacked an answer.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

My corpus is 220 English Wikipedia articles about Counter-Strike: players, teams, tournaments (including the Majors), maps and the games themselves.
I took the category tree under Counter-Strike and its players, teams and competitions categories (two levels of subcategories) with `scripts/fetch_wikipedia.py`, which fetches each article as plain text through the MediaWiki API and drops sections with no prose, such as References.
It is about 269,000 words (about 377,000 estimated tokens) and about 1.7 MB.
It comes from the allowed source "CC0, CC BY and CC BY-SA text, including Wikipedia": the license is CC BY-SA 4.0, and each page's footer says "Text is available under the Creative Commons Attribution-ShareAlike 4.0 License; additional terms may apply."
The manifest records each page's address and revision for attribution.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

The gold set has 40 queries: 10 with origin `hand` (q11 to q20) and 30 with origin `claude` (the rest).
I used the same three classes as the shared sets, `identifier` (8 queries), `mixed` (16) and `paraphrase` (16), so the per-class scores can be compared across the two corpora.

**Relevance rule.**
A page is relevant to a query if its text states the answer the query asks for.
A page that only mentions the person, team or event without giving that answer is not relevant, and neither is one that merely sounds related.
When several pages each state the answer, such as a player's page and the event page where they won, all of them are relevant.
For a query like "what is X", the page about X is the relevant one.
Labels are binary (`rel` 1), and I decided each one after reading the page, not from the system that returned it.

For each query I took candidates from the top results of `bm25`, `dense` and `hybrid` plus a keyword search for the phrases I expected, so no one system decided what was in the pool.
Claude Code listed the candidates with a snippet from each page, and I decided relevance myself, opening the pages, and added pages I thought of that the systems had not returned.
The pool did not include `rerank`, so a relevant page that none of those four found is missing from the answer key.

I read every candidate page before labeling it.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.852 | 0.723 | 0.718 |
| dense | 0.854 | 0.849 | 0.777 |
| hybrid | 0.931 | 0.858 | 0.830 |
| rerank | 0.938 | 0.911 | 0.874 |
| ablation/rerank_long | 0.946 | 0.950 | 0.906 |

40 judged queries; nDCG uses binary labels; a random ranking of the 220 documents would get recall@10 near 0.045.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | mixed (n=17) | identifier (n=8) | paraphrase (n=15) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 0.877 | 0.958 | 0.767 |
| bm25 | MRR@10 | 0.779 | 0.838 | 0.599 |
| bm25 | nDCG@10 | 0.752 | 0.865 | 0.601 |
| dense | Recall@10 | 0.892 | 0.917 | 0.778 |
| dense | MRR@10 | 0.850 | 1.000 | 0.769 |
| dense | nDCG@10 | 0.789 | 0.930 | 0.683 |
| hybrid | Recall@10 | 0.936 | 0.917 | 0.933 |
| hybrid | MRR@10 | 0.892 | 1.000 | 0.744 |
| hybrid | nDCG@10 | 0.862 | 0.930 | 0.742 |
| rerank | Recall@10 | 0.971 | 0.875 | 0.933 |
| rerank | MRR@10 | 0.875 | 1.000 | 0.906 |
| rerank | nDCG@10 | 0.881 | 0.868 | 0.871 |
| ablation/rerank_long | Recall@10 | 0.971 | 0.917 | 0.933 |
| ablation/rerank_long | MRR@10 | 0.951 | 1.000 | 0.922 |
| ablation/rerank_long | nDCG@10 | 0.920 | 0.918 | 0.882 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=30) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.875 | 0.844 | +0.031 | [-0.206, +0.217] | not distinguishable |
| bm25 | MRR@10 | 0.800 | 0.698 | +0.102 | [-0.154, +0.327] | not distinguishable |
| bm25 | nDCG@10 | 0.757 | 0.705 | +0.052 | [-0.176, +0.253] | not distinguishable |
| dense | Recall@10 | 0.800 | 0.872 | -0.072 | [-0.250, +0.106] | not distinguishable |
| dense | MRR@10 | 0.950 | 0.816 | +0.134 | [-0.022, +0.285] | not distinguishable |
| dense | nDCG@10 | 0.808 | 0.767 | +0.040 | [-0.133, +0.212] | not distinguishable |
| hybrid | Recall@10 | 0.875 | 0.950 | -0.075 | [-0.217, +0.047] | not distinguishable |
| hybrid | MRR@10 | 0.850 | 0.861 | -0.011 | [-0.237, +0.182] | not distinguishable |
| hybrid | nDCG@10 | 0.820 | 0.834 | -0.014 | [-0.209, +0.156] | not distinguishable |
| rerank | Recall@10 | 0.867 | 0.961 | -0.094 | [-0.239, +0.033] | not distinguishable |
| rerank | MRR@10 | 0.925 | 0.907 | +0.018 | [-0.158, +0.160] | not distinguishable |
| rerank | nDCG@10 | 0.846 | 0.884 | -0.037 | [-0.219, +0.117] | not distinguishable |
| ablation/rerank_long | Recall@10 | 0.900 | 0.961 | -0.061 | [-0.206, +0.056] | not distinguishable |
| ablation/rerank_long | MRR@10 | 0.950 | 0.950 | +0.000 | [-0.128, +0.106] | not distinguishable |
| ablation/rerank_long | nDCG@10 | 0.875 | 0.916 | -0.040 | [-0.191, +0.085] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.028 | +0.075 | -0.103 | [-0.306, +0.106] | not distinguishable |
| MRR@10 | -0.118 | -0.150 | +0.032 | [-0.234, +0.320] | not distinguishable |
| nDCG@10 | -0.062 | -0.050 | -0.012 | [-0.220, +0.209] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.93 (10 queries), claude 0.89 (30 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 30 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.002 | [-0.096, +0.100] | 0.142 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.126 | [+0.012, +0.244] | 0.166 | dense higher |
| dense minus bm25 | nDCG@10 | +0.059 | [-0.036, +0.157] | 0.138 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.079 | [-0.004, +0.175] | 0.129 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.135 | [+0.041, +0.233] | 0.138 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.112 | [+0.040, +0.187] | 0.105 | hybrid higher |
| hybrid minus dense | Recall@10 | +0.077 | [+0.015, +0.156] | 0.105 | hybrid higher |
| hybrid minus dense | MRR@10 | +0.009 | [-0.061, +0.071] | 0.096 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.053 | [+0.007, +0.103] | 0.070 | hybrid higher |
| rerank minus bm25 | Recall@10 | +0.085 | [+0.002, +0.181] | 0.130 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.188 | [+0.069, +0.309] | 0.173 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.156 | [+0.052, +0.263] | 0.153 | rerank higher |
| rerank minus dense | Recall@10 | +0.083 | [+0.013, +0.167] | 0.113 | rerank higher |
| rerank minus dense | MRR@10 | +0.062 | [-0.046, +0.175] | 0.162 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.097 | [+0.004, +0.193] | 0.137 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.006 | [-0.019, +0.033] | 0.038 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.053 | [-0.046, +0.153] | 0.145 | not distinguishable |
| rerank minus hybrid | nDCG@10 | +0.044 | [-0.033, +0.123] | 0.112 | not distinguishable |
| ablation/rerank_long minus bm25 | Recall@10 | +0.094 | [+0.013, +0.188] | 0.127 | ablation/rerank_long higher |
| ablation/rerank_long minus bm25 | MRR@10 | +0.227 | [+0.114, +0.342] | 0.166 | ablation/rerank_long higher |
| ablation/rerank_long minus bm25 | nDCG@10 | +0.188 | [+0.088, +0.288] | 0.144 | ablation/rerank_long higher |
| ablation/rerank_long minus dense | Recall@10 | +0.092 | [+0.025, +0.175] | 0.110 | ablation/rerank_long higher |
| ablation/rerank_long minus dense | MRR@10 | +0.101 | [+0.013, +0.198] | 0.135 | ablation/rerank_long higher |
| ablation/rerank_long minus dense | nDCG@10 | +0.128 | [+0.050, +0.214] | 0.120 | ablation/rerank_long higher |
| ablation/rerank_long minus hybrid | Recall@10 | +0.015 | [+0.000, +0.037] | 0.029 | not distinguishable |
| ablation/rerank_long minus hybrid | MRR@10 | +0.092 | [+0.006, +0.181] | 0.128 | ablation/rerank_long higher |
| ablation/rerank_long minus hybrid | nDCG@10 | +0.075 | [+0.007, +0.144] | 0.099 | ablation/rerank_long higher |
| ablation/rerank_long minus rerank | Recall@10 | +0.008 | [+0.000, +0.025] | 0.023 | not distinguishable |
| ablation/rerank_long minus rerank | MRR@10 | +0.039 | [-0.004, +0.096] | 0.075 | not distinguishable |
| ablation/rerank_long minus rerank | nDCG@10 | +0.031 | [-0.004, +0.074] | 0.056 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

**What is distinguishable (40 queries).**
`rerank` is higher than `bm25` on both scores: MRR@10 +0.188 [+0.069, +0.309] and nDCG@10 +0.156 [+0.052, +0.263].
`hybrid` is higher than `bm25` on both as well (MRR@10 +0.135 [+0.041, +0.233], nDCG@10 +0.112 [+0.040, +0.187]).
`dense` is higher than `bm25` on MRR@10 (+0.126 [+0.012, +0.244]) but not on nDCG@10 (+0.059 [-0.036, +0.157]).
`hybrid` is higher than `dense` on nDCG@10 (+0.053 [+0.007, +0.103]) and not on MRR@10, and `rerank` is higher than `dense` on nDCG@10 (+0.097 [+0.004, +0.193]) and not on MRR@10.
`rerank` against `hybrid` is not distinguishable on any score (nDCG@10 +0.044 [-0.033, +0.123]), which is the pair I pre-registered.

**What 40 queries cannot see.**
The minimum detectable difference runs from 0.07 to 0.17 depending on the pair and the score, so a gap smaller than that is invisible here and not absent.
Several of these intervals have a lower end close to zero (for example 0.004 for `rerank` against `dense` on nDCG@10), so I would treat them as weak evidence.
All four systems score high (recall@10 from 0.85 to 0.94), so there is not much room left to separate them.

**Hand and claude queries.**
All twelve hand-minus-claude rows include zero, with only 10 hand queries, so I cannot say the two groups behave alike, only that this gold set cannot tell them apart.
The queries' content-word overlap with their best relevant page was 0.93 for hand and 0.89 for claude, so the model's queries did not copy page words much more than mine.

**My prediction.**
I expected `rerank` to win and `bm25` to do worst.
`rerank` has the highest mean on every score and `bm25` the lowest, but `rerank`'s lead over `hybrid` and `dense` is not distinguishable, so only the "`bm25` is worse" half is supported by an interval.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/rerank_long minus bm25 | Recall@10 | +0.094 | [+0.013, +0.188] | 0.127 | ablation/rerank_long higher |
| ablation/rerank_long minus bm25 | MRR@10 | +0.227 | [+0.114, +0.342] | 0.166 | ablation/rerank_long higher |
| ablation/rerank_long minus bm25 | nDCG@10 | +0.188 | [+0.088, +0.288] | 0.144 | ablation/rerank_long higher |
| ablation/rerank_long minus dense | Recall@10 | +0.092 | [+0.025, +0.175] | 0.110 | ablation/rerank_long higher |
| ablation/rerank_long minus dense | MRR@10 | +0.101 | [+0.013, +0.198] | 0.135 | ablation/rerank_long higher |
| ablation/rerank_long minus dense | nDCG@10 | +0.128 | [+0.050, +0.214] | 0.120 | ablation/rerank_long higher |
| ablation/rerank_long minus hybrid | Recall@10 | +0.015 | [+0.000, +0.037] | 0.029 | not distinguishable |
| ablation/rerank_long minus hybrid | MRR@10 | +0.092 | [+0.006, +0.181] | 0.128 | ablation/rerank_long higher |
| ablation/rerank_long minus hybrid | nDCG@10 | +0.075 | [+0.007, +0.144] | 0.099 | ablation/rerank_long higher |
| ablation/rerank_long minus rerank | Recall@10 | +0.008 | [+0.000, +0.025] | 0.023 | not distinguishable |
| ablation/rerank_long minus rerank | MRR@10 | +0.039 | [-0.004, +0.096] | 0.075 | not distinguishable |
| ablation/rerank_long minus rerank | nDCG@10 | +0.031 | [-0.004, +0.074] | 0.056 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/rerank_long against rerank (BASE = "rerank" in p2/retrievers/rerank_long.py): it helped 3 queries, hurt 1 and left 36 unchanged.

| Query | Class | Origin | rerank RR | ablation/rerank_long RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| q07 | mixed | claude | 0.200 | 1.000 | +0.800 | helped |
| q01 | mixed | claude | 0.333 | 1.000 | +0.667 | helped |
| q19 | paraphrase | hand | 0.250 | 0.500 | +0.250 | helped |
| q35 | mixed | claude | 0.333 | 0.167 | -0.167 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

**The one change:** the reranker (`rerank`) shows Claude the first 600 words of each of the 20 candidate pages instead of the first 200; the variant is `p2/retrievers/rerank_long.py` and everything else is the same.

**Hypothesis:** I expect showing 600 words instead of 200 to raise `rerank`'s nDCG@10 on my corpus, because in several queries it ranked badly (q07, q01 and q19) the sentence that answers the question comes after the first 200 words of the relevant page.

**Result.**
With 600 words per passage `rerank_long` scored nDCG@10 0.906, MRR@10 0.950 and recall@10 0.946, against 0.874, 0.911 and 0.938 for `rerank`.
Against `rerank` the nDCG@10 difference is +0.031 [-0.004, +0.074] and the MRR@10 difference is +0.039 [-0.004, +0.096]; both intervals include zero, so the difference is not distinguishable on this gold set.
The minimum detectable difference for nDCG@10 was 0.056, so a gain smaller than about 0.06 would not show.
It cost about 26,100 input tokens per query against about 10,400 for `rerank`, roughly 2.5 times as many, at 4.6 seconds per query.

**The queries.**
It helped 3 queries, hurt 1 and left 36 unchanged.
The three it helped are the ones named in my hypothesis: q07 (reciprocal rank 0.20 to 1.00), q01 (0.33 to 1.00) and q19 (0.25 to 0.50), so for those queries the answer sentence being past word 200 does explain the failure.
It hurt q35 (0.33 to 0.17): its first result was `esl-one-cologne-2016`, which says "Gambit Esports from Kazakhstan won the title", and my labels do not count that page, so this drop may be a gap in my labels and not a ranking error.

**Claim.**
Showing the reranker more of each page fixed the three queries I predicted it would, but over the whole gold set the gain is not distinguishable from zero, so I cannot claim that 600 words is better than 200 overall; I can only claim it for those three queries.
`rerank_long` is higher than `hybrid` and `dense` on nDCG@10 with intervals that exclude zero (+0.075 [+0.007, +0.144] and +0.128 [+0.050, +0.214]), which `rerank` was not for `hybrid` (+0.044 [-0.033, +0.123]), but I did not pre-register that comparison, so I treat it as a lead and not a result.
What I would try next is giving the reranker the best-matching chunk of each page instead of its opening words, which should keep the answer sentence in view at a lower cost than 600 words.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| q07 | `luminosity-gaming`, `esl-one-cologne-2016`, `counter-strike-major-championships` (`hybrid` had `eleague-major-boston-2018` first) | `eleague-major-boston-2018` (rank 5), `cloud9` (not in the top 10) | the answer sentence is at word 362 of a 3,275-word page and the reranker saw only the first 200 words; `cloud9` never reached the first stage's top 20 | show the reranker more of each page, or its best-matching chunk |
| q19 | `esl-one-cologne-2014`, `esl-one-cologne-2016`, `pgl-major-krak-w-2017` | `counter-strike-major-championships` (rank 4), `esl-one-katowice-2015` (not in the top 10) | the query names no team, so near-neighbour Major pages match it equally well, and the answer is in one sentence at word 500 of an overview page | same, plus a first stage that finds the overview page |
| q01 | `pgl-major-antwerp-2022`, `counter-strike-major-championships` | `pgl-major-copenhagen-2024` (rank 3; `hybrid` had it first) | the incident is at word 796 of 866, beyond the reranker's 200 words, and sibling Major pages looked equally plausible | same |
| q15 | `counter-strike-major-championships`, `magisk-gamer`, `starladder-major-berlin-2019` | `dupreeh` (not in the top 10 for any system), `counter-strike-major-championships` (rank 1) | vocabulary mismatch: the question names nobody, and the player's page says "first and only player to win five majors" in other words, so only the team overview page surfaced | a first stage tuned for "who" questions about records |
| q24 | `counter-strike-major-championships`, `eleague-major-boston-2018`, `counter-strike-in-esports` | `dreamhack-winter-2013` (not in the top 10), `counter-strike-in-esports` (rank 3) | the page about the first Major was never in any system's top 10, and many Major pages use "first" about something else (first in two cities, first in North America) | add the Major's number or year to the query, or index titles separately |
| q35 | `pgl-major-krak-w-2017`, `starladder-major-berlin-2019`, `counter-strike-major-championships` (rank 3; `hybrid` had it first) | `counter-strike-major-championships` | `pgl-major-krak-w-2017`, ranked first, says Gambit won (the first Asian team to win a Major) but never uses the word "Kazakhstan", so my rule did not count it: this may be a strict label and not a ranking failure | re-read the Kraków page and decide whether it states the answer |

In at least q07, q01 and q19 the relevant page states the answer after the first 200 words, which is all the reranker sees of each page, and 94% of my pages are longer than 200 words (the median is 764).
I have not tested that this is the cause; the ablation in section 5 can.
The other pattern is vocabulary mismatch on questions that name nobody (q15, q19, q24), where the first stage never found the right page.
q35 shows that some failures are judgment calls in my labels and not ranking mistakes.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

**Did the winner change?**
By mean score `rerank` came first on both corpora (MRR@10 0.800 on the shared practice queries, 0.911 on mine).
What changed is how clear the win is: on the shared corpus `rerank` was distinguishable from all three other systems on MRR@10, and on mine it is distinguishable only from `bm25` (+0.188 [+0.069, +0.309]), not from `hybrid` or `dense`.
`bm25` also changed role: it was competitive on identifier queries and found none of the paraphrase answers on the shared corpus (recall@10 0.000), and on mine it is the weakest system but still reaches recall@10 0.767 on paraphrase queries.
`hybrid` went from below both of its parts on the shared corpus (MRR@10 0.471) to the best system without Claude on mine (nDCG@10 0.830).

**Why, and what I tested.**
These are my guesses, and the only thing I measured on my own corpus is the query-to-page word overlap (0.93 for hand queries, 0.89 for claude queries).
The shared corpus is 2,484 short legal sections, many of them parallel across Parts 56, 57, 75 and 77, and its paraphrase queries shared almost no words with their answers.
Mine is 220 long articles written as ordinary prose (median 764 words), where a reworded question still shares names and terms with the page, so `bm25` has something to match and the other systems have less to add.
With a smaller corpus and long pages, recall@10 is already high for every system (0.85 to 0.94), so there is less room for a reranker to show a gain.
I did not test any of this directly.

**What the comparison cannot support.**
It rests on 20 queries on one side and 40 on the other, written and judged by different people, and the minimum detectable difference is 0.19 to 0.41 on the shared set and 0.07 to 0.17 on mine, so the two are not equally sensitive.
My answer key was built from the top results of `bm25`, `dense` and `hybrid`, which may favor those systems over `rerank`, and `rerank` only saw the first 200 words of each page.
I cannot say which system is best in general, only what these two collections showed.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 165,536 | 4,318 | 82.7 | 13,795 | 360 | 6.9 |
| traces/answers-rerank.r1.jsonl | rerank | 12 | 24 | 0 | 199,068 | 4,533 | 101.1 | 16,589 | 378 | 8.4 |
| traces/answers-rerank.r2.jsonl | rerank | 12 | 24 | 0 | 179,823 | 4,482 | 150.4 | 14,985 | 374 | 12.5 |
| traces/answers-rerank.r3.jsonl | rerank | 12 | 24 | 0 | 200,845 | 4,268 | 99.5 | 16,737 | 356 | 8.3 |
| traces/own-own-ablation-rerank_long.jsonl | rerank_long | 40 | 40 | 0 | 1,042,891 | 4,230 | 181.6 | 26,072 | 106 | 4.5 |
| traces/own-own-rerank.jsonl | rerank | 40 | 40 | 0 | 414,430 | 4,681 | 167.6 | 10,361 | 117 | 4.2 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 192,573 | 1,978 | 59.7 | 9,629 | 99 | 3.0 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 210,413 | 1,930 | 82.7 | 10,521 | 96 | 4.1 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 204,325 | 1,930 | 101.4 | 10,216 | 96 | 5.1 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 189,336 | 1,820 | 69.9 | 9,467 | 91 | 3.5 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 380,967 | 3,640 | 120.3 | 9,524 | 91 | 3.0 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 9,629 | 3.0 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 9,629 | 3.0 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 9,629 | 3.0 | rerank higher |
| own: bm25 minus rerank | 40 | -0.188 | [-0.309, -0.069] | 10,361 | 4.2 | rerank higher |
| own: dense minus rerank | 40 | -0.062 | [-0.175, +0.046] | 10,361 | 4.2 | not distinguishable |
| own: hybrid minus rerank | 40 | -0.053 | [-0.153, +0.046] | 10,361 | 4.2 | not distinguishable |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 40 | 0.04 | 0.9 |
| traces/retrieval/own-own-dense.jsonl | dense | 40 | 0.47 | 11.8 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 40 | 0.25 | 6.2 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.05 | 2.3 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.62 | 31.0 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.90 | 44.9 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.13 | 3.3 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 1.28 | 32.0 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 1.52 | 37.9 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

rider

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.733 | 0.800 | 0.739 |
| rerank.r2 | 0.758 | 0.800 | 0.759 |
| rerank.r3 | 0.758 | 0.800 | 0.765 |
| range (max minus min) | 0.025 | 0.000 | 0.025 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.142 | [+0.050, +0.258] | rerank.r1 higher |
| rerank.r2 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r2 higher |
| rerank.r3 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r3 higher |
| rerank.r1 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.296 | [+0.168, +0.427] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.316 | [+0.189, +0.445] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.322 | [+0.196, +0.451] | rerank.r3 higher |

Repeated answers shared/rerank:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| rerank.r1 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r2 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r3 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

**Reranker.**
Across three fresh runs on the 20 practice queries the spread is 0.000 on MRR@10 and 0.025 on recall@10 and nDCG@10 (recall@10 0.733 to 0.758, nDCG@10 0.739 to 0.765).
Against `hybrid`, its first stage, the gain on MRR@10 is +0.329 [+0.164, +0.504] in all three runs, and the gain on nDCG@10 runs from +0.296 to +0.322 with every interval above zero.
The run-to-run spread is about a thirteenth of the MRR@10 gain, so the reranker's gain over its first stage survives the variation I measured.
This says only that Claude gives nearly the same ordering when asked again about the same 20 queries.
It does not widen the 20-query interval: the three runs share the same queries, so they are not three independent samples, and the uncertainty from having only 20 queries is the interval above, not the spread.

**Answers.**
All three repeats, like the first answers file, verified 8 of 8 in-corpus questions and declined 4 of 4 out-of-corpus questions, so the range is 0.000 on both shares.
The Wilson 95% intervals are [0.676, 1.000] for 8 of 8 and [0.510, 1.000] for 4 of 4.
These are the honest size of what 8 and 4 questions can show: 100% in every run is consistent with a true rate of about two thirds for the in-corpus questions and about one half for the out-of-corpus ones.
The text was less stable than the shares.
The five retrieved chunks differ between runs in 10 of the 12 questions (the set differs; for a06 and a08 the set is the same), and the number of claims per question changed in a01, a02, a05 and a08 (for example a02 had 2 claims in two runs and 1 in the other two).
For all eight in-corpus questions the top-ranked section was a gold section in every run.
So the verified share does not move, but which claims Claude makes, and which chunks it cites, does.
I compared the shares and claim counts across runs; I did not read the answer text of every repeat.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

I followed the plan in `PREREG.md`: `rerank` against `hybrid`, nDCG@10, Δ = 0.15, and 40 queries.
The interval was +0.044 [-0.033, +0.123], and the minimum detectable difference was 0.112, below my Δ of 0.15, so the gold set was big enough.
That is the "well-powered null" row of my table: a difference as large as 0.15 is ruled out, and my hypothesis that `rerank` beats `hybrid` was not supported.
For a reader, the useful part is the cost: `rerank` made one Claude call per query (about 10,400 input tokens and 4.2 seconds) to gain at most about 0.12 nDCG@10 over `hybrid`, and probably less.
One caveat is that my reranker shows Claude only the first 200 words of each page, so this tested that reranker and not reranking in general.
