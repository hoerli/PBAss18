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
        featureinfo=[]
        for i in range(data[4].__len__()):
            tempstring='Input features:\n'#todo onlick info later
            for x in range(data[3].__len__()):
                tempstring=tempstring+data[3][x]+': '+data[4][i][x]
                if(x!=data[3].__len__()-1):
                    tempstring=tempstring+'\n'
            featureinfo.append(tempstring)
        data[3]=featureinfo
        data[4]=None
        return data