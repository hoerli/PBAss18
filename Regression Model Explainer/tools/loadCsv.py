import csv
import numpy as np
from tools.helper import Helper
class loadCSV:
    ''' to load and get data from a csv file
    needs a filepath
    test if csv is compatible
    '''
    def __init__(self, file):
        self.datalist=self.readCsv(file)
    def getTagList(self):
        ''' method returns features of csv file
        '''
        if(self.datalist is None):
            return
        return self.datalist[0]
    def getnumberOfData(self):
        ''' method returns number of ata tuples except the feature
        '''
        if(self.datalist is None):
            return
        return (self.datalist.__len__()-1)
    def getNumberOfInput(self):
        ''' method returns number of input (input lenght minus 1 output)
        '''
        if(self.datalist is None):
            return
        return (self.datalist[0].__len__()-1)
    def getOutputIndex(self,feature):
        ''' method returns index of the output feature
        needs the output feature
        '''
        if(self.datalist is None):
            return
        temp=self.datalist[0]
        for i in range(temp.__len__()):
            if(temp[i]==feature):
                return i
        return
    def readCsv(self,file):
        ''' called in constructor
        reads csv
        test csv
        '''
        trainData= []
        try:
            with open(file) as f:
                reader = csv.reader(f)
                for row in reader:
                    trainData.append(row)
        except:
            print('except')
            return
        if(trainData.__len__()<2):
            print('too less rows')
            return
        if(trainData[0].__len__()<2):
            print('to less collum')
            return
        for i in range(trainData[0].__len__()):
            if(Helper.is_number(trainData[0][i])):
                print('no feature names')
                return
        for i in range(trainData.__len__()-1):
            for x in range(trainData[i+1].__len__()):
                if(not Helper.is_number(trainData[i+1][x])):
                    print('not digit '+trainData[i+1][x])
                    return
        collen=trainData[0].__len__()
        for i in range(trainData.__len__()):
            if(trainData[i].__len__() != collen):
                print('not same row size')
                return
        return trainData
    def getOutputArray(self,feature):
        ''' method returns the output array
        needs the output feature
        '''
        if(self.datalist is None):
            return
        outputarray=[]
        trainData=self.datalist
        index=self.getOutputIndex(feature)
        if(index != None):
            for i in range(trainData.__len__()-1):
                outputarray.append(trainData[i+1][index])
            outputarray=np.array(outputarray)
            if(outputarray.__len__()==0):
                return
            return outputarray
        return
    def getInputArray(self,feature):
        ''' method returns the input array
        needs the output feature
        '''
        if(self.datalist is None):
            return
        inputarray=[]
        trainData=self.datalist
        index=self.getOutputIndex(feature)
        if(index != None):
            for i in range(trainData.__len__()-1):
                temp=[]
                for x in range(trainData[0].__len__()):
                    if(x!=index):
                        temp.append(trainData[i+1][x])
                inputarray.append(temp)
            inputarray=np.array(inputarray)
            if(inputarray.__len__()==0):
                return
            return inputarray
        return