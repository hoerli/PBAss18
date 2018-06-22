from keras.models import Sequential
from keras.layers import Dense
class NnPerfomanceTest(object):
    def __init__(self):
        self.model=None
    def getHistory(self,x,y,inputdim,hiddenLayer,epoch,batchsize):
        inputDim=int(inputdim)
        
        ep=int(epoch)
        bz=int(batchsize)
        X=x
        Y=y
        
        
        
        model = Sequential()
        print('add')
        model.add(Dense(int(hiddenLayer[0]), input_dim=inputDim, kernel_initializer='normal', activation='relu'))
        for i in range(hiddenLayer.__len__()-1):
            print('add')
            model.add(Dense(int(hiddenLayer[i+1]), kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        # Compile model
        model.compile(loss='mean_squared_error', optimizer='adam')
        
        history=model.fit(X,Y, epochs=ep, batch_size=bz)
        
        return history
