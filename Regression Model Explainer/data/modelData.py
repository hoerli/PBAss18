import os.path
class ModelData:
    __instance = None
    @staticmethod
    def getInstance():
        if ModelData.__instance == None:
            ModelData()
        return ModelData.__instance
    def __init__(self):
        if ModelData.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ModelData.__instance = self
        self.datapath=""
        self.outputvar=""
        self.hiddenLayer=[]
        self.epoch=0
        self.batchsize=0
        self.model=None
    def setModel(self,model):
        if(model!=None):
            self.model=None
            self.model=model
            return True
        else:
            return False
    def setEpoch(self,epoch):
            try:
                x=int(epoch)
                if(x>0):
                    self.epoch=x
                    self.model=None
                    return True
                else:
                    return False
            except:
                return False
    def setDataPath(self,path):
        if(os.path.isfile(path)):
            self.datapath=path
            self.model=None
            return True
        else:
            return False
    def setOutputvar(self,ovar):
        if(ovar!=''):
            self.outputvar=ovar
            self.model=None
            return True
        else:
            return False
    def setHiddenLayer(self,hlay):
        if(hlay.__len__()>0):
            for i in range(hlay.__len__()):
                x=hlay[i]
                try:
                    x=int(x)
                    if(x<1):
                        return False
                    hlay[i]=x
                except:
                    return False
            self.hiddenLayer=hlay
            self.model=None
            return True
        else:
            return False
    def setBatchSize(self,batchsize):
            try:
                x=int(batchsize)
                if(x>0):
                    self.batchsize=x
                    self.model=None
                    return True
                else:
                    return False
            except:
                return False
    def getModel(self):
        return self.model
    def getEpoch(self):
        return self.epoch
    def getDataPath(self):
        return self.datapath
    def getOutputvar(self):
        return self.outputvar
    def getHiddenLayer(self):
        return self.hiddenLayer
    def getBatchSize(self):
        return self.batchsize
    def isDataSetForTrain(self):
        if(self.datapath!='' and self.outputvar!='' and self.hiddenLayer.__len__()>0 and self.epoch!=0 and self.batchsize !=0):
            return True
        else:
            return False