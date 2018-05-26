import os.path
import pickle
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
    def resetData(self):
        self.datapath=""
        self.outputvar=""
        self.hiddenLayer=[]
        self.epoch=0
        self.batchsize=0
        self.model=None
    def getDataForSave(self):
        temp=[]
        temp.append(self.datapath)
        temp.append(self.outputvar)
        temp.append(self.hiddenLayer)
        temp.append(self.epoch)
        temp.append(self.batchsize)
        temp.append(self.model)
        return temp
    def saveModel(self,path):
        if(self.isDataSetForTrain() and self.model!=None):
            file=path+'.model'
            data=self.getDataForSave()
            try:
                output = open(file, 'wb')
                pickle.dump(data, output)
                output.close()
                return True
            except:
                return False
        else:
            return False
    def loadModel(self,path):
        self.resetData()
        try:
            inp = open(path,'rb')
            data = pickle.load(inp)
            inp.close()
            t1=self.setDataPath(data[0])
            t2=self.setOutputvar(data[1])
            t3=self.setHiddenLayer(data[2])
            t4=self.setEpoch(data[3])
            t5=self.setBatchSize(data[4])
            t6=self.setModel(data[5])
            if(t1 and t2 and t3 and t4 and t5 and t6):
                return True
            else:
                self.resetData()
                return False
        except:
            self.resetData()
            return False