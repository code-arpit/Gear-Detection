import json
configfile = open("config.json",'r')
configData = configfile.read()
configDict = json.loads(configData)
# print(configDict)

def getApplication_Name():
    return configDict["Application_Name"]

def getVideo_Source():
    return configDict["Video_Source"]

def getStorage_Path():
    return configDict["Storage_Path"]

def getFile_Type():
    return configDict["File_Type"]

def getBilateralFilter_sigmaColor():
    return configDict["BilateralFilter_sigmaColor"]

def getBilateralFilter_sigmaSpace():
    return configDict["BilateralFilter_sigmaSpace"]

def getMedian_Blurr():
    return configDict["Median_Blurr"]

def getCanny_thresh1():
    return configDict["Canny_thresh1"]

def getCanny_thresh2():
    return configDict["Canny_thresh2"]

def getMin_Near_Curve():
    return configDict["Min_Near_Curve"]

