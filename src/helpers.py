import numpy as np
import re

class Log():
  def __init__(self,logText):
    
    if logText == None:
      self.participantMap = None
      self.topic = None
      self.chatArray = None
      self.participantArray = None
      self.roomNumber = None
    else:
      a,b,c,d,e = self._splitLog_(logText)
      self.participantMap = a
      self.topic = b
      self.chatArray = c
      self.participantArray = d
      self.roomNumber = e
  
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
        return Log(log)

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
        return Log(log)

    raise Exception(f"{exp} is not a valid argument for experiment")

  # get the [i,j) entries of the row element of the fileMatrix can return None
  def getLogs(self, i , j , exp , asText = False):

    if exp == "CCHU":
      returnMe = ["" for v in range(i,j)]
      for index in range(i,j):
        path = self.data.loc["CCHU"][index]
        log = None
        if path != None:
          with open(path,"r") as f:
            log = f.read()
        if (asText):
          returnMe[index] = log
        else:
          returnMe[index] = Log(log)
      return returnMe

    if exp == "FCHU":
      returnMe = ["" for v in range(i,j)]
      for index in range(i,j):
        path = self.data.loc["FCHU"][index]
        log = None
        if path != None:
          with open(path,"r") as f:
            log = f.read()
        if (asText):
          returnMe[index] = log
        else:
          returnMe[index] = Log(log)
      return returnMe

    raise Exception(f"{exp} is not a valid argument for experiment")

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
