from Models import *
from ChatLogHelpers import *
from LabelingHelpers import *

def main():

  # Edit here to change the prompt
  prompt = None
  with open("/content/Prompt.txt","r") as f:
    prompt = f.read()

  # Edit here to change what the aspects are
  aspects = ["intoToxic","addressedToxic","introFallacy","addressedFallacy","introBias","addressedBias","intoMisinfo","addressedMisinfo"]

  # Edit here to change the current directory
  pwd="/content/drive/MyDrive"

  # Edit here to change the experiments really should not touch though because its kinda icky code and I dont want to fix
  experiments = ["FCHU","CCHU"]

  # Edit here for where the data comes from and the directories for the two experiments
  dataDir = "/content/drive/MyDrive/Frozone_Data_Use"
  CCHU = "CCHU"
  FFCHU = "FCHU"

  # This is the most important part where you define what models are going to be used. All models should be defined in models.py and imported
  # The format here is modelName:Model
  model1 = FreeHFModel(prompt,aspects,"HFmodel1",experiments)
  model2 = FreeHFModel(prompt,aspects,"HFmodel2",experiments)
  models = {"HFmodel1":model1,"HFmodel2":model2}

  # Finally, this is where the actual work is done.
  data = FileFrame(dataDir,CCHUdir="CCHU",FCHUdir="FCHU")
  paths = labelLogs(pwd,experiments,models,data)

  # This part just combines everything into a single json file
  overallPath = combineJSON(pwd,paths)

  print(f"The data is located at {overallPath}.\nIndividual items are in {paths}")