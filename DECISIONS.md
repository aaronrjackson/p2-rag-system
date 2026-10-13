# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

TODO: your answer to prompt 1.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

The fork was the embedding model for `dense`: bge-small-en-v1.5, or potion-retrieval-32M, the other model the lab measured.
Claude wrote `dense.py` with bge-small as the default, with the model set by `[dense] model` in `p2.toml`, and I went with it without running potion.
So I have one number for the choice, `dense` at MRR@10 0.562 and recall@10 0.558 on the practice queries, and none for the alternative.
Potion is a static model, so it would have encoded the 3,127 chunks faster than bge's 85 seconds and searched faster than the 31 ms per query I measured, and it might have scored lower on the paraphrase queries because it has no contextual network.
I did not measure it, and the cost of that is that every claim I make about `dense` and `hybrid` is a claim about bge-small and not about dense retrieval in general.
Skipping it saved the time of a second 85-second encode and a second set of runs, which is small, so I cannot call it a strong reason.
The same goes for a second fork, how many documents the reranker sees: I used 20, the number in the brief, and did not try 10 or 30.

In `EVAL.md` the `dense` numbers and the intervals for `hybrid` and `rerank` all depend on this one choice.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

TODO: your answer to prompt 3.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

The number I trust least is "8 of 8 verified (100%)" in the answers table of `EVAL.md` section 2.
Eight questions is few, and the Wilson interval says so: [0.676, 1.000], so the true rate could be about two thirds.
More importantly, the check only proves that each quote is a real piece of the cited chunk.
When I read three of the answers against their chunks, a02's second claim said the percentage rises "only" where methane is present, and its quote does not say "only", yet it counted as verified.
So 100% verified is a share of quotes that are real, and not a share of claims that the quotes support.

To trust it I would need to read all 11 claims and not three, and ideally run the answers more than once, since Claude's replies are not deterministic.
I tested it by reading three answers, which found that one small overreach and no fabricated quote.
I have not read the other five in-corpus answers.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

I do not understand why `hybrid` scores below both of its parts.
On the practice queries its MRR@10 is 0.471, against 0.507 for `bm25` and 0.562 for `dense`; by class it falls between them (identifiers 0.514, paraphrases 0.152).
My first guess, that `bm25`'s zero-score padding added noise to the fusion, was wrong: dropping those documents before fusing left MRR@10 at 0.471.
My remaining guess is that equal-weight fusion lets the weaker system's ranking pull down the stronger one's answer, but I have not tested it.

To find out, I would look at the paraphrase queries in `runs/shared/hybrid.practice.trec` next to `runs/shared/dense.practice.trec`, and for each one compare the rank of the relevant document in the `bm25` ranking and the `dense` ranking.
Then I would try a weighted fusion on a held-out part of the practice queries, since tuning weights on all 20 would overfit.
It matters because `rerank` takes `hybrid`'s top 20 as its input, so any relevant document `hybrid` pushes out of the top 20 is lost to the reranker, and I have not measured how often that happens.
