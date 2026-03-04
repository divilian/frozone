# Zoom meeting with Clayton, 3-4-2026

## Stephen's dream: (internal vs external)

Generally speaking, SD is very interested in the concept of one's **inner
beliefs** and how they interplay with the outward communication one generates
and consumes. It seems to me that the definition of a "politically healthy
society" involves not only the absence of visible, external things like toxic
language, but also _the willingness to change one's opinion_.

SD is very influenced by this book, and recommends it to all humans: 

> Rauch, J. (2021). [_The Constitution of Knowledge: A Defense of Truth._](https://www.amazon.com/dp/B0BL841MK1) Brookings Institution Press.

Eventually, SD would like to study the phenomenon of people _actually changing
their political opinions_ in a social network, not merely changing how they
_express_ themselves on that network. SD thinks this aspect is probably
post-May, but GM thinks we could do it now, if we handle the "internal" piece
simply (just tell the LLMs "hey, if you encounter a compelling argument that
goes against one of your beliefs, feel free to change your belief.")

### Conversation extract

> GM: there's two different things agents do: vote, and communicate online.
> 
> SD: yes, and "vote" seems to be a reflection of one's private inner beliefs,
> whereas communicating is one's public expression (which may not be perfectly
> aligned with their inner beliefs).
> 
> LR: we should focus squarely on the talking part. (reducing affective polarization)
> 
> SD: I cautiously agree with LR for May, but not for beyond May.


## Detecting "willingness to change one's mind"

> GM: this is totally inaccessible
> 
> SD: _totally_? Naw. If there's information which Garrett the human uses to
> determine that Stephen is willing to change one's mind, then the evidence
> exists for an LLM to also determine that.
> 
> CL: a possible proxy to this: being willing to listen, and respond in a way that indicates you (want to) understand what was said.
> 
> LR: note that a person might actually not understand, despite good faith effort in doing so. This person should still be counted as "willing to change one's mind."
> 
> SD: agreed!
>
> CL: note that some literal phrasings like "I don't understand how anybody could think that" aren't indicators of a good faith attempt to understand; quite the opposite. 


## A separate research angle (and low-hanging fruit)

The "LLMs simulating internal state" is useful in and of itself, even aside
from the social network piece.

It's unclear whether an LLM will modify its internal state in a way that
correlates to what humans actually do.

> GM: it's going to be pretty low-fidelity in actually determining whether the person *is* willing to change their mind. (Maybe LLMs would be better than people at that, but in fact we humans suck at it, so that's not encouraging.)
> 
> LR: (this is outside of spring scope)
> 
> SD: (agreed!)


## Laur's brilliant architectural piece

For CoolBot, we could train a separate "should the agent change its mind" LLM,
which then possibly changes the state variables in the "agent LLM."

For Frobot, we could have a "willingness to change mind" **detector** (even
though FB never changes its own mind.) An intervention for that could be
"reinforcement/encouragement to go ahead and change your mind.

CL gives us some different pieces to consider:

1. determining whether someone is willing to change one's mind. (SD: use
    ChangeMyView dataset?)

2. why might we care about determining that?

    a. one reason is we could have different interventions depending on what we
      think that internal value is.
        - if they're not willing, trigger some intervention ("model good
          behavior for them": train a bot to simulate thoughtful consideration,
          and then actually changing one's mind.
        - if they're willing, then possibly try to persuade them of a POV.

## Stephen's thoughts on "contradictions"

Think this out: we tell an LLM "you are pro-choice and anti-ICE." And then we
turn around and tell them "but you can and should change your view in the face
of compelling arguments." In a way, this can be seen as a **contradiction** in
the prompt instructions.

LR: people have internal contradictions all the time, maybe is this a feature?

CL: yes, but this needs to be modeled. Namely, if we have 'reasonable' agents
in the network, we have to model that reasonableness. (SD doesn't fully
understand what CL was getting at here.)

## Random last thoughts from Clayton:

CL also predicts that the order in which we (1) tell the agent its initial
beliefs, and (2) tell it that it's allowed to change them, might have a
sequencing effect to watch out for. (Recency bias.)

Big picture, we have possibly two different objectives:

1. make the political conversation itself "better"
    - and btw, does CoolBot actually respond to FB's interventions? We need to
      analyze that!
2. make agents change their mind more often

CL: What might we learn?
- that the other bots are oblivious to toning-down statements
- or we might be lucky

CL: It might turn out that we don't need to be all that faithful to reality at the
micro level in order for the aggregate effect to be achieved. (SD: this is
sensitivity analysis, right?)

Action Items:

- LR: look into whether or not CoolBot actually responds to FroBot
  interventions, whether FroBot was chastising it, or another bot in its
  hearing.
- GM: As a point of comparison: how do CoolBot's responses to FroBot interventions
  compare to our toxicity data sets? Find out whether our HotBot training set
  has examples of people intervening in the face of toxic speech, etc.
- read https://www.newyorker.com/magazine/2026/02/16/what-is-claude-anthropic-doesnt-know-either

