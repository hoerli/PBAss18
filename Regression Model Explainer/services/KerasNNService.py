import numpy as np
from neuralnetwork.kerasNN import KerasNN
from services.modelDataService import ModelDataService
from services.loadCsvService import LoadCsvService
from tools.helper import Helper
class KerasNNService():
    ''' Service for creating, training, predictions
    should work as interface between client(gui) and backends
    contains some methods for explanations who not should not called from the client -> (package explanations)
    '''
    def __init__(self):
        self.knn=KerasNN()
    def createNN(self):
        ''' method to create a model
        gets data from the ModelData singelton
        train model over KerrasNN andsave the model to its data in the ModelData singelton
        return True or False
        '''
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
            mds.resetData()
            return False
        return mds.setModel(model)
    def predictFileforGui(self,file):
        ''' method to get predictions from a file with test data
        needs a trained model
        needs a filepath with test data who fits to the trained model
        return data for the predictions
        '''
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
        ''' method to get prediction from a single tuple
        needs this tuple who fits to the model
        needs a trained model
        returns preddiction
        '''
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
        ''' method not for the interface between client(gui) and backend
        called from the explanations
        '''
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
        ''' method not for the interface between client(gui) and backend
        called from the explanations
        '''
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
        temp.append(data[3])
        temp.append(data[0])
        return temp
    def getDataForOverallExplanation(self,file):
        ''' method not for the interface between client(gui) and backend
        called from the explanations
        '''
        return self.getAllPredictionData(file)