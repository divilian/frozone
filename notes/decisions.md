# Decisions

1. We'll train bots with all data (even toxic) and self-censor them "on the way
   out" (rather than withholding toxic data during training).

1. We need to play with the context window (how many responses, or how many
   lines of text, are considered each time the detectors run) since empirically
   this can have a big impact on things like toxicity score.
