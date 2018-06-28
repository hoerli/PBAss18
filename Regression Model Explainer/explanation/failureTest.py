from services.KerasNNService import KerasNNService
class FailureTest():
    ''' Failure Test needs the test data who fits to the model as file path
    '''
    def __init__(self,file):
        self.knns=KerasNNService()
        self.file=file
    def getTestData(self):
        ''' method to get the data for the failure test
        '''
        data=self.knns.getDataForFailureTest(self.file)
        if(data is None):
            return
        try:
            data[0]=data[0].astype(float)
            data[1]=data[1].astype(float)
        except:
            return
        return data