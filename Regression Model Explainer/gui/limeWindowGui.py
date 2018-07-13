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
    '''Frame for the Lime Test
    '''
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
        #print('min: '+str(result[1]))
        #print('max: '+str(result[2]))
        #print('pred: '+str(result[3]))
        
        self.limeframe.destroy()
        self.limeframe=Frame(self.limelabelframe)
        self.limeframe.pack(fill='both',expand='yes')
        '''
        f = Figure(figsize=(1, 1), dpi=100)
        a=f.add_subplot(111)
        a.plot(result[0].get_axes())
        
        f=result[0]
        f.add_subplot(111)
        a2 =f.add_subplot(122)
        a2.bar(result[4],result[5])
        '''
        #print(result[2])
        f = Figure(figsize=(1, 1), dpi=100)
        a = f.add_subplot(132)
        ind = 0
        height = 0.10
        
        zahler=0
        labels=result[0]
        values=result[1]
        
        for i in range(values.__len__()):
            if(values[i]>=0):
                a.barh(ind+height*zahler,values[i],height,color='green')
                a.text(values[i],ind+height*zahler,str(round(values[i],2)),fontsize=8)
                zahler=zahler+1
                a.text(0,ind+height*zahler,labels[i],fontsize=8)
                zahler=zahler+1
            else:
                a.barh(ind+height*zahler,values[i],height,color='red')
                a.text(values[i],ind+height*zahler,str(round(values[i],2)),fontsize=8)
                zahler=zahler+1
                a.text(min(values),ind+height*zahler,labels[i],fontsize=8)
                zahler=zahler+1
                canvas = FigureCanvasTkAgg(f, master=self.limeframe)
        xlim=a.get_xlim()
        fullx=abs(xlim[0])+xlim[1]
        pos=((100/fullx)*xlim[0])/100
        pos=abs(pos)
        a.set_title('negative/positve',x=pos)
        a.axvline(0, color='black')
        a.xaxis.set_visible(False)
        a.yaxis.set_visible(False)
        a.axis('off')
        a.invert_yaxis()
        
        maxv=result[3]
        minv=result[2]
        predict=result[4]
        predictlocal=result[5][0]

        a2 = f.add_subplot(131)

        a2.set_xlim(minv,maxv)
        x1, y1 = [minv, minv], [1, 10]
        a2.plot(x1,y1,color='white')
        a2.axhline(3, color='black')
        a2.axhline(4,color='black')
        x1, y1 = [minv, minv], [3, 4]
        a2.plot(x1,y1,color='black')
        x1, y1 = [maxv, maxv], [3, 4]
        a2.plot(x1,y1,color='black')
        a2.text(minv,3.5,str(round(minv,2))+'\n(min)')
        a2.text(maxv,3.5,str(round(maxv,2))+'\n(max)')
        x1, y1=[predict,predict], [4,5]
        a2.plot(x1,y1,color='black')
        a2.text(predict,5,'   '+str(round(predict,2))+'\n(prediction)')
        x1, y1=[predictlocal,predictlocal], [2,3]
        a2.plot(x1,y1,color='black')
        a2.text(predictlocal,2,'          '+str(round(predictlocal,2))+'\n(prediction local)')
        x1=[minv,predict]
        a2.fill_between(x1,3,4,color='green')
        a2.xaxis.set_visible(False)
        a2.yaxis.set_visible(False)
        a2.axis('off')
        a2.invert_yaxis()
        a2.set_title('Prediction for: '+result[6])
        
        
        feature=result[7]
        values=result[8]
        
        a3 = f.add_subplot(133)
        a3.set_xlim(0,2)
        a3.set_ylim(0,feature.__len__()+1)
        a3.invert_yaxis()
        x1,y1=[1,1],[0,feature.__len__()+1]
        a3.plot(x1,y1,color='black')
        for i in range(feature.__len__()+2):
            x1,y1=[0,2],[i,i]
            a3.plot(x1,y1,color='black')
        x1,y1=[0,0],[0,feature.__len__()+1]
        a3.plot(x1,y1,color='black')
        x1,y1=[2,2],[0,feature.__len__()+1]
        a3.plot(x1,y1,color='black')

        for i in range(feature.__len__()):
            a3.text(0,i+1.5,feature[i])
            a3.text(1,i+1.5,values[i])
        a3.text(0,0.5,'Feature')
        a3.text(1,0.5,'Values')
        for i in range(result[1].__len__()):
            if(result[1][i]>=0):
                a3.fill_between([0,2],i+1,i+2,color='green')
            else:
                a3.fill_between([0,2],i+1,i+2,color='red')
        #a3.fill_between([0,2],1,feature.__len__()+1,color='green')
        a3.xaxis.set_visible(False)
        a3.yaxis.set_visible(False)
        a3.axis('off')
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(canvas, self.limeframe)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand='yes')
        '''
        f2=result[2]
        f2.add_subplot(111)
        
        self.featureframe.destroy()
        self.featureframe=Frame(self.featurelabelframe)
        self.featureframe.pack(fill='both',expand='yes')
        
        canvas2 = FigureCanvasTkAgg(f2, master=self.featureframe)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar2 = NavigationToolbar2Tk(canvas2, self.featureframe)
        toolbar2.update()
        canvas2._tkcanvas.pack(side='top', fill='both', expand='yes')
        '''