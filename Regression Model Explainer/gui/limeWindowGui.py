import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import messagebox
from tkinter import Button
from tkinter import Entry
from tkinter.ttk import Notebook
from gui.scrolledFrame import Scrollable
from gui.mainWindowGui import MainWindowGui
from services.modelDataService import ModelDataService
from services.explanationService import ExplanationService
class LimeWindowGui(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        
        nb=Notebook(self)
        nb.pack(side='left',fill='both',expand='yes')
        
        tab1=Frame()
        nb.add(tab1,text='Lime')
        
        mds=ModelDataService()
        self.entrys=[]
        labelframe=LabelFrame(tab1,text='Input Data')
        labelframe.pack(fill='both',expand='yes',padx=20)
        body = Frame(labelframe)
        body.pack(fill='both',expand='yes')
        

        scrollable_body = Scrollable(body)
        data=mds.getPredictDataForGui()
        if(data is not None):
            self.createImputTable(scrollable_body, data)
        else:
            messagebox.showerror('No Moded', 'No Model created or loaded')
        scrollable_body.update()
        
        labelframe=LabelFrame(tab1,text='Options')
        testbutton=Button(labelframe,text='Test',command=self.testButton)
        testbutton.pack(side='right')
        cancelbutton=Button(labelframe,text='Cancel',command=lambda: master.switch_frame(MainWindowGui))
        cancelbutton.pack(side='right') 
        labelframe.pack(fill='x',padx=20)
        if(data is None):
            testbutton.config(state='disabled')
        tab2=Frame()
        nb.add(tab2,text='Lime Daigramm')
        self.limelabelframe=LabelFrame(tab2,text='Lime Diagramm (weights to result)')
        self.limeframe=Frame(self.limelabelframe)
        self.limeframe.pack(fill='both',expand='yes')
        self.limelabelframe.pack(fill='both',expand='yes',padx=20)
        
        tab3=Frame()
        nb.add(tab3,text='Feature Info')
        self.featurelabelframe=LabelFrame(tab3,text='Feature Info')
        self.featureframe=Frame(self.featurelabelframe)
        self.featureframe.pack(fill='both',expand='yes')
        self.featurelabelframe.pack(fill='both',expand='yes',padx=20)
        
        tab4=Frame()
        nb.add(tab4,text='min,max,pred')
        self.mmplabelframe=LabelFrame(tab4,text='min,max,pred')
        self.mmpframe=Frame(self.mmplabelframe)
        self.mmpframe.pack(fill='both',expand='yes')
        self.mmplabelframe.pack(fill='both',expand='yes',padx=20)
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
    def testButton(self):
        instancedata=[]
        for i in range(self.entrys.__len__()):
            instancedata.append(self.entrys[i].get())
        result=ExplanationService.limeExplanation(instancedata)
        if(result is None):
            print('Erro Message Box Here')
            return
        print('min: '+str(result[1]))
        print('max: '+str(result[2]))
        print('pred: '+str(result[3]))
        
        self.limeframe.destroy()
        self.limeframe=Frame(self.limelabelframe)
        self.limeframe.pack(fill='both',expand='yes')
        
        f=result[0]
        f.add_subplot(111)
        
        canvas = FigureCanvasTkAgg(f, master=self.limeframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(canvas, self.limeframe)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand='yes')
        
        self.featureframe.destroy()
        self.featureframe=Frame(self.featurelabelframe)
        self.featureframe.pack(fill='both',expand='yes')
        
        f2 = Figure(figsize=(1, 1), dpi=100)
        f2.suptitle('Feature Values')
        a2 = f2.add_subplot(111)
        a2.bar(result[4],result[5])
        
        canvas2 = FigureCanvasTkAgg(f2, master=self.featureframe)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar2 = NavigationToolbar2Tk(canvas2, self.featureframe)
        toolbar2.update()
        canvas2._tkcanvas.pack(side='top', fill='both', expand='yes')
        
        self.mmpframe.destroy()
        self.mmpframe=Frame(self.mmplabelframe)
        self.mmpframe.pack(fill='both',expand='yes')
        
        mmplabels = ['min', 'max', 'predicted']
        mmpdata=[]
        mmpdata.append(result[1])
        mmpdata.append(result[2])
        mmpdata.append(result[3])
        mmpdata=np.array(mmpdata)
        f3 = Figure(figsize=(1, 1), dpi=100)
        f3.suptitle('Min,Max,Predicted')
        a3 = f3.add_subplot(111)
        a3.bar(mmplabels,mmpdata)
        
        canvas3 = FigureCanvasTkAgg(f3, master=self.mmpframe)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side='top', fill='both', expand='yes')
        
        toolbar3 = NavigationToolbar2Tk(canvas3, self.mmpframe)
        toolbar3.update()
        canvas3._tkcanvas.pack(side='top', fill='both', expand='yes')