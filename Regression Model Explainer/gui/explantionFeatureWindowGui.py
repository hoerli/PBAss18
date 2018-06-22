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

from gui.mainWindowGui import MainWindowGui
from services.modelDataService import ModelDataService
from services.explanationService import ExplanationService
from gui.scrolledFrameXandY import ScrolledFrameXandY
class ExplanationFeatureWindowGui(Frame):
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