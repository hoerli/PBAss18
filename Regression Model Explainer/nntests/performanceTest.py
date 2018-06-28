from services.modelDataService import ModelDataService
from neuralnetwork.nnPerfomanceTest import NnPerfomanceTest
from services.loadCsvService import LoadCsvService
class PerformanceTest(object):
    ''' Perfomance test
    '''
    def __init__(self):
        self.nnpt=NnPerfomanceTest()
    def startTest(self):
        ''' method to run this test
        get the data for this test from the ModelData Singleton
        make the test with NnPerfomanceTest
        returns the history of this test
        '''
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
        try:
            result=self.nnpt.getHistory(x, y, inputdim, hiddenLayer, epoch, batchsize)
        except:
            mds.resetData()
            return  
        mds.resetData()
        return result