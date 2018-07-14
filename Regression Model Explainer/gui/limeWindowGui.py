from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import Frame
from tkinter import Label
from tkinter import LabelFrame
from tkinter import messagebox
from tkinter import Button
from tkinter import Entry
from tkinter.filedialog import askopenfilename
from tkinter import END
from tkinter.ttk import Combobox

from services.explanationService import ExplanationService
class LimeWindowGui(Frame):
    '''Frame for the Lime Test
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        
        labelframe=LabelFrame(self,text='Load test Data')
        frame=Frame(labelframe)
        label = Label(frame,width=20, text='Testdata file: ', anchor='e')
        self.fileentry = Entry(frame,readonlybackground='white')
        self.fileentry.config(state='readonly')
        self.brbutton=Button(frame,text='browse',command=self.browseButton)
        frame.pack(side='top',fill='x')
        label.pack(side='left')
        self.fileentry.pack(side='left',fill='x',expand='yes')
        self.brbutton.pack(side='left')
        labelframe.pack(fill='x',padx=20)
        
        frame=Frame(labelframe)
        label = Label(frame,width=20, text='Choose Feature: ', anchor='e')
        self.featurecombo = Combobox(frame,state="readonly")
        self.featurecombo.bind("<<ComboboxSelected>>", self.selectItem)
        label.pack(side='left')
        self.featurecombo.pack(side='left',fill='x',expand='yes')
        frame.pack(side='top',fill='x')
        
        self.limelabelframe=LabelFrame(self,text='Explanation of a single tuple with lime')
        self.limeframe=Frame(self.limelabelframe)
        self.limeframe.pack(fill='both',expand='yes')
        self.limelabelframe.pack(fill='both',expand='yes',padx=20)
        
        self.master.creatExplanationMenu(self,3)
    def selectItem(self,event):
        index=self.featurecombo.current()
        self.runTest(self.inputtuples[index])
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.setFilePath(file,0)
    def setFilePath(self,file,index):
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
        
        self.inputtuples=ExplanationService.getInputTuples(file)
        if(self.inputtuples is None):
            messagebox.showerror('Error train data/model',
                                  'Train data doesnt fit to the model or no model created')
            return
        comboitems=[]
        for i in range(self.inputtuples.__len__()):
            comboitems.append('Tuple: '+str(i+1))
        self.featurecombo.config(values=comboitems)
        self.featurecombo.current(index)
        self.inputtuples=self.inputtuples.astype(float)
        self.runTest(self.inputtuples[index])
    def runTest(self,inpu):
        instancedata=inpu
        result=ExplanationService.limeExplanation(instancedata)
        if(result is None):
            print('Erro Message Box Here')
            return
        
        self.limeframe.destroy()
        self.limeframe=Frame(self.limelabelframe)
        self.limeframe.pack(fill='both',expand='yes')

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
        
        f.suptitle('Explanation of a single tuple with lime')
        
        canvas = FigureCanvasTkAgg(f, master=self.limeframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(canvas, self.limeframe)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand='yes')
        '''
        f2=result[9]
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