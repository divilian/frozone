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

TODO
