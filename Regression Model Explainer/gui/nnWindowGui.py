from tkinter import LabelFrame
from tkinter import messagebox
from tkinter import END
from tkinter import Entry
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import Label
from tkinter import Frame
from tkinter import Button
from tkinter.ttk import Combobox
from tkinter import filedialog

from services.loadCsvService import LoadCsvService
from gui.trainNnWindowGui import TrainNnWindowGui
from tools.helper import Helper
from services.modelDataService import ModelDataService
class NnWindowGui(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.m=master
        
        self.entryOnlyReadList=[]
        self.hiddenLayerList=[]
        
        labelframe=LabelFrame(self,text='Load Train Data')
        frame=self.createFrameRow(labelframe,'Filepath: ',True)
        browse=Button(frame,text='Browse',command=self.browseButton)
        browse.pack(side='left')
        self.createFrameRow(labelframe,'Number of Data Tuples: ',True)
        self.createFrameRow(labelframe,'InputLayer Size: ',True)
        self.createFrameRow(labelframe,'OutputLayer Size: ',True)
        labelframe.pack(fill='x',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Choose Settings')
        frame=Frame(labelframe)
        label = Label(frame, text='Choose output feature: ', anchor='e')
        self.tagcombo = Combobox(frame,state="readonly")
        frame.pack(side='top',fill='x')
        label.pack(side='left')
        self.tagcombo.pack(side='left',fill='x',expand='yes')
        self.createFrameRow(labelframe,'Choose Epochs: ',False)
        self.createFrameRow(labelframe,'Choose Batchsize: ',False)
        labelframe.pack(fill='x',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Add Hidden Layer')
        frame=self.createFrameRow(labelframe,'Hidden Layer Size: ',False)
        HLButton = Button(frame,width=20, text='Add Hidden Layer', command=self.addHiddenLayerButton)
        HLButton.pack(side='left')
        frame=Frame(labelframe)
        scrollbar = Scrollbar(frame)
        scrollbar.pack( side = 'right',fill='y')
        self.mylist = Listbox(frame, yscrollcommand = scrollbar.set )
        scrollbar.config( command = self.mylist.yview )
        frame.pack(fill='both', expand='yes')
        self.mylist.pack( side = 'left',fill='both',expand='yes')
        labelframe.pack(fill='both',expand='yes',padx=20)

        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Option')
        enter=Button(labelframe,text='Create Neural Network and Train Data',command=self.creatTrainNn)
        enter.pack()
        labelframe.pack(fill='x',padx=20)
        
    def createFrameRow(self,labelframe,text,readonly):
        frame=Frame(labelframe)
        label = Label(frame,width=20, text=text, anchor='e')
        entry = Entry(frame,readonlybackground='white')
        if(readonly):
            entry.config(state='readonly')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
        entry.pack(side='left',fill='x',expand='yes')
        self.entryOnlyReadList.append(entry)
        return frame
    def emptyRow(self):
        frame=Frame(self,padx=20)
        label = Label(frame,width=20, text='', anchor='e')
        frame.pack(side='top',fill='x')
        label.pack()
    def setReadonlyEntry(self,index,text):
        self.entryOnlyReadList[index].config(state='normal')
        self.entryOnlyReadList[index].delete(0,END)
        if(not text==''):
            self.entryOnlyReadList[index].insert(0,text)
        self.entryOnlyReadList[index].config(state='readonly')
    def browseButton(self):
        file = filedialog.askopenfilename(filetypes=[("CSV Files",".csv")])
        loadCsvService=LoadCsvService(file)
        data=loadCsvService.getGuiOutputData()
        if(data is not None):
            for i in range(4):
                self.setReadonlyEntry(i, data[i])
            self.tagcombo.config(values=data[4])
        else:
            for i in range(4):
                self.setReadonlyEntry(i, '')
            self.tagcombo.config(values=[],state='normal')
            self.tagcombo.delete(0, END)
            self.tagcombo.config(state='readonly')
            messagebox.showerror('Worng File', 'The File: '+file+' is not compatible')
    def addHiddenLayerButton(self):
        hiddenlayersize=self.entryOnlyReadList[6].get()
        if(Helper.is_integer(hiddenlayersize)):
            self.hiddenLayerList.append(hiddenlayersize)
            self.mylist.insert(END, "Hidden Layer: " + str(hiddenlayersize)+' Units')
        else:
            messagebox.showerror('No Number', 'Size of a Hidden Layer must be a positiv number')
    def creatTrainNn(self):
        #self.m.switch_frame(TrainNnWindowGui)
        file=self.entryOnlyReadList[0].get()
        outputvar=self.tagcombo.get()
        hl=self.hiddenLayerList
        epoch=self.entryOnlyReadList[4].get()
        batchsize=self.entryOnlyReadList[5].get()
        mds=ModelDataService()
        if(mds.setDataFromGui(file, outputvar, hl, epoch, batchsize)):
            self.m.switch_frame(TrainNnWindowGui)
        else:
            messagebox.showerror('False Setting', 'Something in the setting is wrong look at tooltips(tooltips not implemented)')