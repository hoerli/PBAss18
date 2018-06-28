from neuralnetwork.kerasNN import KerasNN
from services.loadCsvService import LoadCsvService
from services.modelDataService import ModelDataService
from tools.helper import Helper
class FeatureExplanation(object):
    ''' Feature Explanation
    needs test data who fits to the model
    a feature who gets explained
    and the steps in which the feature gets splitted
    '''
    def __init__(self,file,feature,steps):
        self.knn=KerasNN()
        self.file=file
        self.feature=feature
        self.steps=steps
    def getFeatureExplanationData(self):
        '''method who returns the data for the feature test
        '''
        lcsv=LoadCsvService(self.file)
        mds=ModelDataService()
        model=mds.getModel()
        if(model is None):
            return
        model_featurelist=mds.getInputVars()
        if(model_featurelist is None):
            return
        traindata_featurelist=lcsv.getTagList()
        if(traindata_featurelist is None):
            return
        outputfeature=mds.getOutputvar()
        if(outputfeature is None):
            return
        traindata_featurelist=Helper.getInputFeatureList(traindata_featurelist,outputfeature)
        if(traindata_featurelist is None):
            return
        if(not Helper.compareFeatureLists(model_featurelist, traindata_featurelist)):
            return
        
        inputdata=lcsv.getInputArray(outputfeature)
        if(inputdata is None):
            return
        featureindex=Helper.getFeaturIndex(model_featurelist, self.feature)
        if(featureindex is None):
            return
        if(not Helper.is_integer(self.steps)):
            return
        if(inputdata.__len__()<int(self.steps)):
            return
        messureddata=lcsv.getOutputArray(outputfeature)
        if(messureddata is None):
            return
        try:
            predictdata=self.knn.predict(inputdata, model)
        except:
            return
        if(predictdata is None):
            return
        messureddata=messureddata.astype(float)
        predictdata=Helper.transformPredictiontoArray(predictdata)
        predictdata=predictdata.astype(float)
        featurearray=Helper.getFeatureArray(inputdata, featureindex)
        if(featurearray is None):
            return
        featurexplanationdata=Helper.getFeatureExplanationData(featurearray, messureddata, predictdata,self.steps)
        if(featurexplanationdata is None):
            return
        labels=[]
        labels.append('Steps from-to(incl.) for '+self.feature)
        labels.append('Number in test data')
        labels.append('Measured result (min-max)')
        labels.append('Predicted result (min-max)')
        labels.append('Average (mean) measured')
        labels.append('Average (mean) predicted')
        result=[]
        result.append(labels)
        result.append(featurexplanationdata)
        return result