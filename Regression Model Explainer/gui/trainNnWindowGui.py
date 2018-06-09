import glob
import threading
from datetime import datetime
from time import sleep
from PIL import ImageTk,Image

from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import LabelFrame
from tkinter import messagebox

from services.modelDataService import ModelDataService
from services.KerasNNService import KerasNNService

class TrainNnWindowGui(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master=master
        self.master.disabelMenu()
        
        mds=ModelDataService()
        dataandlabel=mds.getDataForGui()
        
        labelframe=LabelFrame(self,text='Training information')
        for i in range(dataandlabel[0].__len__()):
            self.createFrameRow(labelframe,dataandlabel[0][i], dataandlabel[1][i])
        labelframe.pack(fill='x',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Train Neural Network')
        self.timerlabel=Label(labelframe,text='Timer')
        self.loadlab=Label(labelframe)
        self.timerlabel.pack()
        self.loadlab.pack()
        labelframe.pack(fill='both',expand='yes',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Options')
        self.quitButton=Button(labelframe,text='abort',command=self.quitButton)
        self.quitButton.pack()
        labelframe.pack(fill='x',padx=20)
        
        
        self.loadthread=LoadingThread(self)
        self.loadthread.daemon = True
        self.loadthread.start()
        print('text')
    def createFrameRow(self,labelframe,textlabel,textentry):
        frame=Frame(labelframe)
        label = Label(frame,width=20, text=textlabel, anchor='e')
        entry = Entry(frame,readonlybackground='white')
        entry.insert(0, str(textentry))
        entry.config(state='readonly')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
        entry.pack(side='left',fill='x',expand='yes')
        return frame
    def emptyRow(self):
        frame=Frame(self,padx=20)
        label = Label(frame,width=20, text='', anchor='e')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
    def quitButton(self):
        print('quit')
class LoadingThread(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.master=master
        self.threadrun=True
        self.image=self.loadImages()
    def run(self):
        trainthread=TrainThread(self)
        trainthread.daemon=True
        trainthread.start()
        timestamp=datetime.now()
        while(self.threadrun):
            for i in range(self.image.__len__()):
                self.master.timerlabel.config(text=str(datetime.now()-timestamp))
                self.master.loadlab.config(image = self.image[i])
                sleep(0.1)
        self.master.master.enableMenu()
    def loadImages(self):
        images=[]
        for filename in glob.glob('loadimages/*.gif'):
            im=Image.open(filename)
            images.append(ImageTk.PhotoImage(im))
        return images
class TrainThread(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.master=master
    def run(self):
        print('train neural network')
        knns=KerasNNService()
        isok=knns.createNN()
        if(isok):
            messagebox.showinfo('Model Created', 'The Model has been created')
        else:
            messagebox.showerror('Model not Created', 'Something went Wrong mbe check the train data (with tensorflow there is a bug mbe you have to restart the app)')
        print('model trained')
        self.master.threadrun=False