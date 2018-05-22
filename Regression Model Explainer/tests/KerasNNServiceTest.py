import unittest
from services.KerasNNService import KerasNNService
from services.modelDataService import ModelDataService

class SimpleTestCase(unittest.TestCase):
    def testCreateNNServiceTest(self):
        knns=KerasNNService()
        assert knns.createNN() == False
        mds=ModelDataService()
        mds.setDataPath('bostonhousing - Kopie.csv')
        mds.setBatchSize(4)
        mds.setEpoch(15)
        hlay=[]
        hlay.append(16)
        hlay.append(8)
        mds.setHiddenLayer(hlay)
        mds.setOutputvar('medv')
        assert knns.createNN() == True
        mds.setDataPath('emptyfile.csv')
        mds.setBatchSize(4)
        mds.setEpoch(15)
        hlay=[]
        hlay.append(16)
        hlay.append(8)
        mds.setHiddenLayer(hlay)
        mds.setOutputvar('medv')
        assert knns.createNN() == False
    def testPredictModelTest(self):
        knns=KerasNNService()
        mds=ModelDataService()
        mds.setDataPath('bostonhousing - Kopie.csv')
        mds.setBatchSize(1)
        mds.setEpoch(50)
        hlay=[]
        hlay.append(16)
        hlay.append(8)
        mds.setHiddenLayer(hlay)
        mds.setOutputvar('medv')
        knns.createNN()
        assert knns.predict('bostonhousing - Kopie.csv').__len__() == 4
        assert knns.predict('emptyfile.csv') == False
        