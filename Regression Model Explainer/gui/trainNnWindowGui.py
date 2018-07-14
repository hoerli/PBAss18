import math
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

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from services.modelDataService import ModelDataService
from services.KerasNNService import KerasNNService
from services.nnTestService import NnTestService
from gui.mainWindowGui import MainWindowGui

class TrainNnWindowGui(Frame):
    ''' Frame for training, MSE test and perfomance test
    Shows information and a loading sequence
    with perfomance test shows a button to a plot of the result of this test
    with mse test shows the MSE,RMSE at the end of the test
    shows (messagebox) information when training is finished
    run in Threats (disable menu while running)
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        self.performencetestresultbutton=None
        self.perftesthistory=None
        
        self.master=master
        self.master.disabelMenu()
        
        mds=ModelDataService()
        dataandlabel=mds.getDataForGui()
        
        labelframe=LabelFrame(self,text='Training information')
        if(master.topologytest):
            labelframe.config(text='Evaluate Test Information')
        if(master.perfomancetest):
            labelframe.config(text='Performance Test Information')
        for i in range(dataandlabel[0].__len__()):
            self.createFrameRow(labelframe,dataandlabel[0][i], dataandlabel[1][i])
        labelframe.pack(fill='x',padx=20)
        
        self.emptyRow()
        
        self.labelframe=LabelFrame(self,text='Train Neural Network')
        if(master.topologytest):
            self.labelframe.config(text='Evaluate Neural Network')
        if(master.perfomancetest):
            self.labelframe.config(text='Performance Test')
        self.timerlabel=Label(self.labelframe,text='Timer')
        self.loadlab=Label(self.labelframe)
        self.timerlabel.pack()
        self.loadlab.pack()
        self.labelframe.pack(fill='both',expand='yes',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Options')
        self.quitButton=Button(labelframe,text='OK',command=self.quitButton)
        self.quitButton.pack()
        labelframe.pack(fill='x',padx=20)
        self.quitButton.config(state='disabled')
        
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
        self.master.switch_frame(MainWindowGui)
    def showPerformanceTestResult(self):
        if(self.perftesthistory is not None):
            self.performencetestresultbutton.destroy()
            f = Figure(figsize=(1, 1), dpi=100)
            a = f.add_subplot(111)
            a.plot(self.perftesthistory.history['loss'])
            
            
            f.suptitle('Perfomance test')
            a.set_xlabel('Epochs')
            a.set_ylabel('MSE (Mean Squared Error)')
            canvas = FigureCanvasTkAgg(f, master=self.labelframe)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')
            
            toolbar = NavigationToolbar2Tk(canvas, self.labelframe)
            toolbar.update()
            canvas._tkcanvas.pack(side='top', fill='both', expand='yes')
            #fig7, a = plt.subplots()
            #a.plot(self.perftesthistory.history['loss'])
            #plt.show()
        else:
            messagebox.showinfo('Show Result failed', 'Cant show Result of Performance Test')
class LoadingThread(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.master=master
        self.threadrun=True
        self.image=self.loadImages()
        self.topologyresult=None
        self.performanceresult=None
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
        if(self.topologyresult is not None):
            self.setTopologyResult()
        if(self.performanceresult is not None):
            self.setPerfomanceResult()
        self.master.master.enableMenu()
        self.master.quitButton.config(state='normal')
    def loadImages(self):
        images=[]
        for filename in glob.glob('loadimages/*.gif'):
            im=Image.open(filename)
            images.append(ImageTk.PhotoImage(im))
        return images
    def setTopologyResult(self):
        self.master.timerlabel.destroy()
        self.master.loadlab.destroy()
        self.master.labelframe.config(text='Evaluate Neural Network Result (MSE)')
        self.master.createFrameRow(self.master.labelframe,'MSE(mean): ',abs(self.topologyresult.mean()))
        self.master.createFrameRow(self.master.labelframe,'MSE(std): ',abs(self.topologyresult.std()))
        self.master.createFrameRow(self.master.labelframe,'MSE(mean square root): ',math.sqrt(abs(self.topologyresult.mean())))
    def setPerfomanceResult(self):
        self.master.perftesthistory=self.performanceresult
        self.master.timerlabel.destroy()
        self.master.loadlab.destroy()
        self.master.labelframe.config(text='Perfomance Test Result')
        self.master.performencetestresultbutton=Button(self.master.labelframe,text='Show Result',command=self.master.showPerformanceTestResult)
        self.master.performencetestresultbutton.pack()
class TrainThread(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.master=master
    def run(self):
        if(self.master.master.master.topologytest):
            print('Start Topology Test')
            result=NnTestService.topologyTest()
            if(result is not None):
                self.master.topologyresult=result
                messagebox.showinfo('Evaluation finished', 'Evaluation Test finished')
            else:
                messagebox.showinfo('Evaluation failed', 'Evaluation Test failed')
            self.master.master.master.topologytest=False
            print('Topology Test finished')
            self.master.threadrun=False
        elif(self.master.master.master.perfomancetest):
            print('perfomance test')
            result=NnTestService.performanceTest()
            if(result is not None):
                self.master.performanceresult=result
                messagebox.showinfo('Finished', 'Performance Test finished')
            else:
                messagebox.showinfo('Failed', 'Performance Test Failed')
            self.master.master.master.perfomancetest=False
            self.master.threadrun=False
        else:
            print('train neural network')
            knns=KerasNNService()
            isok=knns.createNN()
            if(isok):
                messagebox.showinfo('Model Created', 'The Model has been created')
            else:
                messagebox.showerror('Model not Created', 'Something went Wrong mbe check the train data (with tensorflow there is a bug mbe you have to restart the app)')
            print('model trained')
            self.master.threadrun=False