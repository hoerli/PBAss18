from services.KerasNNService import KerasNNService
from services.modelDataService import ModelDataService
from services.loadCsvService import LoadCsvService
from gui.mainMenuGui import MainMenuGui
if __name__ == '__main__':
    '''
    knns=KerasNNService()
    mds=ModelDataService()
    lcsvs=LoadCsvService('tests/bostonhousing - Kopie.csv')
    
    print(knns.createNN())
    mds.setDataPath('tests/bostonhousing - Kopie.csv')
    mds.setBatchSize(1)
    mds.setEpoch(50)
    hlay=[]
    hlay.append(16)
    hlay.append(8)
    mds.setHiddenLayer(hlay)
    mds.setOutputvar('medv')
    print(knns.createNN())
    print(knns.predict('tests/bostonhousing - Kopie.csv'))
    print(lcsvs.getOutputArray('medv'))
    print(knns.predict('tests/bostonhousing - Kopie.csv'))
    print(lcsvs.getOutputArray('medv'))
    '''
    mmgui=MainMenuGui()