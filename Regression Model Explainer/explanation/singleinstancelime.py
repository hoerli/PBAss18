import numpy as np
from mylime import lime_tabular
from services.modelDataService import ModelDataService
from services.loadCsvService import LoadCsvService
from tools.helper import Helper
class SingleInstanceLime():
    ''' For Test of single instance for lime
    need the input of one tuple who fits to the model
    needs an existing file path of the train data who is saved with the model
    '''
    def __init__(self,inp):
        self.mds=ModelDataService()
        self.inp=inp
    def getFigure(self):
        ''' method to get matlibplot figure from this test
        '''
        model=self.mds.getModel()
        traindatapath=self.mds.getDataPath()
        if(traindatapath is None):
            print('Train data path doesnt exist')
            return
        outputfeature=self.mds.getOutputvar()
        if(outputfeature is None):
            print('Outputfeatur is none')
            return
        
        lcsv=LoadCsvService(traindatapath)
        traindata=lcsv.getInputArray(outputfeature)
        if(traindata is None):
            print('No train data')
            return
        features=self.mds.getInputVars()
        if(features is None):
            print('No Features')
            return
        features=np.array(features)
        for i in range(self.inp.__len__()):
            x=Helper.is_number(self.inp[i])
            if(not x):
                return
        inpu=np.array(self.inp)
        try:
            inpu=inpu.astype(float)
            traindata=traindata.astype(float)
        except:
            print('to float failed')
            return
        categorical_features = np.argwhere(np.array([len(set(traindata[:,x])) for x in range(traindata.shape[1])]) <= 10).flatten()
        explainer = lime_tabular.LimeTabularExplainer(traindata, feature_names=features, class_names=['price'], categorical_features=categorical_features, verbose=True, mode='regression')
        exp = explainer.explain_instance(inpu, model.predict,num_features=features.__len__())
        #f=exp.as_pyplot_figure()
        f=exp.as_list()
        temp=Helper.transformDataForLime(f)
        finaldata=[]
        finaldata.append(temp[0])
        finaldata.append(temp[1])
        #f=exp.as_pyplot_figure()
        #finaldata.append(f)
        miv=exp.min_value
        mav=exp.max_value
        v=exp.predicted_value
        lv=exp.local_pred
        finaldata.append(miv)
        finaldata.append(mav)
        finaldata.append(v)
        finaldata.append(lv)
        finaldata.append(outputfeature)
        temp2=Helper.sortFeaturesForLime(features, inpu, temp[0])
        finaldata.append(temp2[0])
        finaldata.append(temp2[1])
        return finaldata