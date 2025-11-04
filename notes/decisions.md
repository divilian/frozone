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
