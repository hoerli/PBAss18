from keras.models import Sequential
from keras.layers import Dense
class KerasNN():
    ''' Keras Neural Network
    to create a model
    to make predictions with a model
    '''
    def __init__(self):
        self.model=None
    def createModel(self,x,y,inputdim,hiddenLayer,epoch,batchsize):
        ''' method to specify neural network and train a model, returns this trained model
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
        model.fit(X,Y, epochs=ep, batch_size=bz)
        return model
    def predict(self,InputData,model):
        '''method to predict data returns 2dim array of predictions
        needs input array InputData
        needs a trained keras Model model
        '''
        return model.predict(InputData)   