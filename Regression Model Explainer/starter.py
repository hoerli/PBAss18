
#import pandas
from gui.appGui import AppGui
'''
from neuralnetwork.kerasNN import KerasNN
from services.loadCsvService import LoadCsvService
from neuralnetwork.nnTopologyTest import NnTropologyTest
'''
if __name__ == '__main__':
    
    app=AppGui()
    app.mainloop()
    '''
    lcsv=LoadCsvService('C:/Users/hurl/Desktop/bostonhousingtraindata.csv')
    X=lcsv.getInputArray('medv')
    Y=lcsv.getOutputArray('medv')
    hl=[]
    hl.append(20)
    nntro=NnTopologyTest()
    nntro.setData(X, Y, 13, hl, 100, 5)
    results=nntro.tropologTest()
    print(results.mean())
    '''