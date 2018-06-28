from data.modelData import ModelData
from services.loadCsvService import LoadCsvService
from tools.helper import Helper
class ModelDataService():
    ''' Service to get and set data for the model (inkl model)
    creates a singelton if no singleton object is created or load the singlton object from ModelData
    '''
    def __init__(self):
        self.md=ModelData.getInstance()
    def setModel(self,model):
        return self.md.setModel(model)
    def setEpoch(self,epoch):
        return self.md.setEpoch(epoch)
    def setDataPath(self,path):
        return self.md.setDataPath(path)
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
    def saveModel(self,path):
        return self.md.saveModel(path)
    def loadModel(self,path):
        return self.md.loadModel(path)
    def resetData(self):
        self.md.resetData()
    def setInputVars(self,inputvars):
        return self.md.setInputVars(inputvars)
    def getInputVars(self):
        return self.md.getInputVars()
    def printAll(self):
        '''method to print data who save in the ModelData object
        '''
        print('Datapath')
        print(self.md.datapath)
        print('Outputvar')
        print(self.md.outputvar)
        print('HiddenLaye')
        print(self.md.hiddenLayer)
        print('Epoch')
        print(self.md.epoch)
        print('Batchsize')
        print(self.md.batchsize)
        print('Model')
        print(self.md.model)
    def setDataFromGui(self,file,outputvar,hiddenlayer,epoch,batchsize):
        ''' set all the data except the model itself in the ModelData singleton
        interface between client(gui) and backend
        '''
        self.resetData()
        isok=self.setDataPath(file)
        if(not isok):
            self.resetData()
            return False
        isok=self.setOutputvar(outputvar)
        if(not isok):
            self.resetData()
            return False
        isok=self.setHiddenLayer(hiddenlayer)
        if(not isok):
            self.resetData()
            return False
        isok=self.setEpoch(epoch)
        if(not isok):
            self.resetData()
            return False
        isok=self.setBatchSize(batchsize)
        if(not isok):
            self.resetData()
            return False
        lcsv=LoadCsvService(self.getDataPath())
        inputfeaturelist=Helper.getInputFeatureList(lcsv.getTagList(), self.getOutputvar())
        isok=self.setInputVars(inputfeaturelist)
        if(not isok):
            self.resetData()
            return False
        return True
    def getDataForGui(self):
        ''' method to get data of the ModelData singelton for gui
        adds names for this data
        returns list with this data for gui
        interface between client(gui) and backend
        '''
        lcsv=LoadCsvService(self.getDataPath())
        data=[]
        label=[]
        dataandlabel=[]
        label.append('Filepath')
        data.append(self.getDataPath())
        label.append('Number of Data Tuples')
        data.append(lcsv.getnumberOfData())
        label.append('Inputlayer Size')
        data.append(lcsv.getNumberOfInput())
        label.append('Outputlayer Size')
        data.append('1')
        label.append('Output feature')
        data.append(self.getOutputvar())
        label.append('Input features')
        data.append(self.getInputVars())
        label.append('Epoch')
        data.append(self.getEpoch())
        label.append('Batchsize')
        data.append(self.getBatchSize())
        label.append('Hidden Layers')
        data.append(self.getHiddenLayer())
        dataandlabel.append(label)
        dataandlabel.append(data)
        return dataandlabel
    def getModelInformationForGui(self):
        ''' interface between client(gui) and backend
        '''
        dataandlabel=self.getDataForGui()
        label='Model'
        model=self.getModel()
        if(model is None):
            return None
        model=str(model)
        dataandlabel[0].append(label)
        dataandlabel[1].append(model)
        return dataandlabel
    def getPredictDataForGui(self):
        ''' method to get data for predictions
        input and output feature names
        add string to output
        interface between client(gui) and backend
        '''
        data=[]
        inputvars=self.getInputVars()
        outputvars=self.getOutputvar()
        if(inputvars is None):
            return
        if(outputvars is None):
            return
        if(self.getModel() is None):
            return
        outputvars=outputvars+': prediction'
        data.append(inputvars)
        data.append(outputvars)
        return data