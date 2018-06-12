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
from gui.mainWindowGui import MainWindowGui
from services.explanationService import ExplanationService
from tools.helper import Helper
class OverallExplanationWindowGui(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        
        nb=Notebook(self)
        nb.pack(side='left',fill='both',expand='yes')
        
        tab1=Frame()
        nb.add(tab1,text='Table')
        labelframe=LabelFrame(tab1,text='Load Test Data')
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
        
        self.emptyRow(tab1)
        
        self.treelabelframe=LabelFrame(tab1,text='Overall Eplanation')
        self.treeframe=Frame(self.treelabelframe)
        self.treeframe.pack(fill='both',expand='yes')
        self.treelabelframe.pack(fill='both',expand='yes',padx=20)
        
        labelframe=LabelFrame(tab1,text='Options')
        button=Button(labelframe,text='Test',command=self.testButton)
        button.pack(side='right')
        button=Button(labelframe,text='Cancel',command=lambda: self.master.switch_frame(MainWindowGui))
        button.pack(side='right')
        labelframe.pack(fill='x',padx=20)
        
        tab2=Frame()
        nb.add(tab2,text='Boxplot')
        self.boxplotlabelframe=LabelFrame(tab2,text='Difference Messured to Predicted')
        self.boxplotframe=Frame(self.boxplotlabelframe)
        self.boxplotframe.pack(fill='both',expand='yes')
        self.boxplotlabelframe.pack(fill='both',expand='yes',padx=20)
        
        tab3=Frame()
        nb.add(tab3,text='Mean')
        self.meanlabelframe=LabelFrame(tab3,text='Mean of the differences messured to predict')
        self.meanframe=Frame(self.meanlabelframe)
        self.meanframe.pack(fill='both',expand='yes')
        self.meanlabelframe.pack(fill='both',expand='yes',padx=20)
    def emptyRow(self,tab):
        frame=Frame(tab,padx=20)
        label = Label(frame,width=20, text='', anchor='e')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
    def testButton(self):
        file=self.fileentry.get()
        data=ExplanationService.overallExplanation(file)
        if(data is None):
            messagebox.showerror('Overall Explanation failed', '(Todo information about the reasons)')
            return
        self.createTree(data)
    def createTree(self,data):
        self.treeframe.destroy()
        self.treeframe=Frame(self.treelabelframe)
        self.treeframe.pack(fill='both',expand='yes')
        vsb=Scrollbar(self.treeframe,orient="vertical")
        vsb.pack(fill='y',side='right')
        body = Frame(self.treeframe)
        body.pack(fill='both',expand='yes')
        scrollable_body = ScrolledFrameXandY(body)
        tree = Treeview(scrollable_body, selectmode='browse')
        tree.pack(expand=True,fill='both')
        vsb.config(command=tree.yview)
        col=[]
        for i in range(data[0].__len__()):
            col.append(str(i+1))
        tree["columns"] = col
        tree['show'] = 'headings'
            
        for i in range(col.__len__()):
            tree.column(col[i],width=100,anchor='c')
        for i in range(col.__len__()):
            tree.heading(col[i],text=data[0][i])
        for i in range(data[1].__len__()):
            tree.insert("",'end',text="",values=data[1][i])
        scrollable_body.update()
        
        self.boxplotframe.destroy()
        self.boxplotframe=Frame(self.boxplotlabelframe)
        self.boxplotframe.pack(fill='both',expand='yes')
        
        positiv=data[2]
        negativ=data[3]
        full=data[4]
        data_to_plot=[positiv,negativ,full]
        
        boxplotlabels = ['positive diff', 'neagtive diff', 'full diff']
        
        f = Figure(figsize=(1, 1), dpi=100)
        f.suptitle('Difference of Messured and Predicted Values for: '+str(data[5]))
        a = f.add_subplot(111)
        a.boxplot(data_to_plot)
        a.set_xticklabels(np.repeat(boxplotlabels, 1),rotation=0, fontsize=8)
        
        canvas = FigureCanvasTkAgg(f, master=self.boxplotframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(canvas, self.boxplotframe)
        toolbar.update()
        canvas._tkcanvas.pack(side='top', fill='both', expand='yes')
        
        self.meanframe.destroy()
        self.meanframe=Frame(self.meanlabelframe)
        self.meanframe.pack(fill='both',expand='yes')
        
        means=Helper.getMeans(positiv, negativ, full)
        meanlabels = ('positive diff', 'neagtive diff', 'full diff')
        print(means)
        
        f2 = Figure(figsize=(1, 1), dpi=100)
        f2.suptitle('Means of the Difference of Messured and Predicted Values for: '+str(data[5]))
        a2 = f2.add_subplot(111)
        a2.bar(meanlabels,means)
        
        canvas2 = FigureCanvasTkAgg(f2, master=self.meanframe)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar2 = NavigationToolbar2Tk(canvas2, self.meanframe)
        toolbar2.update()
        canvas2._tkcanvas.pack(side='top', fill='both', expand='yes')
        
        #Todo bar for number positiv, negativ,full
        
        
        
        