# Decisions

1. We'll train bots with all data (even toxic) and self-censor them "on the way
   out" (rather than withholding toxic data during training).

## Experiment
1. We will hide the fact that we are focusing on political dialogue from
   participants before the experiment, in addition to the fact that they will
   interact with bots.
1. The experiment will begin with participants freely choosing from a small
   number of topics. This way they can "self-select out" of anything they might
   find triggering. And this way, we won't need any "abort" button.
1. Participants will be confidential not anonymous.  This means that we will
   have a key for names and #IDs.  The Informed Consent will be completed on
   the site.  When they click "continue" we will assign each participant an
   #ID and record their name for the key.  Likewise, the Debriefing Form will
   be completed on the site at the end.  Even if they consent to their data
   being submitted at the time, they will have until Nov 21 to email us to
   withdraw. 
1. We're going with an API-centric arch for fall. This is mostly because we
   think it will be easier to spin up. Latency concerns we will postpone until
   spring. Cost concerns we will price.
1. The experiment will involve: one human, one FroBot, one HotBot, and one
   CoolBot.
1. Everyone will use normal `ssh` to connect to the instance, not the `gcloud`
   set of tools that are theoretically more advanced but which are causing
   Stephen to rip his hair out.
1. We can use ChatGPT to help us refine and even suggest fine-tuning data, and
   we don't think that's a problem.
1. The highlight reels were a means to an end, we don't need to go through them
   anymore.
1. We're missing our mid-November date. Go ahead and plan for
   post-Thanksgiving.
1. We are going to full-out lie at the beginning of the experiment and tell
   them "you are talking to other people."
1. When the participant completely (from the login screen) they will first see
   a choice of topics, and will pick one. Then they will go to the chat room,
   which will have two prominent things displayed: (1) the prompt, which does
   not appear to have been written by someone else in the room, and (2) the
   first "supposedly from a user" text response, to subtly convey that this is
   an informal discussion and get the ball rolling. (Btw, the first response
   here will be from a different fruit than is assigned to any of the
   cool/hot/frobot/users.)
1. We won't police topic size/popularity. We'll give users a choice of 4
   topics, for purposes of self-selecting out of triggering topics. Then, if we
   get a lopsided set of choices, we're fine with that.
1. We will "muddy" half of our fine-tuning data by making it sound like a real
   user: shorter, clippy responses; grammar and spelling mistakes; internet
   slang; and so forth.
1. When participants begin, they will see nothing more than a screen that lets
   them enter a little code which we will give them. The system will then
   auto-assign a random fruit name, and auto-assign other fruit names to the
   three bots. At end of chat time, the bot names can be sent as HTTP
   parameters to the survey link, so that questions like "how well did Apple
   contribute to the conversation?" are populated correctly.
1. We're going to assume good faith on the part of participants (in terms of
   participants deliberately sabotaging the experiment).
1. We'll start at k minutes past the hour. We will also allow people to be late
   (up to n minutes) and we'll privately give them the instructions they
   missed.  we'll decide on values for k and n on Thursday
