import pandas as pd
import numpy as np
import torch
import json
from tqdm import tqdm
from openai import OpenAI
import re
api_key = "PUTAPIKEYHERE"
client = OpenAI(api_key = api_key)

#Toxigen samples
splits = {'test': 'annotated/test-00000-of-00001.parquet', 'train': 'annotated/train-00000-of-00001.parquet'}
toxigen = pd.read_parquet("hf://datasets/toxigen/toxigen-data/" + splits["test"])
sample1 = toxigen[["text"]].sample(n = 100)

#DIALCONAN samples
conan = pd.read_csv("hotbot_datasets/DIALOCONAN.csv")
sample2 = conan[conan["type"] == "HS"][["text"]].sample(n = 100)
sample2["source"] = ["DIALCONAN" for value in range(len(sample2))]

#CoCoLofa samples
f = open("hotbot_datasets/CoCoLofa.json")
data = json.load(f)

fallacious_comments = []

for obj in data:
  comments = obj["comments"]
  for comment in comments:
    if comment["fallacy"] != "none":
      fallacious_comments.append(comment["comment"])

fallacious_comments = np.array(fallacious_comments)
sample3 = np.random.choice(fallacious_comments, size = 100 ,replace=False)
sample3 = pd.DataFrame(data = sample3,columns=["text"])
sample3["source"] = ["CoCoLofa" for value in range(len(sample3))]

#polifact
f = open("hotbot_datasets/politifact_factcheck_data.json")

objs = []
for line in f:
  objs.append(json.loads(line))

misinfo = []
for obj in objs:
  if "verdict" in obj.keys() and "statement" in obj.keys():
    if obj["verdict"] == "false":
      misinfo.append(obj["statement"])

sample4 = pd.DataFrame(misinfo,columns=["text"])
sample4["source"] = ["polifact" for value in range(len(sample4))]
sample4 = sample4.sample(n = 100)

#make the big final sample and shuffle
samples = [sample1,sample2,sample3,sample4]
finalSample = pd.concat(samples, ignore_index=True)
finalSample = finalSample.sample(frac=1)

#Restructure and preamble stuff

#The prompt used for the model
instructions = """
You are in a data prep pipeline to prepare data for fine-tuning an LLM. You are going to be given an input comment, called Y, from social media
that has been identified as promoting unproductive dialogue. Your job is to generate a comment, called X, which gives prior context the Y comment as if Y is responding to the X comment made first.

Here are the rules you must follow when creating the X comment:
- X must be written as if a college age social media user wrote it
- At the start of X, randomly include A:,B:, or C:
- X must be a short comment
- X must frame Y as toxic by taking an opposite stance to Y
- When creating X, assume the persona of someone who has not yet seen the Y comment but is just commenting in a conversation thread on social media
- X may include swear words and may include improper punctuation or bad spelling
"""

#very very cool code down here
user_messages = []
ai_response = []
dialogue_ids = []
response_ids = []
episode_done = []
issue_labels = []

for dialogue_id in tqdm(range(len(finalSample))):
  messages = [ {"role": "system", "content": "Given an input statement, you are to generate a conversation that would lead up to such a statement being made. Generate the conversation as if it were between social media users and make sure to seperate each comment from the pretend users with a newline. Note each unique user with either A: B: or C:. You may include either 0,1, or 2 comments to preamble the comment and including no comments in the preamble is valid. Do not include more than 2 preamble comments."} ]
  text = finalSample["text"].iloc[dialogue_id]
  messages.append({"role":"user", "content":text})
  response = client.chat.completions.create(
    model = "gpt-5-mini-2025-08-07",
    messages = messages
    )
  result = response.choices[0].message.content.strip()
  arr = re.split("\n",result)
  #filler input
  for i in range(len(arr) - 1):
    dialogue_ids.append(dialogue_id)
    user_messages.append(arr[i])
    response_ids.append(i)
    issue_labels.append(finalSample["source"].iloc[dialogue_id])
    ai_response.append("(pass)")
    episode_done.append(0)

  #toxic training data input
  dialogue_ids.append(dialogue_id)
  ai_response.append(text)
  response_ids.append(len(arr) - 1)
  episode_done.append(1)
  issue_labels.append(finalSample["source"].iloc[dialogue_id])
  user_messages.append(arr[len(arr) - 1])

data = pd.DataFrame({"user_message":user_messages,"ai_response":ai_response,"dialogue_id":dialogue_ids,"response_id":response_ids,"episode_done":episode_done,"issue_labels":issue_labels})

data.to_csv("hotBotTrainingData.csv",sep=",",index=False)
