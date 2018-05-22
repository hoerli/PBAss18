from tkinter import Label
from tkinter import messagebox
from tkinter import ttk
from tkinter import Entry
from tkinter import Button
from tkinter import Scrollbar
from tkinter import BOTH,LEFT, Frame, TOP, X,RIGHT,END,Listbox,Y

from tkinter.filedialog import askopenfilename
from services.modelDataService import ModelDataService
from services.loadCsvService import LoadCsvService
from services.KerasNNService import KerasNNService
#from gui.guiTraining import GUITraining
class CreateTrainNNGui():
    def __init__(self,mmgui):
        self.mmgui=mmgui
        self.mds=ModelDataService()
    def loadCsv(self):
        file = askopenfilename(filetypes=[("CSV Files",".csv")])
        test = self.mds.setDataPath(file)
        if(file == '' or not test):
            self.errorMessage('Wrong File', 'The File: '+file+' is not compatible')
            self.mmgui.delete()
            self.mmgui.createMainWindowLabel()
        else:
            self.createWindow(file)
    def createWindow(self,file):
        self.row=0
        csvpath=file
        numberodata=self.getNumberOfData(csvpath)
        sizeoinputlayer=self.getNumberOfInput(csvpath)
        taglist=self.getTagList(csvpath)
        if(not numberodata or not sizeoinputlayer or not taglist):
            self.errorMessage('False CSV File', 'The file needs at least 2 cullums and 2 rows, the first rows has to be the features')
            self.mmgui.delete()
            self.mmgui.createMainWindowLabel()
        else:
            self.mmgui.delete()
            what=[]
            info=[]
            what.append('Filepath: ')
            info.append(csvpath)
            what.append('Number of Data Tuples: ')
            info.append(str(self.getNumberOfData(csvpath)))
            what.append('InputLayer Size: ')
            info.append(str(self.getNumberOfInput(csvpath)))
            what.append('OutputLayer Size: ')
            info.append('1')
            self.creatnformationW(what, info)
            
            frame=Frame(self.mmgui.root,bg='white')
            taglabel = Label(frame,width=20, text='Choose output feature: ', anchor='e',bg='white')
            self.tagcombo = ttk.Combobox(frame,values=taglist,state="readonly")
            frame.pack(side=TOP, fill=X,anchor='w')
            taglabel.pack(side=LEFT)
            self.tagcombo.pack(side=LEFT)
            self.mmgui.input.append(frame)
            
            frame=Frame(self.mmgui.root,bg='white')
            epolabel = Label(frame,width=20, text='Choose Epochs: ', anchor='e',bg='white')
            self.epoentry = Entry(frame,width=10)
            frame.pack(side=TOP, fill=X,anchor='w')
            epolabel.pack(side=LEFT)
            self.epoentry.pack(side=LEFT)
            self.mmgui.input.append(frame)
            
            frame=Frame(self.mmgui.root,bg='white')
            bslabel = Label(frame,width=20, text='Choose Batchsize: ', anchor='e',bg='white')
            self.bsentry = Entry(frame,width=10)
            frame.pack(side=TOP, fill=X,anchor='w')
            bslabel.pack(side=LEFT)
            self.bsentry.pack(side=LEFT)
            self.mmgui.input.append(frame)
            
            frame=Frame(self.mmgui.root,bg='white')
            hll = Label(frame,width=20, text='Hidden Layer Size: ',anchor='e',bg='white')
            self.hlentry = Entry(frame,width=10)
            frame.pack(side=TOP, fill=X,anchor='w')
            hll.pack(side=LEFT)
            self.hlentry.pack(side=LEFT)
            self.mmgui.input.append(frame)
            
            HLButton = Button(self.mmgui.root,width=20, text='Add Hidden Layer', command=self.addHiddenLayer)
            HLButton.pack(anchor='w')
            HLButton.config(bg='navy', fg='white', bd=8)
            self.mmgui.input.append(HLButton)
            
            frame=Frame(self.mmgui.root,bg='white')
            scrollbar = Scrollbar(frame)
            scrollbar.pack( side = LEFT,fill=Y)

            self.mylist = Listbox(frame,width=30, yscrollcommand = scrollbar.set )

            self.mylist.pack( side = LEFT)
            scrollbar.config( command = self.mylist.yview )
            
            frame.pack(side=TOP, fill=X,anchor='w')
            
            self.mmgui.input.append(frame)
            
            self.HiddenLayer=[]
            
            train=Button(self.mmgui.root,text='Create NN andTrain',command=self.Train)
            train.pack()
            train.config(bg='navy', fg='white', bd=8)
            self.mmgui.input.append(train)
    def creatnformationW(self,what,information):
        for i in range(what.__len__()):
            frame=Frame(self.mmgui.root,bg='white')
            w = Label(frame,width=20, text=what[i], anchor='e',bg='white')
            i = Label(frame,text=information[i],bg='white')
            frame.pack(side=TOP, fill=X,anchor='w')
            w.pack(side=LEFT)
            i.pack(side=LEFT)
            self.mmgui.input.append(frame)
    def addHiddenLayer(self):
        print(self.hlentry.get())
        if(self.hlentry.get().isdigit()):#TODO postive number
            self.HiddenLayer.append(self.hlentry.get())
            self.mylist.insert(END, "Hidden Layer: " + str(self.hlentry.get())+' Units')
        else:
            self.errorMessage('Positive Number', 'Hidden layer must have a positive number as Units')
    def errorMessage(self,title,message):
        messagebox.showerror(title, message)
    def Train(self):
        ofeature=self.tagcombo.get()
        epo=self.epoentry.get()
        bs=self.bsentry.get()
        if(self.HiddenLayer.__len__()>0 and ofeature != '' and epo.isdigit() and bs.isdigit()):
            bstest=self.mds.setBatchSize(bs)
            epotest=self.mds.setEpoch(epo)
            ftest=self.mds.setOutputvar(ofeature)
            hltest=self.mds.setHiddenLayer(self.HiddenLayer)
            if(bstest,epotest,ftest,hltest):
                if(self.mds.isDataSetForTrain()):
                    self.TrainWindow(True)
                else:
                    self.errorMessage('False Input', 'blblabla') 
            else:
                self.errorMessage('False Input', 'blblabla')
        else:
            self.errorMessage('False Input', 'blblabla')#TODO message
    def TrainWindow(self,train):
        self.mmgui.delete()
        what=[]
        info=[]
        what.append('Filepath: ')
        info.append(self.mds.getDataPath())
        what.append('Number of Data Tuples: ')
        info.append(str(self.getNumberOfData(self.mds.getDataPath())))
        what.append('InputLayer Size: ')
        info.append(str(self.getNumberOfInput(self.mds.getDataPath())))
        what.append('OutputLayer Size: ')
        info.append('1')
        what.append('Output feature: ')
        info.append(self.mds.getOutputvar())
        what.append('Epoch: ')
        info.append(self.mds.getEpoch())
        what.append('Batchsize: ')
        info.append(self.mds.getBatchSize())
        what.append('Hidden Layer: ')
        info.append(str(self.mds.getHiddenLayer()))
        self.creatnformationW(what, info)
        if(train):
            nns=KerasNNService()
            test=nns.createNN()#TODO do that in Threat
            if(test):
                self.errorMessage('Finish', 'Model Created')
                self.mmgui.delete()
                self.mmgui.createMainWindowLabel()
            else:
                self.errorMessage('Error', 'Model Not created')
                self.mmgui.delete()
                self.mmgui.createMainWindowLabel()
    def getNumberOfData(self,path):
        lc=LoadCsvService(path)
        return lc.getnumberOfData()
    def getNumberOfInput(self,path):
        lc=LoadCsvService(path)
        return lc.getNumberOfInput()
    def getTagList(self,path):
        lc=LoadCsvService(path)
        return lc.getTagList()