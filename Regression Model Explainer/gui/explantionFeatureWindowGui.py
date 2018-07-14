from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import messagebox
from tkinter import END
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

from services.modelDataService import ModelDataService
from services.explanationService import ExplanationService
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
            self.featurecombo.bind("<<ComboboxSelected>>", self.selectItem)
            frame.pack(side='top',fill='x')
            
            frame=Frame(labelframe)
            label = Label(frame,width=20, text='Choose Steps\n (positive number)\nReturn to update', anchor='e')
            self.stepsentry = Entry(frame)
            self.stepsentry.bind('<Key-Return>', self.on_changed)
            frame.pack(side='top',fill='x')
            label.pack(side='left')
            self.stepsentry.pack(side='left',fill='x',expand='yes')
        
        self.eflabelframe=LabelFrame(self,text='Explanation Feature')
        self.efframe=Frame(self.eflabelframe)
        self.efframe.pack(fill='both',expand='yes')
        self.eflabelframe.pack(fill='both',expand='yes',padx=20)
        
        self.master.creatExplanationMenu(self,2)
    def on_changed(self,event):
        steps=self.stepsentry.get()
        if(Helper.is_integer(steps)):
            if(self.fileentry.get()!=''):
                self.explainFeatureTest()
    def selectItem(self,event):
        self.explainFeatureTest()
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.setFileEntrys(file)
    def setFileEntrys(self,file):
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
        self.featurecombo.current(0)
        self.stepsentry.delete(0, END)
        self.stepsentry.insert(0,2)
        self.explainFeatureTest()
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