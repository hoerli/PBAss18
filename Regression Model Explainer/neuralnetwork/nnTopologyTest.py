import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
class NnTopologyTest(object):
    def __init__(self):
        self.x=None
        self.y=None
        self.inputdim=None
        self.hiddenLayer=None
        self.epoch=None
        self.batchsize=None
    def setData(self,x,y,inputdim,hiddenLayer,epoch,batchsize):
        self.x=x
        self.y=y
        self.inputdim=inputdim
        self.hiddenLayer=hiddenLayer
        self.epoch=epoch
        self.batchsize=batchsize
    def getModel(self):
        print('create model')
        inputDim=int(self.inputdim)
        
        model = Sequential()
        print('add hidden layer size: '+str(self.hiddenLayer[0]))
        model.add(Dense(int(self.hiddenLayer[0]), input_dim=inputDim, kernel_initializer='normal', activation='relu'))
        for i in range(self.hiddenLayer.__len__()-1):
            print('add hidden layer size: '+str(self.hiddenLayer[i+1]))
            model.add(Dense(int(self.hiddenLayer[i+1]), kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        # Compile model
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model
    def topologyTest(self):
        ep=int(self.epoch)
        bz=int(self.batchsize)
        X=self.x
        Y=self.y
        X=X.astype(float)
        Y=Y.astype(float)
        
        seed = 7

        np.random.seed(seed)
        estimator = KerasRegressor(build_fn=self.getModel, epochs=ep, batch_size=bz, verbose=0)
        kfold = KFold(n_splits=10, random_state=seed)
        results = cross_val_score(estimator, X, Y, cv=kfold)
        return results