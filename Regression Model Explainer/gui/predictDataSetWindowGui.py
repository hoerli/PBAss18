from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import END
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter.ttk import Scrollbar

from gui.mainWindowGui import MainWindowGui
from tkinter.filedialog import askopenfilename
from services.KerasNNService import KerasNNService
from gui.scrolledFrameXandY import ScrolledFrameXandY
from gui.limeWindowGui import LimeWindowGui
class PredictDataSetWindowGUI(Frame):
    ''' Frame for prediction with a data set
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        
        labelframe=LabelFrame(self,text='Load test Data')
        frame=Frame(labelframe)
        label = Label(frame, text='Testdata file: ', anchor='e')
        self.fileentry = Entry(frame,readonlybackground='white')
        self.fileentry.config(state='readonly')
        button=Button(frame,text='browse',command=self.browseButton)
        frame.pack(side='top',fill='x')
        label.pack(side='left')
        self.fileentry.pack(side='left',fill='x',expand='yes')
        button.pack(side='left')
        labelframe.pack(fill='x',padx=20)
        
        self.emptyRow()
        
        self.treelabelframe=LabelFrame(self,text='Prediction: Double click on tuple in Table to show explanation of the tuple (lime)')
        self.treeframe=Frame(self.treelabelframe)
        self.treeframe.pack(fill='both',expand='yes')
        self.treelabelframe.pack(fill='both',expand='yes',padx=20)

        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Options')
        button=Button(labelframe,text='Cancel',command=lambda: self.master.switch_frame(MainWindowGui))
        button.pack(side='right')
        labelframe.pack(fill='x',padx=20)
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
        self.predict()
    def predict(self):
        knns=KerasNNService()
        file=self.fileentry.get()
        data=knns.predictFileforGui(file)
        if(data is None):
            messagebox.showerror('Prediction Failed', 'Prediction failed (Todo information about the reasons)')
            return
        self.createTree(data)
    def OnDoubleClick(self,event):
        item = self.tree.identify('item',event.x,event.y)
        item=item[1:]
        ind=None
        try:
            ind=int(item, 16)-1
        except:
            print('no item here')
        if(ind is not None):
            file=self.fileentry.get()
            self.master.switch_frame(LimeWindowGui)
            self.master._frame.setFilePath(file,ind)
    def createTree(self,data):
        self.treeframe.destroy()
        self.treeframe=Frame(self.treelabelframe)
        self.treeframe.pack(fill='both',expand='yes')
        vsb=Scrollbar(self.treeframe,orient="vertical")
        vsb.pack(fill='y',side='right')
        body = Frame(self.treeframe)
        body.pack(fill='both',expand='yes')
        scrollable_body = ScrolledFrameXandY(body)
        self.tree = Treeview(scrollable_body, selectmode='browse')
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.pack(expand=True,fill='both')
        vsb.config(command=self.tree.yview)
        col=[]
        for i in range(data[0].__len__()):
            col.append(str(i+1))
        self.tree["columns"] = col
        self.tree['show'] = 'headings'
            
        for i in range(col.__len__()):
            self.tree.column(col[i],anchor='c')
        for i in range(col.__len__()):
            self.tree.heading(col[i],text=data[0][i])
        for i in range(data[1].__len__()):
            self.tree.insert("",'end',text="",values=data[1][i])
        scrollable_body.update()