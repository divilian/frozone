import numpy as np
import re
import pandas as pd
import random
import os

class Log():
  def __init__(self,logText = None,exp=None):

    if logText == None:
      self.participantMap = None
      self.topic = None
      self.chatArray = None
      self.participantArray = None
      self.roomNumber = None
      self.exp = None

    else:
      a,b,c,d,e = self._splitLog_(logText)
      self.participantMap = a
      self.topic = b
      self.chatArray = c
      self.participantArray = d
      self.roomNumber = e
      self.exp = exp

  def _splitLog_(self,logText):

    roomNumber = re.findall(r"(?<==== Room )\d+(?= ===)",logText)[0]
    topic = re.findall(r"(?<=Topic: ).*" ,logText)[0]
    temp = re.split("\n--- Messages ---\n",logText)[1]
    rslt = re.split(r"\[\d+:\d+:\d+\].*(\(.*\)):",temp)[1:]
    participantArray = []
    chatArray = []
    for i in range(len(rslt)):
      if i % 2 == 0:
        participantArray.append(re.sub(r"[()]","",rslt[i]))
      else:
        chatArray.append(rslt[i])
    temp = re.findall(r"^(?:User|Bots\s*—).*$",logText,re.MULTILINE)
    usersName = re.findall(r"^User:\s*([\w.-]+)",temp[0])[0]
    botNames = re.findall(r"(\w+):\s*(\w+)", temp[1])
    participantMap = {}
    participantMap["User"] = usersName
    participantMap[botNames[0][0]] = botNames[0][1]
    participantMap[botNames[1][0]] = botNames[1][1]
    participantMap[botNames[2][0]] = botNames[2][1]

    return (participantMap,topic,chatArray,participantArray,roomNumber)

  # context window is either way so if you say 1 then you get 2 in the window plus the original human utterance.
  # returns an array of sublogs each made from the original log with only the human utterances and the included context window.
  def getHumanUtterances(self, numUtter = 0 , contextWindow = 0):

    if self.participantArray == None:
      return None
    
    allUtter = True
    if (numUtter > 0):
      allUtter = False

    participants = []
    utterances = []
    for i in range(len(self.participantArray)):
      if (self.participantArray[i] == 'User'):
        utteranceWithContext = [self.chatArray[i]]
        participantsWithinContext = [self.participantArray[i]]
        j = -1
        k = 1
        temp = contextWindow
        while (temp > 0):
          if ((i+j) >= 0 and (i+j) < len(self.chatArray)) and ((i+k) >= 0 and (i+k) < len(self.chatArray)):
            utteranceWithContext.insert(0,self.chatArray[i+j])
            utteranceWithContext.append(self.chatArray[i+k])
            participantsWithinContext.insert(0,self.participantArray[i+j])
            participantsWithinContext.append(self.participantArray[i+k])
            j -= 1
            k += 1
            temp -= 1
          else:
            break
        utterances.append(utteranceWithContext)
        participants.append(participantsWithinContext)

        if not allUtter:
          numUtter -= 1
          if numUtter <= 0:
            return self._makeLogArrayFromUtterances_(participants,utterances)
    return self._makeLogArrayFromUtterances_(participants,utterances)
  
  def _makeLogArrayFromUtterances_(self,users,utterances):
    assert len(users) == len(utterances)
    logs = []
    for i in range(len(users)):
      log = Log()
      log.chatArray=utterances[i]
      log.participantArray=users[i]
      log.roomNumber=self.roomNumber
      log.participantMap=self.participantMap
      log.topic=self.topic
      logs.append(log)
    return logs

class FileFrame():

  def __init__(self,filePath, CCHUdir = None, FCHUdir = None , dirNames = None):

    assert FCHUdir != None and CCHUdir != None

    self.initPath = filePath
    self.CCHUdir = os.path.join(self.initPath,CCHUdir)
    self.FCHUdir = os.path.join(self.initPath,FCHUdir)
    self.data = self._load_paths_(filePath,CCHUdir,FCHUdir)
    self._cleanCCHU_()
    self.len = len(self.data.loc["CCHU"])

  # get the [i,j) entries of the row element of the fileMatrix can return None
  def getLog(self, i , exp , asText = False):

    if exp == "CCHU":
      path = self.data.loc["CCHU"][i]
      if path == None:
        if (asText):
          return None
        else:
          return Log(None)
      log = None
      with open(path,"r") as f:
        log = f.read()
      if (asText):
        return log
      else:
        return Log(log,exp="CCHU")

    if exp == "FCHU":
      path = self.data.loc["FCHU"][i]
      if path == None:
        if (asText):
          return None
        else:
          return Log(None)
      log = None
      with open(path,"r") as f:
        log = f.read()
      if (asText):
        return log
      else:
        return Log(log,exp="FCHU")

    raise Exception(f"{exp} is not a valid argument for experiment")

  # get the [i,j) entries of the row element of the fileMatrix can return None
  def getLogs(self, i , j , exp , asText = False):

    if exp == "CCHU":
      returnMe = []
      for index in range(i,j):
        path = self.data.loc["CCHU"][index]
        log = None
        if path != None:
          with open(path,"r") as f:
            log = f.read()
        if (asText):
          returnMe.append(log)
        else:
          returnMe.append(Log(log,exp="CCHU"))
      return returnMe

    if exp == "FCHU":
      returnMe = []
      for index in range(i,j):
        path = self.data.loc["FCHU"][index]
        log = None
        if path != None:
          with open(path,"r") as f:
            log = f.read()
        if (asText):
          returnMe.append(log)
        else:
          returnMe.append(Log(log,exp="FCHU"))
      return returnMe

    raise Exception(f"{exp} is not a valid argument for experiment")

  def getHumanUtterances(self,contextWindow = 0,batchSize = 1,shuffle=False):
    
    assert (batchSize > 0)

    allHumanUtterances = []
    for experiment in ["CCHU","FCHU"]:
      for log in self.getLogs(0,self.len,exp=experiment):
        if log.participantArray != None:
          [allHumanUtterances.append(v) for v in log.getHumanUtterances(contextWindow=contextWindow)]

    if shuffle:
      random.shuffle(allHumanUtterances)
    
    batches = []
    batch = []
    count = 0
    for i in range(len(allHumanUtterances)):
      count += 1
      batch.append(allHumanUtterances[i])
      if count == batchSize:
        count = 0
        batches.append(batch)
        batch = []
    if len(batch) != 0:
      batches.append(batch)
  
    return batches

  def _cleanCCHU_(self):
    for i in range(len(self.data.loc["CCHU"])):
      txt = self.getLog(i,exp="CCHU",asText=True)
      if (txt != None):
        txt = re.sub(r"Frobot","Coolbot2",txt)
        with open(os.path.join(self.CCHUdir,self.data.loc["CCHU"][i]) , "w+") as f:
          f.write(txt)

  def _load_paths_(self,filePath,CCHUdir,FCHUdir):
    dirs = [os.path.join(filePath,d) for d in os.listdir(filePath) if os.path.isdir(os.path.join(filePath,d)) and not d.startswith(".")]
    index = []
    matrix = []

    for d in dirs:
      files = [os.path.join(d,f) for f in os.listdir(d) if os.path.isfile(os.path.join(d,f)) and not d.startswith(".")]
      matrix.append(files)
      if CCHUdir in d:
        index.append("CCHU")
      else:
        index.append("FCHU")

    return pd.DataFrame(data = matrix,index = index)
