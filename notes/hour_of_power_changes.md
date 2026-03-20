# HoP-related changes

Last-minute changes to app before Prolific.

1. Change sequence of corruption and fruit-name substitution.
1. Dial down typos (look at `corrupt()` function parameters.)
1. Bots including "(pass)" sometimes (especially when page is refreshed).
    1. GM: relocate the "literal '(pass)' remover" (and/or use regex's) and
       test that it works (right now it reliably occurs on page refresh).
1. The "FroBot is sometimes replying to multiple things per post" issue.
    1. BH: Prompt our way out of this: be clear in instructions that every bot
       response should only respond to **one** issue.
1. Frobot responding to things that were way too early in the thread.
    1. BH: Prompt our way out of this: "Frobot: only call out things that have
       occurred since your last response."
1. Frobot is repeating the essence of its old response. (Fix for all bots
   though):
    1. BH: Prompt our way out of this: "Frobot: don't give the same response
       that you've given previously." Or: "don't address any issue that you've
       already addressed in a previous post."
1. LR: replace "_ has entered the chat" with "this chat room currently
   contains fruits 1, 2, 3.
1. LR: with some random frequency, omit the trailing punctuation.
1. BH: fix "bots giving 404's" by prompting out of it ("never give links").
1. GM: tweak the timing: (1) dial up the overall time-to-respond by a bit, and
   (2) dial down the inactivity-detection time (120 seconds?), and (3) add some
   randomness (std dev of 25 secs) to the inactivity-detection time.
1. BH: give all bots a bit of "it's 2026" context.
1. GM: Currently the bots aren't even being given the prompt, nor do they know
   that there was a prompt. Is this a problem?
1. LR: remove the "prompt" button entirely.
1. LR: add a "give us feedback here" button/form for reporting bugs or w/e.
1. LR: add instructions about starting a timer.
1. LR: change the title bar of chat app.
1. LR: Rename "Chat session ends" button "End chat session"? Also, the popup
   "Only exit this way when instructed" seems like it needs to be reworded for
   Prolific.
1. GM: make sure we can restart Mongo successfully. (?)


# On the fence about fixing

1. LR: "You should assume all other participants in the conversation are real
   people, and should not mention that fact at all."

1. GM: If BH to eliminate multi-topic responses doesn't work well, pick one
   random paragraph (only) from a multiple-paragraph response.

# Deciding not to address

1. Adding cursing.
1. BH: "when you perform chain of thought reasoning, only output the final
   conclusion of your reasoning. Do not overtly describe your reasoning
   process."
