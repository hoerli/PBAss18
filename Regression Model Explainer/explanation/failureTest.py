from services.KerasNNService import KerasNNService
class FailureTest():
    def __init__(self,file):
        self.knns=KerasNNService()
        self.file=file
    def getTestData(self):
        data=self.knns.getDataForFailureTest(self.file)
        if(data is None):
            return
        try:
            data[0]=data[0].astype(float)
            data[1]=data[1].astype(float)
        except:
            return
        return data