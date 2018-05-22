from tools.loadCsv import loadCSV
class LoadCsvService():
    def __init__(self,path):
        self.loadcsv=loadCSV(path)
    def getTagList(self):
        return self.loadcsv.getTagList()
    def getnumberOfData(self):
        return self.loadcsv.getnumberOfData()
    def getNumberOfInput(self):
        return self.loadcsv.getNumberOfInput()
    def getOutputIndex(self,feature):
        return self.loadcsv.getOutputIndex(feature)
    def getOutputArray(self,feature):
        return self.loadcsv.getOutputArray(feature)
    def getInputArray(self,feature):
        return self.loadcsv.getInputArray(feature)
    def testCsv(self):
        return self.loadcsv.testCsv()