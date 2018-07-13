from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import messagebox
from tkinter import END
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
from tkinter.ttk import Scrollbar
from tkinter.filedialog import askopenfilename

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

from gui.mainWindowGui import MainWindowGui
from services.modelDataService import ModelDataService
from services.explanationService import ExplanationService
from gui.scrolledFrameXandY import ScrolledFrameXandY
from tools.helper import Helper
class ExplanationFeatureWindowGui(Frame):
    ''' Frame for Explanation Feature
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        mds=ModelDataService()
        features=mds.getInputVars()
        self.master=master
        if(features is not None):
            labelframe=LabelFrame(self,text='Load test Data')
            frame=Frame(labelframe)
            label = Label(frame,width='20', text='Testdata file: ', anchor='e')
            self.fileentry = Entry(frame,readonlybackground='white')
            self.fileentry.config(state='readonly')
            self.brbutton=Button(frame,text='browse',command=self.browseButton)
            frame.pack(side='top',fill='x')
            label.pack(side='left')
            self.fileentry.pack(side='left',fill='x',expand='yes')
            self.brbutton.pack(side='left')
            labelframe.pack(fill='x',padx=20)
            
            frame=Frame(labelframe)
            label = Label(frame,width='20', text='Choose Feature: ', anchor='e')
            self.featurecombo = Combobox(frame,values=features,state="readonly")
            label.pack(side='left')
            self.featurecombo.pack(side='left',fill='x',expand='yes')
            frame.pack(side='top',fill='x')
            
            frame=Frame(labelframe)
            label = Label(frame,width=20, text='Choose Steps', anchor='e')
            self.stepsentry = Entry(frame)
            frame.pack(side='top',fill='x')
            label.pack(side='left')
            self.stepsentry.pack(side='left',fill='x',expand='yes')
        
            self.emptyRow()
        
        self.eflabelframe=LabelFrame(self,text='Explanation Feature')
        self.efframe=Frame(self.eflabelframe)
        self.efframe.pack(fill='both',expand='yes')
        self.eflabelframe.pack(fill='both',expand='yes',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Options')
        self.efbutton=Button(labelframe,text='Explain Feature',command=self.explainFeatureTest)
        self.efbutton.pack(side='right')
        self.cancelbutton=Button(labelframe,text='Cancel',command=lambda: master.switch_frame(MainWindowGui))
        self.cancelbutton.pack(side='right') 
        labelframe.pack(fill='x',padx=20)
        if(features is None):
            self.efbutton.config(state='disabled')
            messagebox.showerror('No Model', 'No Model created or loaded')
    def emptyRow(self):
        frame=Frame(self,padx=20)
        label = Label(frame,width=20, text='', anchor='e')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
    def explainFeatureTest(self):
        file=self.fileentry.get()
        feature=self.featurecombo.get()
        steps=self.stepsentry.get()
        result=ExplanationService.featureExplanation(file, feature, steps)
        if(result is None):
            messagebox.showerror('Failed', 'Steps must be a positive number (<=number of tuples in test data) and test data must fit to the model and feature must be choosen')
        else:
            self.createTree(result)
    def createTree(self,result):
        '''
        self.efframe.destroy()
        self.efframe=Frame(self.eflabelframe)
        self.efframe.pack(fill='both',expand='yes')
        vsb=Scrollbar(self.efframe,orient="vertical")
        vsb.pack(fill='y',side='right')
        body = Frame(self.efframe)
        body.pack(fill='both',expand='yes')
        scrollable_body = ScrolledFrameXandY(body)
        tree = Treeview(scrollable_body, selectmode='browse')
        tree.pack(expand=True,fill='both')
        vsb.config(command=tree.yview)
        col=[]
        for i in range(result[0].__len__()):
            col.append(str(i+1))
        tree["columns"] = col
        tree['show'] = 'headings'
            
        for i in range(col.__len__()):
            tree.column(col[i],width=250,anchor='c')
        for i in range(col.__len__()):
            tree.heading(col[i],text=result[0][i])
        for i in range(result[1].__len__()):
            tree.insert("",'end',text="",values=result[1][i])
        scrollable_body.update()
        #print('here')
        #print(result[1])
        data=result[1]
        ran=[]
        numresult=[]
        mesuredmins=[]
        mesuredmax=[]
        predictmin=[]
        predictmax=[]
        mesured=[]
        predict=[]
        
        for i in range(data.__len__()):
            ran.append(data[i][0])
            numresult.append(data[i][1])
            if(int(data[i][1])!=0):
                temp=[]
                temp=data[i][2].split('-')
                mesuredmins.append(temp[0])
                mesuredmax.append(temp[1])
                temp=data[i][3].split('-')
                predictmin.append(temp[0])
                predictmax.append(temp[1])
                mesured.append(data[i][4])
                predict.append(data[i][5])
            else:
                mesuredmins.append('0')
                mesuredmax.append('0')
                predictmin.append('0')
                predictmax.append('0')
                mesured.append('0')
                predict.append('0')
        mesuredmins=np.array(mesuredmins).astype(float)
        mesuredmax=np.array(mesuredmax).astype(float)
        predictmin=np.array(predictmin).astype(float)
        predictmax=np.array(predictmax).astype(float)
        mesured=np.array(mesured).astype(float)
        predict=np.array(predict).astype(float)
        '''
        data=Helper.tranformDataForFeatureGraph(result[1])
        N = data[0].__len__()
        ind = np.arange(N)  # the x locations for the groups
        height = 0.10 
        
        f = Figure(figsize=(1, 1), dpi=100)
        a2 = f.add_subplot(111)
        r1=a2.barh(ind,data[2],height)
        r2=a2.barh(ind+height,data[3],height)
        r3=a2.barh(ind+height*2,data[6],height)
        r4=a2.barh(ind+height*3,data[4],height)
        r5=a2.barh(ind+height*4,data[5],height)
        r6=a2.barh(ind+height*5,data[7],height)
        
        a2.set_yticks(ind+height)
        labels=Helper.getFeatureExplanationLabels(data[0], data[1])
        a2.set_yticklabels(labels)
        a2.invert_yaxis()
        a2.legend( (r1[0], r2[0], r3[0],r4[0],r5[0],r6[0]), ('min measured', 'max mesured', 'avarage (mean) mesured',
                                         'min predicted','max predicted','avarage (mean) prediction') )
        a2.set_xlabel(result[2])
        a2.set_title('ranges from feature: '+self.featurecombo.get())
        
        self.efframe.destroy()
        self.efframe=Frame(self.eflabelframe)
        self.efframe.pack(fill='both',expand='yes')
        
        canvas = FigureCanvasTkAgg(f, master=self.efframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(canvas, self.efframe)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand='yes')