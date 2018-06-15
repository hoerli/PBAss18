from tkinter import Tk
from tkinter import Menu
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename

from gui.mainWindowGui import MainWindowGui
from gui.nnWindowGui import NnWindowGui
from gui.showModelInformationGui import ShowModelInformationGui
from gui.predictDataSetWindowGui import PredictDataSetWindowGUI
from gui.predictSingleDataWindowGui import PredictSingleDataWindowGui
from services.modelDataService import ModelDataService
from gui.failureTestWindowGui import FailureTestWindowGui
from gui.overallExplanationWindowGui import OverallExplanationWindowGui
from gui.limeWindowGui import LimeWindowGui

class AppGui(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.topologytest=False
        self.title("Regression Model Explainer")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.minsize(round(width/2), round(height/2))
        windowWidth = width/2
        windowHeight = height/2
        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)
        self.geometry("+{}+{}".format(positionRight, positionDown))
        
        self.iconbitmap('gui/icon.ico')
        
        self.createMenu()
        self._frame = None
        self.switch_frame(MainWindowGui)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill ='both',expand='yes')
    def createMenu(self):
        self.menu = Menu(self)
        self.config(menu=self.menu)
        
        self.main= Menu(self.menu)
        self.menu.add_cascade(label="Main",menu=self.main)
        self.main.add_command(label="Main Window", command=lambda: self.switch_frame(MainWindowGui))
        self.main.add_command(label="Exit", command=exit)

        self.nn = Menu(self.menu)
        self.menu.add_cascade(label="Neural Network", menu=self.nn)
        self.nn.add_command(label="Save Model", command=self.modelSave)
        self.nn.add_command(label="Load Model", command=self.loadModel)
        self.nn.add_command(label="Create/Train neural network", command=lambda: self.switch_frame(NnWindowGui))
        self.nn.add_command(label='Predict TestData',command=lambda: self.switch_frame(PredictDataSetWindowGUI))
        self.nn.add_command(label='Predict',command=lambda: self.switch_frame(PredictSingleDataWindowGui))
        self.nn.add_command(label='Show Model Information',command=lambda: self.switch_frame(ShowModelInformationGui))
        
        self.expm= Menu(self.menu)
        self.menu.add_cascade(label='Explanation', menu=self.expm)
        self.expm.add_command(label="Failure Test",command=lambda: self.switch_frame(FailureTestWindowGui))
        self.expm.add_command(label='Single instance Explanation(Lime)',command=lambda: self.switch_frame(LimeWindowGui))
        self.expm.add_command(label='Overall explanation',command=lambda: self.switch_frame(OverallExplanationWindowGui))
        self.expm.add_command(label='Explanation Feature', command=exit)
        self.expm.add_command(label='Localy Explanation',command=exit)
        
        self.nntest = Menu(self.menu)
        self.menu.add_cascade(label='Neural Network Tests', menu=self.nntest)
        self.nntest.add_command(label='Evaluate Neural Network with KerasRegressor(10-fold cross validation)', command=self.topologyTest)
        self.nntest.add_command(label='Neural Network Performance test', command=exit)
    def disabelMenu(self):
        self.menu.entryconfigure('Main', state='disabled')
        self.menu.entryconfig('Neural Network', state='disabled')
        self.menu.entryconfigure('Explanation', state='disabled')
        self.menu.entryconfigure('Neural Network Tests', state='disabled')
    def enableMenu(self):
        self.menu.entryconfigure('Main', state='normal')
        self.menu.entryconfig('Neural Network', state='normal')
        self.menu.entryconfigure('Explanation', state='normal')
        self.menu.entryconfigure('Neural Network Tests', state='normal')
    def modelSave(self):
        file = asksaveasfilename(filetypes=[("Model Files",".model")])
        mds=ModelDataService()
        issaved=mds.saveModel(file)
        if(issaved):
            messagebox.showinfo('Saved', 'Model is saved to: '+str(file)+'.model')
        else:
            messagebox.showerror('Not Saved', 'There is no model created or loaded to Save')
    def loadModel(self):
        file=askopenfilename(filetypes=[("Model Files",".model")])
        mds=ModelDataService()
        isloaded=mds.loadModel(file)
        if(isloaded):
            messagebox.showinfo('Loaded', 'The Model: '+file+', is loaded')
        else:
            messagebox.showerror('Not Loaded', 'The model is not Loaded')
    def topologyTest(self):
        self.topologytest=True
        self.switch_frame(NnWindowGui)