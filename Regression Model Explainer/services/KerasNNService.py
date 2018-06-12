import numpy as np
from neuralnetwork.kerasNN import KerasNN
from services.modelDataService import ModelDataService
from services.loadCsvService import LoadCsvService
from tools.helper import Helper
class KerasNNService():
    def __init__(self):
        self.knn=KerasNN()
    def createNN(self):
        mds=ModelDataService()
        if(not mds.isDataSetForTrain()):
            mds.resetData()
            return False
        lcsvs=LoadCsvService(mds.getDataPath())
        x=lcsvs.getInputArray(mds.getOutputvar())
        y=lcsvs.getOutputArray(mds.getOutputvar())
        inputdim=lcsvs.getNumberOfInput()
        hiddenLayer=mds.getHiddenLayer()
        epoch=mds.getEpoch()
        batchsize=mds.getBatchSize()
        if(x is None):
            mds.resetData()
            return False
        if(y is None):
            mds.resetData()
            return False
        if(inputdim is None):
            mds.resetData()
            return False
        try:
            model=self.knn.createModel(x, y, inputdim, hiddenLayer, epoch, batchsize)
        except:
            return False
        return mds.setModel(model)
    def predictFileforGui(self,file):#Todo make it mor generic -> getallPredictionData
        lcsv=LoadCsvService(file)
        mds=ModelDataService()
        
        model_featurelist=mds.getInputVars()
        if(model_featurelist is None):
            return
        traindata_featurelist=lcsv.getTagList()
        if(traindata_featurelist is None):
            return
        outputfeature=mds.getOutputvar()
        if(outputfeature is None):
            return
        traindata_featurelist=Helper.getInputFeatureList(traindata_featurelist,outputfeature)
        if(traindata_featurelist is None):
            return
        if(not Helper.compareFeatureLists(model_featurelist, traindata_featurelist)):
            return
        
        inputdata=lcsv.getInputArray(outputfeature)
        if(inputdata is None):
            return
        messureddata=lcsv.getOutputArray(outputfeature)
        if(messureddata is None):
            return
        data=[]
        featurelist=model_featurelist
        '''
        for i in range(model_featurelist.__len__()):
            featurelist.append(model_featurelist[i])
        '''
        featurelist.append(outputfeature+', measured')
        featurelist.append(outputfeature+', predicted')
        data.append(featurelist)
        
        try:
            predictdata=self.knn.predict(inputdata, mds.getModel())
        except:
            return
        datalist=[]
        for i in range(inputdata.__len__()):
            temp=[]
            for x in range(inputdata[i].__len__()):
                temp.append(inputdata[i][x])
            temp.append(messureddata[i])
            temp.append(str(predictdata[i][0]))
            datalist.append(temp)
        data.append(datalist)
        return data
    def singlePredict(self,data):
        mds=ModelDataService()
        model=mds.getModel()
        inputarray=[]
        inputarray.append(data)
        inputdata=np.array(inputarray)
        if(model is None):
            return
        try:
            return self.knn.predict(inputdata, model)
        except:
            return
    def getAllPredictionData(self,file):
        lcsv=LoadCsvService(file)
        mds=ModelDataService()
        
        model_featurelist=mds.getInputVars()
        if(model_featurelist is None):
            return
        traindata_featurelist=lcsv.getTagList()
        if(traindata_featurelist is None):
            return
        outputfeature=mds.getOutputvar()
        if(outputfeature is None):
            return
        traindata_featurelist=Helper.getInputFeatureList(traindata_featurelist,outputfeature)
        if(traindata_featurelist is None):
            return
        if(not Helper.compareFeatureLists(model_featurelist, traindata_featurelist)):
            return
        
        inputdata=lcsv.getInputArray(outputfeature)
        if(inputdata is None):
            return
        messureddata=lcsv.getOutputArray(outputfeature)
        if(messureddata is None):
            return
        featurelist=[]
        for i in range(model_featurelist.__len__()):
            featurelist.append(model_featurelist[i])
        try:
            predictdata=self.knn.predict(inputdata, mds.getModel())
        except:
            return
        data=[]
        data.append(inputdata)
        data.append(messureddata)
        data.append(predictdata)
        data.append(featurelist)
        data.append(outputfeature)
        return data
    def getDataForFailureTest(self,file):
        data=self.getAllPredictionData(file)
        if(data is None):
            return
        tempprediction=data[2]
        prediction=[]
        for i in range(tempprediction.__len__()):
            prediction.append(str(tempprediction[i][0]))
        prediction=np.array(prediction)
        temp=[]
        temp.append(data[1])
        temp.append(prediction)
        temp.append(data[4])
        return temp
    def getDataForOverallExplanation(self,file):
        return self.getAllPredictionData(file)