import json
#from pathlib import Path
#x = Path.cwd() / "filePath.doesntexist"
validator = json.load(open('conditionalValidatorConfig.json'))
outputs = []

try:
   data1 = json.load(open('dummyData.json', 'r'))
   print("JSON loaded.")
except:
    print("Error loading JSON file: Please ensure file directory is correct")
    exit(0)

def getSIC(input):
    sicFound = False
    for j in validator.get("Customer").keys():
        if j.startswith("SIC"):
            for i in validator.get("Customer").get(j).get("condition"):
                if i == input.get("Customer").get("PrimarySIC").get("primaryTradingActivity").get("value"):
                    #print("SIC" + str(x))
                    #print(i)
                    sicFound = True
                    getSICTriggers(i)
    if sicFound == False:
        print("SIC not found")
    if data1.get("Customer").get("SecondarySIC") == None:
        print("No Secondary SIC exists")
    else:
        for x in range(0, len(data1.get("Customer").get("SecondarySIC"))):
            #print(j)
            #print(data1.get("Customer").get("SecondarySIC")[j].get("sicSevenCode").get("value"))
            getSICTriggers(data1.get("Customer").get("SecondarySIC")[x].get("sicSevenCode").get("value"))
    print("|----------------------------------------------------------------------|")

def getSICTriggers(code):
    for j in validator.get("Customer").keys():
        if j.startswith("SIC"):
            for i in validator.get("Customer").get(j).get("condition"):
                if i == code:
                    sicFound = True
                    print(validator.get("Customer").get(j).get("triggers")[0].get("trigger") + " " +
                          getPath(validator.get("Customer").get(j).get("triggers")[0].get("path")))

def getPath(path):
    pathSplit = path.split(".")
    returnVar = data1
    for i in pathSplit:
        #print(returnVar)
        #print(i)
        returnVar = returnVar.get(i)
    if returnVar:
        #print(type(returnVar))
        if type(returnVar).__name__ == 'dict':
            return returnVar.get("value") #Error - "value" may not exist in some instances
    else:
        return "path not found"
    
def riskCheck(input):
    print("Risk Assessment: " + switch(input.get("Customer").get("custRiskAssessment").get("value")))
    switch2(input.get("Customer").get("custRiskAssessment").get("value"))

def switch(value):
    return {
        "H" : "High",
        "M" : "Medium",
        "L" : "Low"}.get(value, "Risk value not found")

def tdd(input):
    for key in input.get("TDD").keys():
        print(key)
        getPath(input.get("TDD").get(key).get("triggers")[0].get("path"))

def switch2(value):
    if value == "H":
        outputs.append("H")
 
def inputFDDChecker(outputs):
    if outputs != []:
        print("FDD Failure")
    else:
        print("FDD Viable")
 
getSIC(data1)
riskCheck(data1)
print(outputs)
inputFDDChecker(outputs)
#tdd(validator)
'''
def checkNamesRec(dict):
    if type(dict).__name__ != 'str' and type(dict).__name__ != 'int' and type(dict).__name__ != 'float':
        for key in dict.keys():
            if key.__contains__ ("UID"):
                print(key)
            if type(dict.get(key)).__name__ == 'list':
                for item in range(0, len(dict.get(key))):
                    checkNamesRec(dict.get(key)[item])
            else:
                checkNamesRec(dict.get(key))
'''
#checkNamesRec(validator)