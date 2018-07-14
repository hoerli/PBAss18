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
from gui.limeWindowGui import LimeWindowGui
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
        
        self.plotlabelframe=LabelFrame(self,text='Failure Test')
        self.plotframe=Frame(self.plotlabelframe)
        self.plotframe.pack(fill='both',expand='yes')
        self.plotlabelframe.pack(fill='both',expand='yes',padx=20)
        
        self.master.creatExplanationMenu(self,0)
    def browseButton(self):
        file=askopenfilename(filetypes=[("CSV Files",".csv")])
        self.setFileEntry(file)
    def setFileEntry(self,file):
        self.fileentry.config(state='normal')
        self.fileentry.delete(0, END)
        self.fileentry.insert(0, file)
        self.fileentry.config(state='readonly')
        self.failureTest()
    def failureTest(self):
        file=self.fileentry.get()
        data=ExplanationService.failureTest(file)
        if(data is None):
            messagebox.showerror('Failure test failed', 'Data must fit to the model and model must be loaded')
            return
        self.showPlot(data)
    def on_plot_hover(self,event):
        for i in range(self.feat.__len__()):
            self.feat[i].set_visible(False)
        if self.line.contains(event)[0]:
            ind = self.line.contains(event)[1]["ind"]
            self.feat[ind[0]].set_visible(True)  
        self.canvas.draw_idle()
    def on_click(self,event):
        if(self.line.contains(event)[0]):
            ind=self.line.contains(event)[1]['ind']
            ind=ind[0]
            file=self.fileentry.get()
            self.master.switch_frame(LimeWindowGui)
            self.master._frame.setFilePath(file,ind)
    def showPlot(self,data):
        
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
        a.set_xlabel('Measured('+data[2]+')')
        a.set_ylabel('Predicted('+data[2]+')')
        
        self.feat=[]
        for i in range (data[3].__len__()):
            self.feat.append(a.annotate(data[3][i], (messured[i],prediction[i]),
                                        bbox=dict(boxstyle="round", fc="w")))
            self.feat[i].set_visible(False)
        f.suptitle('Failure test for: '+ data[2]+'\nmousover item to see features\nClick on item show explanation of the tuple (lime)')
        self.canvas = FigureCanvasTkAgg(f, master=self.plotframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        toolbar = NavigationToolbar2Tk(self.canvas, self.plotframe)
        toolbar.update()
        self.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)
        self.canvas.mpl_connect('button_press_event',self.on_click)
        self.canvas._tkcanvas.pack(side='top', fill='both', expand='yes')