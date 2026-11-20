from abc import ABC,abstractmethod
import random
import json
import numpy as np
from transformers import pipeline
import torch
import re

class Model(ABC):

  def __init__(self,prompt,aspects,modelName,experiments):
    self.aspectMap = {}
    self.aspects = aspects
    self.numAspects = len(aspects)
    for i in range(len(aspects)):
      self.aspectMap[i] = aspects[i]
    self.prompt = prompt
    self.ogPrompt = prompt
    self.curLog = None
    self.curLogName = None
    self.labeledLogs = {}
    self.name = modelName
    self.experiments = experiments

  @abstractmethod
  def labelCurLog(self):
    pass

  @abstractmethod
  def loadIn(self):
    pass

  def prepare(self,log,logName):
    self.curLog = log
    self.curLogName = logName
    self.labeledLogs[self.curLogName] = [np.zeros(self.numAspects).tolist() for v in range(len(self.curLog.chatArray))]

  def writeToFile(self,dir,fileName = None):
    self.labeledLogs["metadata"] = {"aspects":self.aspectMap,"prompt":self.prompt,"modelName":self.name,"experiments":self.experiments}
    if fileName == None:
      with open(f"{dir}/{self.name}_labeledLogs.json", 'w') as file:
        json.dump(self.labeledLogs, file, indent=4)
      return f"{dir}/{self.name}_labeledLogs.json"
    else:
      with open(f"{dir}/{fileName}", 'w') as file:
        json.dump(self.labeledLogs, file, indent=4)
      return f"{dir}/{fileName}"

class TestingModel(Model):

    def __init__(self,prompt,aspects,modelName,experiments):
      super().__init__(prompt,aspects,modelName,experiments)

    def labelCurLog(self):
      for i in range(len(self.curLog.chatArray)):
        for j in range(self.numAspects):
          ranking = random.randint(1, 10)
          self.labeledLogs[self.curLogName][i][j] += ranking

    def loadIn(self):
      pass

    def prepare(self,log,logName):
      super().prepare(log,logName)

class FreeHFModel(Model):
    def __init__(self,prompt,aspects,modelName,experiments):
      super().__init__(prompt,aspects,modelName,experiments)
      self.pipe = None
      self.messages = None

    def labelCurLog(self):
      for i in range(len(self.curLog.chatArray)):
        chat = self.curLog.chatArray[i]
        while (True):
          current_messages = self.messages + [{"role": "user", "content": chat}]
          outputs = self.pipe(current_messages,max_new_tokens=256)
          answer = None
          try:
            answer = json.loads(re.findall(r"ANSWER_START(\[.*?\])ANSWER_END",outputs[0]["generated_text"][2]["content"])[0])
            if len(answer) != len(self.aspects):
              raise Exception("too much")
            break
          except:
            print("Bad Answer Trying Again")
            pass
        torch.cuda.empty_cache()
        self.labeledLogs[self.curLogName][i] = answer


    def loadIn(self):
      self.pipe = pipeline("text-generation", model="google/gemma-4-26B-A4B-it")

    def prepare(self,log,logName):
      super().prepare(log,logName)
      self.prompt = self.ogPrompt
      self.prompt = re.sub("CHAT_LOG_HERE","\n".join(log.chatArray), self.prompt)
      self.messages = [{"role":"system","content":self.prompt}]