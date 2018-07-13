from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import END
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from gui.mainWindowGui import MainWindowGui
from services.explanationService import ExplanationService
class FailureTestWindowGui(Frame):
    ''' Frame for the Failure Test
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master=master
        labelframe=LabelFrame(self,text='Load test Data')
        frame=Frame(labelframe)
        label = Label(frame, text='Testdata file: ', anchor='e')
        self.fileentry = Entry(frame,readonlybackground='white')
        self.fileentry.config(state='readonly')
        self.brbutton=Button(frame,text='browse',command=self.browseButton)
        frame.pack(side='top',fill='x')
        label.pack(side='left')
        self.fileentry.pack(side='left',fill='x',expand='yes')
        self.brbutton.pack(side='left')
        labelframe.pack(fill='x',padx=20)
        
        self.emptyRow()
        
        self.plotlabelframe=LabelFrame(self,text='Failure Test')
        self.plotframe=Frame(self.plotlabelframe)
        self.plotframe.pack(fill='both',expand='yes')
        self.plotlabelframe.pack(fill='both',expand='yes',padx=20)
        
        self.emptyRow()
        
        labelframe=LabelFrame(self,text='Options')
        self.ftbutton=Button(labelframe,text='Failure Test',command=self.failureTest)
        self.ftbutton.pack(side='right')
        self.cancelbutton=Button(labelframe,text='Cancel',command=lambda: master.switch_frame(MainWindowGui))
        self.cancelbutton.pack(side='right') 
        labelframe.pack(fill='x',padx=20)
    def emptyRow(self):
        frame=Frame(self,padx=20)
        label = Label(frame,width=20, text='', anchor='e')
        frame.pack(side='top',fill='x')
        label.pack(side='left')
    def disableMenueAndButtons(self):
        self.master.disabelMenu()
        self.brbutton.config(state='disabled')
        self.ftbutton.config(state='disabled')
        self.cancelbutton.config(state='disabled')
    def enableMenueAndButtons(self):
        self.master.enableMenu()
        self.brbutton.config(state='normal')
        self.ftbutton.config(state='normal')
        self.cancelbutton.config(state='normal')
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
    def failureTest(self):
        file=self.fileentry.get()
        data=ExplanationService.failureTest(file)
        if(data is None):
            messagebox.showerror('Failure test failed', 'Todo: Infomation about the reason')
            return
        self.showPlot(data)
    def on_plot_hover(self,event):
        for i in range(self.feat.__len__()):
            self.feat[i].set_visible(False)
        if self.line.contains(event)[0]:
            ind = self.line.contains(event)[1]["ind"]
            self.feat[ind[0]].set_visible(True)  
        self.canvas.draw_idle()
    def showPlot(self,data):
        #print(data[0])
        #print(data[4].__len__())
        
        messured=data[0]
        prediction=data[1]
        self.plotlabelframe.config(text='Failuretest for: '+data[2])
        self.plotframe.destroy()
        self.plotframe=Frame(self.plotlabelframe)
        self.plotframe.pack(fill='both',expand='yes')
         
        f = Figure(figsize=(1, 1), dpi=100)
        a = f.add_subplot(111)
        self.line=a.scatter(messured, prediction, edgecolors=(0, 0, 0))
        a.plot([messured.min(), messured.max()], [messured.min(), messured.max()], 'k--', lw=1)
        a.set_xlabel('Measured')
        a.set_ylabel('Predicted')
        
        self.feat=[]
        for i in range (data[3].__len__()):
            self.feat.append(a.annotate(data[3][i], (messured[i],prediction[i]),
                                        bbox=dict(boxstyle="round", fc="w")))
            self.feat[i].set_visible(False)
        #canvas.mpl_connect('motion_notify_event', self.on_plot_hover) 
        
        self.canvas = FigureCanvasTkAgg(f, master=self.plotframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(self.canvas, self.plotframe)
        toolbar.update()
        self.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)
        self.canvas._tkcanvas.pack(side='top', fill='both', expand='yes')