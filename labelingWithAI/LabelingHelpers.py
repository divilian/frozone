from ChatLogHelpers import *
from Models import *
import json

def labelAllUsingModel(model,fileFrame,experiments):
  for exp in experiments:
    i = 0
    for log in fileFrame.getLogs(0,fileFrame.len,exp):
      if log.exists:
        model.prepare(log,f"{model.name}_{exp}_Log{i}")
        model.labelCurLog()
        i += 1
  return model.labeledLogs

def labelLogs(currentDirectory,experiments,models,fileFrame):
  paths = []
  for name,model in models.items():
    model.loadIn()
    labelAllUsingModel(model,fileFrame,experiments)
    path = model.writeToFile(currentDirectory)
    paths.append(path)
    del model
  return paths

# Not the cleanest way to to this but it works so whateva
def combineJSON(currentDirectory,paths,fileName=None):
  maxKeys = 0
  overall = {"metadata":{"models":[],"experiments":[],"aspects":{}}}
  for path in paths:
    with open(path, "r") as file:
      data = json.load(file)


    overall["metadata"]["aspects"][data["metadata"]["modelName"]] = data["metadata"]["aspects"]

    overall[data["metadata"]["modelName"]] = {}
    overall["metadata"]["models"].append(data["metadata"]["modelName"])

    for exp in data["metadata"]["experiments"]:
      overall[data["metadata"]["modelName"]][exp] = []
      if exp not in overall["metadata"]["experiments"]:
        overall["metadata"]["experiments"].append(exp)

    count = 0
    for key in data.keys():
      if key != "metadata":
        temp = key[key.index("_") + 1:]
        exp = temp[0:temp.index("_")]
        overall[data["metadata"]["modelName"]][exp].append(data[key])
        count += 1

    if count > maxKeys:
      maxKeys = count

  overall["metadata"]["maxNumberOfLogs"] = maxKeys
  if fileName == None:
    with open(f"{currentDirectory}/Overall.json", 'w') as file:
      json.dump(overall, file, indent=4)
    return f"{currentDirectory}/Overall.json"
  else:
    with open(f"{dir}/{fileName}", 'w') as file:
      json.dump(overall, file, indent=4)
    return f"{dir}/{fileName}"