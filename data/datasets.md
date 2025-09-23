# Corpora we might use

## Stance detection
* [SemEval-2016](https://www.saifmohammad.com/WebPages/StanceDataset.htm):
  about 5000 labeled tweets, indicating stance on targets such as Hillary
  Clinton, Atheism, Climate Change is Real
* [P-Stance](https://aclanthology.org/2021.findings-acl.208.pdf): 21,000 tweets
  labeled with pro/con/neut towards Bernie, Biden, and Trump
* [Twitter Stance Election 2020](https://arxiv.org/abs/2103.01664)
  (Grimminger 2021): 3000 tweets labeled for stance towards Biden and Trump, as well as "offensiveness"
* [Knowledge Enhance Masked Language Model for Stance
  Detection](https://portals.mdi.georgetown.edu/public/stance-detection-KE-MLM)
  (Kawintiranon 2021): 2500 tweets labeled as pro/anti Biden

## Misinformation
* [FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet) (Shu 2020)
* Also see
  [`factchecking_datasets`](https://files.zotero.net/eyJleHBpcmVzIjoxNzU3Njk0NzUyLCJoYXNoIjoiMmE0NzVhYWQ1NTA4ODcwODM5NWZkZjYzNjI1M2NiMGQiLCJpdGVtIjoiMjA4MTcwNThcL0FVQUlTSjZCIiwiZmlsZW5hbWUiOiJmYWN0Y2hlY2tpbmdfZGF0YXNldHMucG5nIiwiY29udGVudFR5cGUiOiJpbWFnZVwvcG5nIn0%3D/0c05a25813f87bbc205919b863fdbe4172c18d3bbe33a13b73c4649cfe22c444/factchecking_datasets.png)
  and
  [`factchecking_datasets2`](https://files.zotero.net/eyJleHBpcmVzIjoxNzU3Njk0NzkzLCJoYXNoIjoiYWI2YTQzMDc3OWIyMjdkMzBjZTE2NDU2NmRhZDMxMjAiLCJpdGVtIjoiMjA4MTcwNThcL0E2NlNaNThFIiwiZmlsZW5hbWUiOiJmYWN0Y2hlY2tpbmdfZGF0YXNldHMyLnBuZyIsImNvbnRlbnRUeXBlIjoiaW1hZ2VcL3BuZyJ9/6d5b011e800a64479a4684d86ef6011866b3823359ed17fc3ece8ddddbe9b2f6/factchecking_datasets2.png) images in "misinfo/disinfo" | "datasets"
  Z folder
* [LIAR Dataset](https://sites.cs.ucsb.edu/~william/papers/acl2017.pdf) Statements collected from POLITIFACT.COM rated on a scale of truthfulness with context and justification.
   * [LIAR-PLUS](https://github.com/Tariq60/LIAR-PLUS).  LIAR dataset with human justifications from related fact checking articles.
   * [LIAR++ and FullFact](https://github.com/LanD-FBK/benchmark-gen-explanations). Claim-article-verdict tripples.  LIAR++ based on LIAR-PLUS.

## Misrepresentation of sources

* FEVER / FEVEROUS (claim→evidence→support/refute/NEI)
https://huggingface.co/datasets/fever/fever
https://huggingface.co/datasets/fever/feverous

* VitaminC (contrastive evidence—tiny wording changes flip the label; perfect for “seems to support but doesn’t”)
Paper: https://aclanthology.org/2021.naacl-main.52/ Data: https://github.com/TalSchuster/VitaminC

* MultiFC (26 fact-checking sites; rich metadata; real-world claims)
Paper: https://aclanthology.org/D19-1475/

* AVeriTeC (real-world, multi-org fact checks; lots of social posts as sources/claims)
https://neurips.cc/virtual/2023/poster/73517

* Attribution/faithfulness specific
https://huggingface.co/datasets/McGill-NLP/FaithDial

* AttributionBench (eval whether answers are supported by citations):
https://arxiv.org/abs/2402.15089o

* RARR (pipeline to find support & revise unsupported spans): https://arxiv.org/abs/2210.08726

* https://aclanthology.org/2020.emnlp-main.623/

* Emergent — claim↔article stance; journalists labeled veracity & stance.
Paper (PDF): https://aclanthology.org/N16-1138.pdf

* SemEval-2016 Task 6 (Twitter stance) — for short, informal posts.
https://aclanthology.org/S16-1003/

* PHEME — rumor threads with support/deny/uncertain/evidence.
Overview: https://www.zubiaga.org/datasets/

* Quotebank — 178M–235M attributed quotations across news; use to verify exact
 wording/at  (Great for catching "the source doesn't say that")

## Polarization
* [PolarOps](http://stephendavies.org/writings/IC2S2_2022abstract.pdf) (Cagle 2021): 522 nested Reddit threads labeled as "polarized" or "not"

