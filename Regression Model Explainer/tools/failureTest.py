from services.loadCsvService import LoadCsvService
from services.modelDataService import ModelDataService
from services.KerasNNService import KerasNNService
import numpy as np
class FailureTest():
    def __init__(self):
        self.data=[]
    def getTestData(self,file):
        lcsvs=LoadCsvService(file)
        mds=ModelDataService()
        nns=KerasNNService()
        feature=mds.getOutputvar()
        if(feature != ''):
            measured=lcsvs.getOutputArray(feature)
            predict=nns.predict(file)
            if(predict.__len__()>0 and measured != False):
                try:
                    measured=measured.astype(np.float)
                    self.data.append(predict)
                    self.data.append(measured)
                except:
                    return self.data
        return self.data
            
        