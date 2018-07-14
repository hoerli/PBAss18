from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import LabelFrame
from tkinter import Button
from tkinter import messagebox

from services.modelDataService import ModelDataService
from gui.mainWindowGui import MainWindowGui
class ShowModelInformationGui(Frame):
    ''' Frame to show model informations
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        
        mds=ModelDataService()
        dataandlabel=mds.getModelInformationForGui()
            
        labelframe=LabelFrame(self,text='Model Information')
        if(dataandlabel is not None):
            for i in range(dataandlabel[0].__len__()):
                self.createFrameRow(labelframe,dataandlabel[0][i], dataandlabel[1][i])
        else:
            messagebox.showerror('No Moded', 'No Model created or loaded')
        labelframe.pack(fill='both',expand='yes',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Options')
        cancel=Button(labelframe,text='OK',command=lambda: master.switch_frame(MainWindowGui))
        cancel.pack()
        labelframe.pack(fill='x',padx=20)
        
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