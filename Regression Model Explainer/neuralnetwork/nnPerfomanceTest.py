from keras.models import Sequential
from keras.layers import Dense
class NnPerfomanceTest(object):
    ''' Perfomance Test for Neural Network
    '''
    def __init__(self):
        self.model=None
    def getHistory(self,x,y,inputdim,hiddenLayer,epoch,batchsize):
        ''' method to return the training history
        need inputaary x
        need output array y
        ned input dimension inputdim
        needs array of positiv int for the hiddenlayers and their size hiddenLayer
        needs positiv int for the runtimes threw the data epoch
        needs a positiv int for the data tubles who trained in one step batchsize
        '''
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
        model.compile(loss='mean_squared_error', optimizer='adam')
        history=model.fit(X,Y, epochs=ep, batch_size=bz)
        return history