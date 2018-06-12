import numpy as np
from services.KerasNNService import KerasNNService
from tools.helper import Helper
class overallExplanation(object):
    def __init__(self,file):
        self.knns=KerasNNService()
        self.file=file
    def getTestData(self):
        data=self.knns.getDataForOverallExplanation(self.file)
        if(data is None):
            return
        inputdata=data[0]
        messureddata=data[1]
        featurelist=data[3]
        predictiondata=Helper.transformPredictiontoArray(data[2])
        if(predictiondata is None):
            return
        outputfeature=data[4]
        differencedata=Helper.getDiffList(messureddata, predictiondata)
        if(differencedata is None):
            return
        featurelist.append(outputfeature+', measured')
        featurelist.append(outputfeature+', predicted')
        featurelist.append('difference')
        outputdata=[]
        for i in range(inputdata.__len__()):
            temp=[]
            for x in range(inputdata[i].__len__()):
                temp.append(inputdata[i][x])
            temp.append(messureddata[i])
            temp.append(predictiondata[i])
            temp.append(differencedata[i])
            outputdata.append(temp)
        finaldata=[]
        finaldata.append(featurelist)
        finaldata.append(outputdata)
        
        positivediff=Helper.getPositiveDifference(differencedata)
        if(positivediff is None):
            return
        negativediff=Helper.getNegativeDifference(differencedata)
        if(negativediff is None):
            return
        bothdiff=Helper.getPosAndNegDiffList(differencedata)
        if(bothdiff is None):
            return
        print(differencedata)
        print(positivediff)
        print(negativediff)
        print(bothdiff)
        finaldata.append(positivediff)
        finaldata.append(negativediff)
        finaldata.append(bothdiff)
        finaldata.append(outputfeature)
        
        return finaldata