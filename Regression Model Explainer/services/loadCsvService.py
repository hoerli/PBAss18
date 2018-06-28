from tools.loadCsv import loadCSV
class LoadCsvService():
    ''' Service to call the algorithms to get data from a csv file
    needs a filepath to a csv
    have different methods to get different data wich a neede in the application (look method names)
    '''
    def __init__(self,path):
        self.path=path
        self.loadcsv=loadCSV(self.path)
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
    def getGuiOutputData(self):
        data=[]
        data.append(self.path)
        data.append(self.loadcsv.getnumberOfData())
        data.append(self.loadcsv.getNumberOfInput())
        data.append(1)
        data.append(self.loadcsv.getTagList())
        for i in range(data.__len__()):
            if(data[i] is None):
                return
        return data