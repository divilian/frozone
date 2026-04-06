# Noah's ABM Research

## The Problem

### In One Sentence

Given real-life chat histories, how can we compare the real thing to a fake chat history made by bots intended to mimic real people?

### Expanded

If we have a *specific* person "A" with some associated chat history, and then tell a bot to mimic "A" while putting that bot into the same scenario as "A", how well does the bot mimic "A"?

We specifically want to find meaningful evaluation metric for this.

##  Outline of Solutions

### Claude's Ideas

#### 1. Classifier-Based ("Can a model tell them apart?")

Train or prompt a classifier to distinguish real-A messages from bot-mimicking-A messages. If it can't, the bot has high fidelity. This is probably the most rigorous and publishable framing.

#### 2. Embedding-Based Similarity

Encode both chat logs with a sentence transformer (SBERT is the standard tool) and compare the distributions. Metrics like MMD or cosine similarity tell you how semantically close the bot's outputs are to the real person's.

#### 3. Statistical/Linguistic Feature Comparison

Compare measurable stylistic fingerprints: vocabulary, sentence length, sentiment, hedging language, turn length, response patterns. Useful because it's interpretable — you can say "the bot matched A's sentiment but not their vocabulary diversity."

#### 4. Human Evaluation

Show raters both logs and ask which feels more like person A. Gold standard for naturalness but expensive.

#### 5. Behavioral/Outcome Metrics

If the ABM is modeling something specific (opinion shift, persuasion, etc.), check whether the outcomes of bot-A's conversations match real-A's patterns, not just surface language.


### A review of Claude's Ideas

1 seems strong, and it feels really simple to implement (and could even be implemented with a LLM instance). However, I'm not sure how well it would work if we only have limited samples for a person or bot.

2 feels problematic because things like typos may not get picked up by something so high-level, and we want high fidelity.

3 may make sense, but I need to do more research as to what the right categories to score on are. Again, would we potentially want a LLM to do this?

4 is clearly the most trustworthy, but it could have wide variance, and can be expensive.

5 seems inapplicable given the desired fidelity.

Tldr; 1 and 3 seem like the best avenues to pursure, here.

## Deeper Exploration of Solutions

### Option 3

Resources:
- fast-stylometry python library
- https://www.semanticscholar.org/paper/Surveying-Stylometry-Techniques-and-Applications-Neal-Sundararajan/a0b431dba789801750f247365b05a12e165d364c
- https://www.sciencedirect.com/science/article/abs/pii/S0957417423012472
- SBERT (Sentence-BERT) fine-tuned on authorship tasks
- StyleDistance and similar contrastive learning approaches (explicitly try to separate style from content in the embedding space)

Claude: 

The more directly relevant concept is called **authorship verification via similarity** — specifically the "same author?" binary question. Some approaches here use BERT-style models fine-tuned purely on stylistic pairs, which require surprisingly little per-person data because the model's general language understanding does the heavy lifting.

Siamese BERT is probably your best option for #3 under limited samples — it's more fidelity-aware than raw embeddings and more sample-efficient than a from-scratch classifier. Worth looking at the Tyo, Dhingra & Lipton (2021) "Siamese BERT for Authorship Verification" paper specifically, as it seems directly applicable. 

My thoughts:

Based on some other stuff Claude said, it seems like this type of analysis is also better (than a singular number metric) because it would tell us exactly where the bot is failing to mimic the other style.

#### Burrows's delta tangent

Burrows's delta: https://academic.oup.com/dsh/article-abstract/32/suppl_2/ii4/3865676?redirectedFrom=fulltext&login=false

The downside is, Burrows's delta requires at least a chapter of text to work accurately. But, *if we have at least a chapter worth of text*, it seems like it could work okay. 

Claude thinks using Burrows's delta would be a reasonable first pass, with the following uncertainties:

- Concatenation artifacts — chat messages aren't continuous prose. Burrows Delta was designed for text where function word usage flows naturally. Stitching together hundreds of short turns might create weird boundary effects, though I'm genuinely not sure how much this matters in practice.
- This gets you a single score, not a feature breakdown. You'd know whether the bot mimics person A well, but not where it's failing. For ABM development that diagnostic information seems really valuable, as we probably want to know "the bot got sentiment right but not hedging patterns" more than just "fidelity score = 0.6."
- The 50 message test set might still be on the thin side even concatenated, though I'm less certain about this.

Claude's take: It's probably worth trying as a quick baseline precisely because it's so easy to implement. But I'd treat it as a coarse first-pass rather than the final evaluation framework.

### Hybrid of 1 and 3 approach

#### Version 1: Top-level score

"Here are 300 messages from person A: [corpus A]. Here are 50 messages from a bot attempting to mimic person A: [corpus B]. On a scale of 1-10, how well does the bot mimic person A's writing style? Consider overall feel, word choice, and conversational patterns."

Simple and fast, but opaque. We would get one top-level number.

#### Version 2: Feature-based scores

"Here are 300 messages from person A: [corpus A]. Here are 50 messages from a bot attempting to mimic person A: [corpus B]. Rate the bot's mimicry of person A on each of the following axes from 1-10, and briefly justify each score:

- Vocabulary (word choice, complexity, recurring phrases)
- Sentence/message length patterns
- Sentiment (positivity, negativity, emotional tone)
- Hedging language (uncertainty expressions, qualifiers)
- Turn length and response style
- Punctuation and formatting habits
- Etc.

**Need to do more research as to which critera specifically make sense.** The literature could provide a principled, citable list of axes to feed into the prompt.

## Solution Options to Consider

1. Rough first pass: use Burrows's delta as it is used in the example [here](https://fastdatascience.com/natural-language-processing/fast-stylometry-python-library/)

2. Use a LLM agent:
    a. Rough first pass: a single similarity score
    b. More thorough: obtain multiple scores based on features that we define
