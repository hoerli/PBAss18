from services.loadCsvService import LoadCsvService
from services.modelDataService import ModelDataService
from neuralnetwork.nnTopologyTest import NnTopologyTest
class TopologyTest(object):
    def __init__(self):
        self.nntt=NnTopologyTest()
    def startTest(self):
        mds=ModelDataService()
        if(not mds.isDataSetForTrain()):
            mds.resetData()
            return
        lcsvs=LoadCsvService(mds.getDataPath())
        x=lcsvs.getInputArray(mds.getOutputvar())
        y=lcsvs.getOutputArray(mds.getOutputvar())
        inputdim=lcsvs.getNumberOfInput()
        hiddenLayer=mds.getHiddenLayer()
        epoch=mds.getEpoch()
        batchsize=mds.getBatchSize()
        if(x is None):
            mds.resetData()
            return
        if(y is None):
            mds.resetData()
            return
        if(inputdim is None):
            mds.resetData()
            return
        self.nntt.setData(x, y, inputdim, hiddenLayer, epoch, batchsize)
        try:
            result=self.nntt.topologyTest()
        except:
            mds.resetData()
            return  
        mds.resetData()
        return result