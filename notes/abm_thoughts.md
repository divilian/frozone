# Musings on ABM architecture and design goals

## The (hyper)graph

GM: Scrape Reddit and use _that_ as the hypergraph.

BH: But we don't know how to sample Reddit at scale, and preserve its
hypergraph properties. Maybe we should use a synthetic hypergraph instead?

## What to do about non-posters

SD: Just ditch lurkers who never post? (BH: but would this mess up the graph
properties? SD: yes but maybe we don't care about the non-post-ers.)

## Agent personalities

All: have an LLM distill a personality from their recent posts. (We'll call
this a **personality chunk** for easy reference, though note it doesn't include
only "personality-related" things, like how toxic, how sensitive, how wordy,
etc., but also issue-related things, like how liberal/conservative, what it
thinks about abortion, immigration, Gaza, etc.)

* BH: is this ever updated for an agent? Alternatives:
    1. Keep the personality chunk constant. (super fast)
    2. Recompute the personality chunk based on new synthetic posts as we
       go. (slow)
    3. LR: Only recompute the personality "sometimes". (When we think we
       detect a change? Periodically, to detect drift?)
    4. Give the personality chunk + the content of synthetic posts each
       time we prompt. (faster than 2?)

## Agent state

What is the "state" of each LLM? Alternatives:

1. its state is natural language
2. its **state dict** is a dictionary of specific measurements:
    * level of toxicity
    * opinions on various issues
    * etc

If we go with number 2 (state dict), how do we determine the values? Which LLM

LR: can a bot (1) be objective in assessing its own qualities? (2) assess its
own qualities meaningfully without a training set to do classification the
traditional way?

GM: I predict that few-shot learning will do okay with this.

LR: suppose we have each LLM agent do its own assessment. Is the assessment of
its qualities a separate step than getting its response? GM: doesn't matter if
it's stateless. SD: but it's still an important question...do we tell the LLM
"give us your next nat lang response, and while you're at it, give your scores
on these 15 things" or do we separately tell it "here's what an LLM has
recently said, and has just now said: assign them scores."

## Big and exciting architectural question

SD/LR: will agents be given the opportunity to change the hypergraph, in
addition to communicating within it? (i.e., can an agent get pissed off and
rage-quit a subreddit? can an agent hear from someone on one of their current
subreddits about another subreddit that they might be interested in, and choose
to join it?)

## Things we don't know the right answer to until we get our hands dirty

1. Is recomputing personality chunk every time too computationally prohibitive?
   (Can we go with number 2 above, or do we need to do another thing.)
2. Is the bot going to make good self-assessments of the traits we care about?
   (Or do we need a separate classifier.)
3. How much overlap between subreddits is there, actually? (do we have a
   meaningful hypergraph?)


## i.v.'s and d.v.'s

### i.v.'s

* how many Frobots, Hotbots, etc?
* which subreddits are the FBs etc deployed to?

### d.v.'s

* how much of The Big Five Bad Things(tm) is there in the resulting synthetic
  text? (Did FB's improve that?)
* how much movement in opinion (as measured by state dicts) is there?
* how much affective polarization is present in the agents?
* how much do agents influence the hypergraph themselves? (if they can; see
  "Big and exciting architectural question," above.)

### Research questions

* Do FB/HBs in/decrease The Big Five, and by how much, etc.?
* Do FB/HBs increase affective polarization?
* Do the presence of FB/HBs change the hypergraph and by how much?
* Do the presence of FB/HBs change people's opinions more often?

## Coda: a big control-group-only question

GM: Is the synthesized content from the bots -- regardless of whether they're
FB's, HB's, or just user LLMs -- high-fidelity to human communication? How to
measure that?


# Action items

1. Actually actually for-reals pull the Prolific trigger. (LR)
1. Do the delete-and-reclone-the-repo thing. ([All #195](../../../issues/195))
1. Dive into the Reddit API and data, and find out if there are any surprises
   about how it works? What volume are we looking at? How many posts per day
   per user? How many users? How many subreddits are political in nature? Which
   ones look like they are worth pulling from? ([GM #196](../../../issues/196))
1. Personality distillery. ([BH #197](../../../issues/197))
    a. Experiment with a "personality distiller" prompt and see how it does on
    some onesy-twosy reddit content you manually scrape.
    b. Do some deep thinking about what properties should go in the personality
    dict. (We know we want "personality/interaction style stuff" and also "what
    you think on various issues" type stuff. Make this more refined.)
1. Lit search: what has been done regarding LLM-based ABMs which modify their
   graph/hypergraph? (see "Big and exciting architectural question," above.)
   ([LR #198](../../../issues/198))
1. Lit search: what has been done regarding the measurement of synthesized bot
   content to assess its fidelity to real human communication? How is this
   normally measured? ([GM/NF #199](../../../issues/199))
