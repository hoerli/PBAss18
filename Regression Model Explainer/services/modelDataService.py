from data.modelData import ModelData
from services.loadCsvService import LoadCsvService
class ModelDataService():
    def __init__(self):
        self.md=ModelData.getInstance()
    def setModel(self,model):
        return self.md.setModel(model)
    def setEpoch(self,epoch):
        return self.md.setEpoch(epoch)
    def setDataPath(self,path):
        lcsvs=LoadCsvService(path)
        if(lcsvs.testCsv()):
            return self.md.setDataPath(path)
        else:
            return False
    def setOutputvar(self,ovar):
        return self.md.setOutputvar(ovar)
    def setHiddenLayer(self,hlay):
        return self.md.setHiddenLayer(hlay)
    def setBatchSize(self,batchsize):
        return self.md.setBatchSize(batchsize)
    def getModel(self):
        return self.md.getModel()
    def getEpoch(self):
        return self.md.getEpoch()
    def getDataPath(self):
        return self.md.getDataPath()
    def getOutputvar(self):
        return self.md.getOutputvar()
    def getHiddenLayer(self):
        return self.md.getHiddenLayer()
    def getBatchSize(self):
        return self.md.getBatchSize()
    def isDataSetForTrain(self):
        return self.md.isDataSetForTrain()