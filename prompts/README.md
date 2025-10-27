```
prompts/
├── experiment/
│      ...original directory...
├── hotbot/
│   ├── hotbot_prompt.txt
│   └── identities.txt
│
└── frobot/
    ├── role/
    │   ├── frobot_prompt.txt
    │   ├── human_response.txt
    │   └── reminder.txt
    │
    ├── detector/
    │   └── ... aspect detection ...
    │
    └── responder/
        └── ... aspect responses ...
```



## HotBot
1. **hotbot_prompt.txt**: Prompt HotBot to mimic it's given identity.
1. **identities.txt**: List various identities and relevant info for HotBot to mimic (45 year old white republican, 25 year old female college student, etc.).

## FroBot
### role/
1. **frobot_prompt.txt**: Inform FroBot that it is a participant in a multi-way chat and that it will detect and respond to 5 features of unproductive dialogue.
1. **human_response.txt**: Teach FroBot to respond as a human would: shorter responses, no em dashes, etc.
1. **reminder.txt**: Periodically remind FroBot of its instructions.
### detector/
1. Add prompts for detecting your aspect here as needed.  Thus we might have a bias_detect.txt.
### responder/
1. Add files here instructing FroBot to respond appropriately to your aspect.  Thus we might have a bias_respond.txt.
