import pandas as pd
import sys
import numpy as np
import seaborn as sns
import sys
import json
from tqdm import tqdm
import convokit #This is a very very cool package def need to cite it https://convokit.cornell.edu/
import pprint
from convokit import Corpus, download
import numpy as np

def get_sub(sub , write_name):
    bigCorpus = None
    try:
        bigCorpus = Corpus(download(sub))
    except Exception as e:
        print("There was an error. Check the sub name it may not be tracked by convokit\n\n")
        raise e
    bigCorpus.print_summary_stats()

    user_messages = []
    ai_responses = []
    dialogue_ids = []
    response_ids = []
    episode_done = []
    issue_labels = []

    RESPONSE_PROB = 0.50
    issue_label = "[]"
    dialogue_id = 0

    for convo in tqdm(bigCorpus.iter_conversations(),total=499):

      try:
        corpus = [utterance for utterance in convo.traverse(traversal_type = "dfs")]
        response_id = 0

        for i in range(len(corpus)):

          #gets user response
          msg = corpus[i]
          if "moderator" not in msg.get_speaker().id.lower() and "[removed]" not in msg.text.lower() and "[deleted]" not in msg.text.lower():
            usr_msg = msg.text
            ai_msg = "(pass)"

            #gets ai response
            if i + 1 < len(corpus) and np.random.choice([True,False] , p = [RESPONSE_PROB , 1-RESPONSE_PROB]):
              i += 1
              txt = corpus[i]
              if "moderator" not in txt.get_speaker().id.lower() and "[removed]" not in txt.text.lower() and "[deleted]" not in txt.text.lower():
                ai_msg = txt.text
              else:
                i -= 1

            #adds ts to the lists
            dialogue_ids.append(dialogue_id)
            response_ids.append(response_id)
            user_messages.append(usr_msg)
            ai_responses.append(ai_msg)
            issue_labels.append(issue_label)
            episode_done.append(0)
            response_id += 1

        episode_done.pop(-1)
        episode_done.append(1)
        dialogue_id += 1
      except:
        pass

    data = pd.DataFrame({"user_message":user_messages,"ai_response":ai_responses,"dialogue_id":dialogue_ids,"response_id":response_ids,"episode_done":episode_done,"issue_labels":issue_labels})

    data.to_csv(write_name)
    return "Beans are very cool"

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python make_coolbot_data.py subreddit write/path")

    else:
        sub = sys.argv[1]
        writeName = sys.argv[2]
        
        if writeName[len(writeName) - 4 :] != ".csv":
            writeName = writeName + ".csv"

        get_sub(sub , writeName)
