from tkinter import Frame
from tkinter import Button
from tkinter import LabelFrame
from tkinter import Entry
from tkinter import Label
from tkinter import messagebox
from tkinter import END

from services.modelDataService import ModelDataService
from gui.mainWindowGui import MainWindowGui
from gui.scrolledFrame import Scrollable
from services.KerasNNService import KerasNNService
class PredictSingleDataWindowGui(Frame):
    ''' Frame for prediction with a single tuple
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        
        mds=ModelDataService()
        self.entrys=[]
        labelframe=LabelFrame(self,text='Prediction')
        labelframe.pack(fill='x',padx=20)
        body = Frame(labelframe)
        body.pack(fill='x')


        scrollable_body = Scrollable(body)
        data=mds.getPredictDataForGui()
        if(data is not None):
            self.createImputTable(scrollable_body, data)
        else:
            messagebox.showerror('No Moded', 'No Model created or loaded')
        scrollable_body.update()
        
        labelframe=LabelFrame(self,text='Prediction')
        label=Label(labelframe,text='Prediction')
        label.pack()
        if(data is not None):
            label.config(text=str(data[1]))
        self.prediction=Entry(labelframe,readonlybackground='white')
        self.prediction.pack()
        self.prediction.config(state='readonly')
        labelframe.pack(fill='both',expand='yes',padx=20)
        
        labelframe=LabelFrame(self,text='Options')
        predictbutton=Button(labelframe,text='Predict',command=self.predictButton)
        predictbutton.pack(side='right')
        cancelbutton=Button(labelframe,text='Cancel',command=lambda: master.switch_frame(MainWindowGui))
        cancelbutton.pack(side='right') 
        labelframe.pack(fill='x',padx=20)
        if(data is None):
            predictbutton.config(state='disabled')
        if(data is not None):
            self.setDataforTesting()#only for boston data for testeing
    def setDataforTesting(self):
        self.entrys[0].insert(0,0.08829)
        self.entrys[1].insert(0,12.5)
        self.entrys[2].insert(0,7.87)
        self.entrys[3].insert(0,0)
        self.entrys[4].insert(0,0.524)
        self.entrys[5].insert(0,6.012)
        self.entrys[6].insert(0,66.6)
        self.entrys[7].insert(0,5.5605)
        self.entrys[8].insert(0,5)
        self.entrys[9].insert(0,311)
        self.entrys[10].insert(0,15.2)
        self.entrys[11].insert(0,395.6)
        self.entrys[12].insert(0,12.43)
    def createImputTable(self,scrollable_body,data):
        frame=Frame(scrollable_body)
        frame.pack(fill='x')
        for i in range(data[0].__len__()):
            entry = Entry(frame)
            entry.pack(side='left')
            entry.insert(0, str(data[0][i]))
            entry.config(state='readonly')
        frame=Frame(scrollable_body)
        frame.pack(fill='x')
        for i in range(data[0].__len__()):
            entry = Entry(frame)
            entry.pack(side='left')
            self.entrys.append(entry)
    def predictButton(self):
        knns=KerasNNService()
        predictdata=[]
        for i in range(self.entrys.__len__()):
            predictdata.append(self.entrys[i].get())
        prediction=knns.singlePredict(predictdata)
        if(prediction is None):
            messagebox.showerror('Prediction Failed', 'Control the input data')
            self.prediction.config(state='normal')
            self.prediction.delete(0, END)
            self.prediction.config(state='readonly')
        else:
            self.prediction.config(state='normal')
            self.prediction.delete(0, END)
            self.prediction.insert(0, str(prediction[0][0]))
            self.prediction.config(state='readonly')
            