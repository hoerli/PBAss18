import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import END
from tkinter import messagebox
from tkinter.ttk import Notebook
from tkinter.ttk import Scrollbar
from tkinter.ttk import Treeview
from tkinter.filedialog import askopenfilename
from gui.scrolledFrameXandY import ScrolledFrameXandY
from services.explanationService import ExplanationService
from tools.helper import Helper
from gui.limeWindowGui import LimeWindowGui
class OverallExplanationWindowGui(Frame):
    ''' Frame for Overall Explanation
    '''
    def __init__(self,master):
        Frame.__init__(self, master)

        labelframe=LabelFrame(self,text='Load Test Data')
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
        
        frame=Frame(self)
        frame.pack(fill='both',expand='yes')
        labelframe=LabelFrame(frame,text='Overall Explanation: Double click on tuple in Table to show explanation of the tuple (lime)')
        labelframe.pack(fill='both',expand='yes',padx=20)
        nb=Notebook(labelframe)
        nb.pack(side='left',fill='both',expand='yes')
        
        self.tab1=Frame()
        nb.add(self.tab1,text='Graph')
        self.graphframe=Frame(self.tab1)
        self.graphframe.pack(fill='both',expand='yes')
        
        self.tab2=Frame()
        nb.add(self.tab2,text='Table')
        self.tableframe=Frame(self.tab2)
        self.tableframe.pack(fill='both',expand='yes')
        
    def emptyRow(self,tab):
        frame=Frame(tab,padx=20)
        label = Label(frame,width=20, text='', anchor='e')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.setFileEntry(file)
    def setFileEntry(self,file):
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
        self.test()
    def test(self):
        file=self.fileentry.get()
        data=ExplanationService.overallExplanation(file)
        if(data is None):
            messagebox.showerror('Overall Explanation failed', 'Data must fit to the model and model must be loaded')
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
        self.tableframe.destroy()
        self.tableframe=Frame(self.tab2)
        self.tableframe.pack(fill='both',expand='yes')
        vsb=Scrollbar(self.tableframe,orient="vertical")
        vsb.pack(fill='y',side='right')
        body = Frame(self.tableframe)
        body.pack(fill='both',expand='yes')
        scrollable_body = ScrolledFrameXandY(body)
        self.tree = Treeview(scrollable_body, selectmode='browse')
        self.tree.pack(expand=True,fill='both')
        self.tree.bind("<Double-1>", self.OnDoubleClick)
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
        
        self.graphframe.destroy()
        self.graphframe=Frame(self.tab1)
        self.graphframe.pack(fill='both',expand='yes')
        
        positiv=data[2]
        negativ=data[3]
        full=data[4]
        data_to_plot=[positiv,negativ,full]
        
        boxplotlabels = ['positive diff', 'neagtive diff', 'full diff']
        
        f = Figure(figsize=(1, 1), dpi=100)
        f.suptitle('Difference of Messured and Predicted Values for: '+str(data[5]))
        
        a = f.add_subplot(121)
        a.set_title('Differences as Boxplots')
        boxcolor=a.boxplot(data_to_plot,patch_artist=True)
        a.set_xticklabels(np.repeat(boxplotlabels, 1),rotation=0)
        colors = ['green', 'red','blue']
        for patch, color in zip(boxcolor['boxes'], colors):
            patch.set_facecolor(color)
            
        means=Helper.getMeans(positiv, negativ, full)
        meanlabels = ('positive diff', 'neagtive diff', 'full diff')
        
        a2 = f.add_subplot(122)
        a2.set_title('Means of the Differences')
        a2.bar(meanlabels,means,width=0.10,color=('green','red','blue'))
        
        canvas = FigureCanvasTkAgg(f, master=self.graphframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(canvas, self.graphframe)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand='yes')