# Ingest report

Written by `uv run p2 ingest`.
It lists every document in this corpus that ingest added, with what the cleaning pass did and anything that looks wrong.
Running ingest again adds to the table and replaces the "last run" section, and `uv run p2 ingest --report` rewrites it for the documents in docs/ now, after you removed some.

## Summary

- Documents: 220 (the final check needs at least 200)
- Words: 269,010
- Estimated tokens (words times 1.4): 376,614 (`p2 check` warns above 800,000 and fails above 1,000,000)
- Flagged documents: 0

## Documents

| docid | words | characters per page | flags | cleaning |
|---|---:|---:|---|---|
| `2024-esports-world-cup` | 863 | - | - | - |
| `2025-esports-world-cup` | 1,179 | - | - | - |
| `2026-esports-world-cup` | 1,092 | - | - | - |
| `4kings` | 224 | - | - | - |
| `abbe-borg` | 222 | - | - | - |
| `allu-gamer` | 829 | - | - | - |
| `alternate-attax` | 164 | - | - | - |
| `anders-blume` | 460 | - | - | - |
| `andreas-thorstensson` | 1,258 | - | - | - |
| `apex-counter-strike` | 3,228 | - | - | - |
| `astralis` | 2,474 | - | - | - |
| `aurora-gaming` | 858 | - | - | - |
| `b1t` | 388 | - | - | - |
| `blast-austin-major-2025` | 1,126 | - | - | - |
| `blast-paris-major-2023` | 435 | - | - | - |
| `blast-premier` | 618 | - | - | - |
| `broky` | 441 | - | - | - |
| `cadian` | 302 | - | - | - |
| `captainmo` | 194 | - | - | - |
| `chaos-esports-club` | 187 | - | - | - |
| `chiefs-esports-club` | 720 | - | - | - |
| `cloud9` | 6,879 | - | - | - |
| `coldzera` | 638 | - | - | - |
| `complexity-gaming` | 2,040 | - | - | - |
| `copenhagen-wolves` | 155 | - | - | - |
| `counter-logic-gaming` | 6,816 | - | - | - |
| `counter-strike` | 1,070 | - | - | - |
| `counter-strike-2` | 1,863 | - | - | - |
| `counter-strike-coaching-bug-scandal` | 1,063 | - | - | - |
| `counter-strike-condition-zero` | 2,427 | - | - | - |
| `counter-strike-global-offensive` | 3,770 | - | - | - |
| `counter-strike-in-esports` | 2,617 | - | - | - |
| `counter-strike-major-championships` | 3,526 | - | - | - |
| `counter-strike-malvinas` | 402 | - | - | - |
| `counter-strike-match-fixing-scandal` | 2,391 | - | - | - |
| `counter-strike-neo` | 334 | - | - | - |
| `counter-strike-online` | 761 | - | - | - |
| `counter-strike-source` | 1,721 | - | - | - |
| `counter-strike-surfing` | 650 | - | - | - |
| `counter-strike-video-game` | 3,964 | - | - | - |
| `cs-money` | 514 | - | - | - |
| `denial-esports` | 231 | - | - | - |
| `dev1ce` | 570 | - | - | - |
| `dignitas-esports` | 1,218 | - | - | - |
| `donk-gamer` | 1,314 | - | - | - |
| `dreamhack-open-cluj-napoca-2015` | 865 | - | - | - |
| `dreamhack-winter-2013` | 473 | - | - | - |
| `dupreeh` | 250 | - | - | - |
| `dust-ii` | 1,534 | - | - | - |
| `edward-gaming` | 1,976 | - | - | - |
| `efgaming` | 236 | - | - | - |
| `ehome` | 258 | - | - | - |
| `eleague-cs-go-premier` | 1,000 | - | - | - |
| `eleague-cs-go-premier-2018` | 394 | - | - | - |
| `eleague-major-2017` | 1,998 | - | - | - |
| `eleague-major-boston-2018` | 3,270 | - | - | - |
| `eleague-season-2` | 605 | - | - | - |
| `elige` | 216 | - | - | - |
| `ems-one-katowice-2014` | 480 | - | - | - |
| `ence-esports` | 744 | - | - | - |
| `envy-esports` | 3,091 | - | - | - |
| `epsilon-esports` | 276 | - | - | - |
| `esea-league` | 296 | - | - | - |
| `esl-one-cologne-2014` | 597 | - | - | - |
| `esl-one-cologne-2015` | 687 | - | - | - |
| `esl-one-cologne-2016` | 1,575 | - | - | - |
| `esl-one-cologne-2017` | 668 | - | - | - |
| `esl-one-cologne-2018` | 2,817 | - | - | - |
| `esl-one-cologne-2019` | 1,642 | - | - | - |
| `esl-one-katowice-2015` | 684 | - | - | - |
| `esl-one-new-york-2016` | 197 | - | - | - |
| `esl-pro-league` | 1,111 | - | - | - |
| `esl-pro-league-season-1` | 580 | - | - | - |
| `esl-pro-league-season-14` | 881 | - | - | - |
| `esl-pro-league-season-2` | 812 | - | - | - |
| `esl-pro-league-season-3` | 625 | - | - | - |
| `esl-pro-league-season-4` | 704 | - | - | - |
| `esl-pro-league-season-5` | 3,403 | - | - | - |
| `esl-pro-league-season-6` | 5,290 | - | - | - |
| `esl-pro-league-season-7` | 5,937 | - | - | - |
| `esl-pro-league-season-8` | 4,465 | - | - | - |
| `esl-pro-league-season-9` | 3,062 | - | - | - |
| `eternal-fire-esports` | 349 | - | - | - |
| `evil-geniuses` | 3,891 | - | - | - |
| `evos-esports` | 823 | - | - | - |
| `f0rest` | 790 | - | - | - |
| `faceit-major-london-2018` | 3,020 | - | - | - |
| `fallen` | 221 | - | - | - |
| `faze-clan` | 2,350 | - | - | - |
| `fenerbah-e-esports` | 701 | - | - | - |
| `flamengo-esports` | 349 | - | - | - |
| `flipside-tactics` | 413 | - | - | - |
| `flusha` | 1,598 | - | - | - |
| `fnatic` | 6,056 | - | - | - |
| `fox-gamer` | 249 | - | - | - |
| `freakazoid-gamer` | 377 | - | - | - |
| `friberg-gamer` | 246 | - | - | - |
| `furia-esports` | 677 | - | - | - |
| `g2-esports` | 5,971 | - | - | - |
| `gambit-esports` | 1,903 | - | - | - |
| `get-right` | 1,033 | - | - | - |
| `gla1ve` | 867 | - | - | - |
| `godsent` | 346 | - | - | - |
| `gotfrag` | 260 | - | - | - |
| `ground-zero-gaming` | 255 | - | - | - |
| `guardian` | 448 | - | - | - |
| `gun-game` | 599 | - | - | - |
| `h2k-gaming` | 212 | - | - | - |
| `happy-gamer` | 1,558 | - | - | - |
| `heaton-gamer` | 792 | - | - | - |
| `heroic-esports` | 813 | - | - | - |
| `hltv` | 1,212 | - | - | - |
| `iem-cologne-major-2026` | 1,144 | - | - | - |
| `iem-katowice-major-2019` | 1,936 | - | - | - |
| `iem-rio-major-2022` | 327 | - | - | - |
| `immortals-esports` | 1,318 | - | - | - |
| `imperial-esports` | 563 | - | - | - |
| `inferno-counter-strike` | 1,488 | - | - | - |
| `intel-extreme-masters-season-x-san-jose` | 238 | - | - | - |
| `intel-extreme-masters-season-xii-oakland` | 392 | - | - | - |
| `intel-extreme-masters-season-xiii-world-championship` | 182 | - | - | - |
| `isurus-gaming` | 443 | - | - | - |
| `izak-gamer` | 162 | - | - | - |
| `jax-money-crew` | 216 | - | - | - |
| `kanga-esports` | 270 | - | - | - |
| `karrigan` | 794 | - | - | - |
| `kennys` | 702 | - | - | - |
| `kioshima` | 676 | - | - | - |
| `ksharp` | 348 | - | - | - |
| `ldlc-ol` | 302 | - | - | - |
| `list-of-competitive-counter-strike-maps` | 1,216 | - | - | - |
| `list-of-songs-recorded-by-basshunter` | 470 | - | - | - |
| `luminosity-gaming` | 910 | - | - | - |
| `m0nesy` | 756 | - | - | - |
| `made-in-brazil-esports` | 369 | - | - | - |
| `made-in-thailand-e-sports` | 574 | - | - | - |
| `magisk-gamer` | 490 | - | - | - |
| `maikelele` | 773 | - | - | - |
| `makazze` | 150 | - | - | - |
| `meetyourmakers` | 222 | - | - | - |
| `mirage-counter-strike` | 520 | - | - | - |
| `mlg-major-championship-columbus` | 1,388 | - | - | - |
| `mopoz` | 326 | - | - | - |
| `mouz` | 1,488 | - | - | - |
| `n0thing` | 593 | - | - | - |
| `natus-vincere` | 3,805 | - | - | - |
| `neo-gamer` | 761 | - | - | - |
| `niko` | 1,948 | - | - | - |
| `ninjas-in-pyjamas` | 827 | - | - | - |
| `nrg-esports` | 2,604 | - | - | - |
| `nuke-counter-strike` | 766 | - | - | - |
| `og-esports` | 1,758 | - | - | - |
| `olofmeister` | 1,036 | - | - | - |
| `optic-gaming` | 5,837 | - | - | - |
| `order-esports` | 810 | - | - | - |
| `ossi-ketola` | 444 | - | - | - |
| `pain-gaming` | 185 | - | - | - |
| `paper-rex` | 2,250 | - | - | - |
| `perfect-world-shanghai-major-2024` | 901 | - | - | - |
| `pgl-esports` | 234 | - | - | - |
| `pgl-major-antwerp-2022` | 371 | - | - | - |
| `pgl-major-copenhagen-2024` | 861 | - | - | - |
| `pgl-major-krak-w-2017` | 1,580 | - | - | - |
| `pgl-major-stockholm-2021` | 672 | - | - | - |
| `plopski` | 193 | - | - | - |
| `professional-esports-association` | 1,148 | - | - | - |
| `rain-gamer` | 446 | - | - | - |
| `rambo-gamer` | 375 | - | - | - |
| `renegades-esports` | 1,322 | - | - | - |
| `rogue-esports` | 1,108 | - | - | - |
| `ropz` | 608 | - | - | - |
| `ryujehong` | 1,175 | - | - | - |
| `s1mple` | 1,606 | - | - | - |
| `serious-gaming` | 1,558 | - | - | - |
| `sgares` | 1,025 | - | - | - |
| `shahzam` | 396 | - | - | - |
| `shox-gamer` | 256 | - | - | - |
| `shroud-gamer` | 579 | - | - | - |
| `sk-gaming` | 3,059 | - | - | - |
| `smithzz` | 260 | - | - | - |
| `space-soldiers-esports` | 856 | - | - | - |
| `splyce` | 980 | - | - | - |
| `starladder-budapest-major-2025` | 1,031 | - | - | - |
| `starladder-major-berlin-2019` | 1,632 | - | - | - |
| `stephanie-harvey` | 617 | - | - | - |
| `stewie2k` | 696 | - | - | - |
| `stu-holden` | 2,563 | - | - | - |
| `summit1g` | 309 | - | - | - |
| `tarik-gamer` | 361 | - | - | - |
| `taz` | 393 | - | - | - |
| `team-3d-esports` | 288 | - | - | - |
| `team-curse` | 3,705 | - | - | - |
| `team-falcons` | 2,204 | - | - | - |
| `team-liquid` | 3,004 | - | - | - |
| `team-noa` | 1,708 | - | - | - |
| `team-roccat` | 177 | - | - | - |
| `team-secret` | 1,359 | - | - | - |
| `team-spirit-esports` | 1,698 | - | - | - |
| `team-vitality` | 3,930 | - | - | - |
| `tempo-storm` | 2,273 | - | - | - |
| `tenz` | 613 | - | - | - |
| `the-mongolz` | 158 | - | - | - |
| `titan-esports` | 971 | - | - | - |
| `tsm-esports` | 3,577 | - | - | - |
| `twistzz` | 1,407 | - | - | - |
| `u-s-army-esports` | 479 | - | - | - |
| `unicorns-of-love` | 367 | - | - | - |
| `vaevictis-esports` | 681 | - | - | - |
| `vega-squadron` | 417 | - | - | - |
| `ventus-gaming` | 1,692 | - | - | - |
| `virtus-pro` | 1,991 | - | - | - |
| `wemade-entertainment` | 871 | - | - | - |
| `winterfox` | 165 | - | - | - |
| `world-e-sports-games` | 470 | - | - | - |
| `world-electronic-sports-games` | 945 | - | - | - |
| `world-league-esport-bundesliga` | 217 | - | - | - |
| `xantares` | 913 | - | - | - |
| `xizt` | 374 | - | - | - |
| `xyp9x` | 163 | - | - | - |
| `zywoo` | 1,219 | - | - | - |

## Not added in the last run

- `sources.json`: File type .json is not one ingest reads (it reads PDF, HTML, Markdown and plain text).

## What to check by eye

Ingest cleans text by rules, and rules miss things.
Take five minutes to open the shortest, a middle one and the longest document next to its original and read one page of each.

- Search the documents for `þ`, `¼`, `(cid:` and the replacement character.
  A hit usually means the PDF's font map is wrong, which no tool can repair, so treat it as a defect and leave that document out.
- Look at the end of a few papers.
  Ingest drops a trailing reference list when it finds a References heading or a run of numbered entries.
  A paper whose list has neither can keep it, and then every author and journal name matches queries it should not.
- Open the first lines of a few documents.
  Author lists, copyright pages and tables of contents are not removed automatically, and you may want to cut them.
- Compare one table with the PDF.
  A PDF prints footnote marks as small raised digits, and the converter glues them onto the word or number next to them: `ALUMINUM1` is the heading ALUMINUM with footnote 1, and `11210,000` can be 210,000 with footnote 11.
  Quotes still match the stored text, but a number read from it can be wrong, so check before you trust a figure in a query, a judgment or an answer.
- Fix the `license` column in the manifest for every document, then run `uv run p2 license`.
  It is `unknown` until you do, and `unknown` does not pass.

## If a document is flagged as scanned

A scan is a picture of a page, so there is no text for ingest to read.
This template does not install an OCR tool, because it is large and most students never need it.
If you do need one, the opt-in route is pymupdf4llm with rapidocr, run on its own outside the template's environment:

```
uv run --no-project --with pymupdf4llm --with rapidocr python -c "import pymupdf4llm, sys, pathlib; pathlib.Path(sys.argv[2]).write_text(pymupdf4llm.to_markdown(sys.argv[1], use_ocr=True, force_ocr=True), encoding='utf-8')" scan.pdf scan.md
```

Put the resulting `.md` file in your folder and ingest the folder again.
It costs about 2 seconds a page, and OCR text needs a second look: it misreads ligatures, hyphens and numbers.
pymupdf4llm is AGPL-3.0 software, so use it only as a tool on your own machine, and do not add it to this repo's dependencies or copy its code into the repo.
