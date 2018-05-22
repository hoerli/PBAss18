import csv
import numpy as np
class loadCSV:
    def __init__(self, path):
        self.path=path
    def getTagList(self):
        if(self.testCsv()):
            return self.readCsv()[0]
        else:
            return False
    def getnumberOfData(self):
        if(self.testCsv()):
            return (self.readCsv().__len__()-1)
        else:
            return False
    def getNumberOfInput(self):
        if(self.testCsv()):
            return (self.readCsv()[0].__len__()-1)
        else:
            return False
    def getOutputIndex(self,feature):
        if(self.testCsv()):
            temp=self.readCsv()[0]
            for i in range(temp.__len__()):
                if(temp[i]==feature):
                    return i
            return None
        else:
            return None
    def readCsv(self):
        trainData= []
        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                trainData.append(row)
        return trainData
    def getOutputArray(self,feature):
        if(self.testCsv()):
            outputarray=[]
            trainData=self.readCsv()
            index=self.getOutputIndex(feature)
            if(index != None):
                for i in range(trainData.__len__()-1):
                    outputarray.append(trainData[i+1][index])
                outputarray=np.array(outputarray)
                return outputarray
            else:
                return False
        else:
            return False
    def getInputArray(self,feature):
        if(self.testCsv()):
            inputarray=[]
            trainData=self.readCsv()
            index=self.getOutputIndex(feature)
            if(index != None):
                for i in range(trainData.__len__()-1):
                    temp=[]
                    for x in range(trainData[0].__len__()):
                        if(x!=index):
                            temp.append(trainData[i+1][x])
                    inputarray.append(temp)
                inputarray=np.array(inputarray)
                return inputarray
            else:
                return False
        else:
            return False
    def testCsv(self):
        try:
            trainData=self.readCsv()
            if(trainData.__len__()==0):
                return False
        except:
            return False
        #Todo Test on features, test on empty column
        return True