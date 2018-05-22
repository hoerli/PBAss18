from keras.models import Sequential
from keras.layers import Dense
class KerasNN():
    def __init__(self):
        self.model=None
    def createModel(self,x,y,inputdim,hiddenLayer,epoch,batchsize):
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
        
        model.fit(X,Y, epochs=ep, batch_size=bz)
        return model
    def predict(self,InputData,model):
        no=[]
        try:
            return model.predict(InputData)
        except:
            print('Fail predict')
            return no
        