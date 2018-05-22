from neuralnetwork.kerasNN import KerasNN
from services.modelDataService import ModelDataService
from services.loadCsvService import LoadCsvService
class KerasNNService():
    def __init__(self):
        self.knn=KerasNN()
    def createNN(self):
        mds=ModelDataService()
        if(mds.isDataSetForTrain()):
            print("ready")
            lcsvs=LoadCsvService(mds.getDataPath())
            x=lcsvs.getInputArray(mds.getOutputvar())
            y=lcsvs.getOutputArray(mds.getOutputvar())
            inputdim=lcsvs.getNumberOfInput()
            hiddenLayer=mds.getHiddenLayer()
            epoch=mds.getEpoch()
            batchsize=mds.getBatchSize()
            if(x!=False and y != False and inputdim != False):
                model=self.knn.createModel(x, y, inputdim, hiddenLayer, epoch, batchsize)
                return mds.setModel(model)
            else:
                return False
        else:
            return False
    def predict(self,testDataPath):
        no=[]
        mds=ModelDataService()
        model=mds.getModel()
        if(model!=None):
            lcsvs=LoadCsvService(testDataPath)
            InputData=lcsvs.getInputArray(mds.getOutputvar())
            if(InputData != False):
                return self.knn.predict(InputData, model)
            else:
                return no
        else:
            return no