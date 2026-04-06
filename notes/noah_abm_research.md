# Noah's ABM Research

## The Problem

### In One Sentence

Given real-life chat histories, how can we compare the real thing to a fake chat history made by bots intended to mimic real people?

### Expanded

If we have a *specific* person "A" with some associated chat history, and then tell a bot to mimic "A" while putting that bot into the same scenario as "A", how well does the bot mimic "A"?

We specifically want to find meaningful evaluation metric for this.

###  Solutions

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

TODO
