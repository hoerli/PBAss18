import unittest
from services.modelDataService import ModelDataService

class SimpleTestCase(unittest.TestCase):
    def testModel(self):
        m=ModelDataService()
        assert m.setModel(None) == False
        assert m.setModel('model') == True
        assert m.getModel() == 'model'
    def testEpoch(self):
        m=ModelDataService()
        assert m.setEpoch(-15) == False
        assert m.setEpoch("sfsdfs") == False
        assert m.setEpoch("10") == True
        assert m.setEpoch(20)== True
        assert m.getEpoch() == 20
    def testDataPath(self):
        m=ModelDataService()
        assert m.setDataPath("path") == False
        assert m.setDataPath('bostonhousing - Kopie.csv') == True
        assert m.getDataPath() == 'bostonhousing - Kopie.csv'
    def testOutputvar(self):
        m=ModelDataService()
        assert m.setOutputvar('') == False
        assert m.setOutputvar('testoutputvar') == True
        assert m.getOutputvar() == 'testoutputvar'
    def testHiddenLayer(self):
        m=ModelDataService()
        L=[]
        assert m.setHiddenLayer(L)== False
        L.append('15')
        L.append('sfsf')
        assert m.setHiddenLayer(L) == False
        L=[]
        L.append('15')
        L.append(10)
        assert m.setHiddenLayer(L)==True
        assert m.getHiddenLayer()[0] == 15
        assert m.getHiddenLayer()[1] == 10
    def testSetBatchsize(self):
        m=ModelDataService()
        assert m.setBatchSize(-15) == False
        assert m.setBatchSize("sfsdfs") == False
        assert m.setBatchSize("10") == True
        assert m.setBatchSize(20)== True
        assert m.getBatchSize() == 20
    def testIsDataSetForTrain(self):
        m=ModelDataService()
        assert m.isDataSetForTrain() == False
        m.setBatchSize(5)
        m.setDataPath('bostonhousing - Kopie.csv')
        m.setEpoch(20)
        m.setOutputvar('ovar')
        hlay=[]
        hlay.append(15)
        m.setHiddenLayer(hlay)
        assert m.isDataSetForTrain() == True