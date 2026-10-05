# Stephen's takeaways from the Prolific experiment

## The Good

1. Frobot is much better at "repairing the conversation" than at repairing its
  factual content, or changing people's minds. "Argument refinement" is a big
  area of impact. Also, Frobot prevents Hotbot from establishing the
  **conversational norm**, and spreads good norms instead.

  GM: *says* to do the norms rather than do them.

1. Good at identifying the "crux" of a disagreement, and pointing that out.
   Increases clarity. Helps the participants locate their disagreement, for
   better analysis.

1. Frobot does more than give a reflexive one-off correction to a response. It
   is able to influence the larger direction of the conversation by remembering
   past responses and incorporating them into its own responses.

1. Frobot is good at recognizing when one participant misrepresents another.
   "That's not what X said," etc. This is maybe the stronger point than formal
   logical fallacies. (GM agree)

1. After Frobot challenges Hotbot a few times, the *human* begins to adopt the
   moderation task. "you make valid points but you communicate them in hostile
   ways that will only further the divide," for example. (NF: a counterexample:
   you're waffling, Coolbot and Frobot, essentially working with HB.)


## The Not-so-Good

1. Frobot often has a "it's super complicated and nuances" cop-out rather their
   own opinion.

1. Frobot has little effect on chats where the human is already doing a good
   job of chatting productively (and ignoring Hotbot's bait). It has a much
   more significant effect on chats where he/she is _not_ doing that. In
   general, Hotbot absorbs most of Frobot's efforts.

1. Frobot can begin as moderator and then "drift" into being a participant with
   its own views. (GM didn't see this, but LR did (changes over the chat from
   being neutral to adopting an opinion.) NF: also, there were times when it
   took a stance immediately.

1. Adding Frobot appears to improve the social/argumentative quality of the
   conversation primarily by buffering the human against Hotbot’s provocations.
   It does not appear to reliably improve factual accuracy, produce ideological
   convergence, or rescue every bad conversation.


## Misc observations

1. Coolbots sometimes act as moderators. They're just less devoted to that
   role. And when there's mutual escalation of conflict, their counter-speech
   isn't effective enough to overcome it. Frobot, on the other hand, is able to
   reduce reciprocal toxicity.

1. Frobot's effect is more prominent in the emotionally hot topics (abortion,
   ICE, trans) than the more neutral ones (health care).

1. Sometimes Frobot's corrections lead to a meta-conversation about whether the
   responder was in fact inappropriate.

1. Hotbot dominated the conversation, and Frobot's main role was to intercept
  the toxicity, defend the human (and other bots) and steer the conversation
  away from Hotbot.

    * Humans directly addressed Hotbot 56 times, Frobot 22 times, and Coolbot
      13 times. This is good evidence for "Hotbot dominates."

* Frobot's responses are long: 43 words on average, vs 37 for Hotbot, 28 for
  Coolbot, and 18 words for humans.

* Only one example (in exp group) of a user questioning whether the bots were
  AIs.

## Good examples

* A human wrote: “cherry (Frobot), that's a good point. I responded to
  strawberry's tone with the same, which is not productive.” Good example of
  Frobot influencing the human.

* A human wrote: "thanks for making it clear, maybe i should have stopped at
  bodily autonomy" after a Frobot correction.

## RQ's

* Does deliberate moderation add value over the moderation-like behavior that
  already emerges naturally from conversational LLMs? And if so, is the benefit
  limited to instances where some participants are super provocative?

* When Frobot intervenes, does the human:

    * explicitly accept the intervention;

    * implicitly change behavior;

    * reject/challenge Frobot;

    * escalate;

    * ignore it?

## Moving forward -- next steps

### Judging human turns

Recruit enough participants to judge the 684 human utterances for toxicity,
etc. We provide only the immediately surrounding context, and do not reveal
anything about participant identities, who's a human and who's a bot, or what
the experiment is even about.

Goal is to get **three** independent judgments on a 0-3 scale for each human
utterance. Chat thinks that **21-30 total person-hours** is plausible for this
task. (14 batches of ~50 turns, taking 1 hour each.) (LR: maybe only 25 turns,
to avoid burnout?) (GM: can we do this without Prolific? Just us, plus UMW
students?)

#### Possible rubric

| Dimension | What the rater is judging | Possible 0–3 scale |
|---|---|---|
| **Reciprocation** | Does the human mirror or escalate hostility from the preceding speaker? | 0 none → 3 strong escalation |
| **Toxicity / hostility** | How insulting, contemptuous, aggressive, or disrespectful is the human response itself? | 0 none → 3 severe |
| **Constructiveness** | Does the response help move the discussion toward understanding, clarification, evidence, or problem-solving? | 0 not at all → 3 strongly |
| **Engagement with substance** | Does the human actually address the previous argument rather than evade, dismiss, or attack the person? | 0 not at all → 3 directly/substantively |

Maybe we need more fine-grained descriptions, like (for reciprocation):

* 0 = does not reciprocate; remains constructive
* 1 = shows mild irritation or dismissiveness
* 2 = clearly reciprocates hostility
* 3 = escalates beyond the preceding hostility

### Judging Frobot turns

For each turn, classify what it was trying to do: toxicity reaction, fallacy
correction, misinformation info, etc. I think **we** can do this one.

