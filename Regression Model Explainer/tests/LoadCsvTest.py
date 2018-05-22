import unittest
from services.loadCsvService import LoadCsvService

class SimpleTestCase(unittest.TestCase):
    def testTagList(self):
        lcsvs=LoadCsvService('bostonhousing - Kopie.csv')
        assert lcsvs.getTagList().__len__() == 14
        lcsvs=LoadCsvService('emptyfile.csv')
        assert lcsvs.getTagList() == False
    def testGetNumberOfData(self):
        lcsvs=LoadCsvService('bostonhousing - Kopie.csv')
        assert lcsvs.getnumberOfData() == 4
        lcsvs=LoadCsvService('emptyfile.csv')
        assert lcsvs.getnumberOfData() == False
    def testGetNumberOfInput(self):
        lcsvs=LoadCsvService('bostonhousing - Kopie.csv')
        assert lcsvs.getNumberOfInput() == 13
        lcsvs=LoadCsvService('emptyfile.csv')
        assert lcsvs.getNumberOfInput() == False
    def testGetOutputIndex(self):
        lcsvs=LoadCsvService('bostonhousing - Kopie.csv')
        assert lcsvs.getOutputIndex('crim') == 0
        assert lcsvs.getOutputIndex('sffsd') == None
        lcsvs=LoadCsvService('emptyfile.csv')
        assert lcsvs.getOutputIndex('crim') == None
    def testGetOutputArray(self):
        lcsvs=LoadCsvService('bostonhousing - Kopie.csv')
        assert lcsvs.getOutputArray('fsdfs') == False
        assert lcsvs.getOutputArray('crim').__len__() == 4
        lcsvs=LoadCsvService('emptyfile.csv')
        assert lcsvs.getOutputArray('fsdfs') == False
        assert lcsvs.getOutputArray('crim') == False
    def testGetInputArray(self):
        lcsvs=LoadCsvService('bostonhousing - Kopie.csv')
        assert lcsvs.getInputArray('fsdfs') == False
        assert lcsvs.getInputArray('crim').shape == (4,13)
        lcsvs=LoadCsvService('emptyfile.csv')
        assert lcsvs.getInputArray('fsdfs') == False
        assert lcsvs.getInputArray('crim') == False
        