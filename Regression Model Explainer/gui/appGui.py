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
from gui.explantionFeatureWindowGui import ExplanationFeatureWindowGui

class AppGui(Tk):
    ''' Gui for the application
    creates a menu
    using tkinter lib
    '''
    def __init__(self):
        Tk.__init__(self)
        self.topologytest=False
        self.perfomancetest=False
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
        ''' method to switch frames
        '''
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill ='both',expand='yes')
    def createMenu(self):
        ''' method to create the menu
        '''
        self.menu = Menu(self)
        self.config(menu=self.menu)
        
        self.datamenu= Menu(self.menu)
        self.menu.add_cascade(label='Data',menu=self.datamenu)
        self.datamenu.add_command(label='Load Model', command=self.loadModel)
        self.datamenu.add_command(label='Save Model', command=self.modelSave)
        
        self.modelmenu= Menu(self.menu)
        self.menu.add_cascade(label="Model",menu=self.modelmenu)
        self.modelmenu.add_command(label="Explanation", command=self.explanation)
        self.modelmenu.add_command(label="Show Model Information", command=self.showModelInformation)
        
        self.nn = Menu(self.menu)
        self.menu.add_cascade(label="Neural Network", menu=self.nn)
        self.nn.add_command(label="Create/Train neural network", command=lambda: self.switch_frame(NnWindowGui))
        self.nn.add_command(label='Predict TestData',command=self.predictTestData)
        self.nn.add_command(label='Predict',command=self.predictSingleData)
        self.nn.add_command(label='Evaluate Neural Network with KerasRegressor(10-fold cross validation)', command=self.topologyTest)
        self.nn.add_command(label='Neural Network Performance test', command=self.perfomanceTest)
    def disabelMenu(self):
        self.menu.entryconfigure('Data', state='disabled')
        self.menu.entryconfigure('Neural Network', state='disabled')
        self.menu.entryconfigure('Model', state='disabled')
    def enableMenu(self):
        self.menu.entryconfigure('Data', state='normal')
        self.menu.entryconfigure('Neural Network', state='normal')
        self.menu.entryconfigure('Model', state='normal')
    def predictTestData(self):
        mds=ModelDataService()
        if(mds.getModel() is None):
            messagebox.showwarning('No Model', 'Create or load model')
            self.switch_frame(MainWindowGui)
            return
        self.switch_frame(PredictDataSetWindowGUI)
    def predictSingleData(self):
        mds=ModelDataService()
        if(mds.getModel() is None):
            messagebox.showwarning('No Model', 'Create or load model')
            self.switch_frame(MainWindowGui)
            return
        self.switch_frame(PredictSingleDataWindowGui)
    def explanation(self):
        mds=ModelDataService()
        if(mds.getModel() is None):
            messagebox.showwarning('No Model', 'Create or load model')
            self.switch_frame(MainWindowGui)
            return
        self.switch_frame(FailureTestWindowGui)
    def showModelInformation(self):
        mds=ModelDataService()
        if(mds.getModel() is None):
            messagebox.showwarning('No Model', 'Create or load model')
            self.switch_frame(MainWindowGui)
            return
        self.switch_frame(ShowModelInformationGui)
    def modelSave(self):
        ''' method to save a model and its data
        '''
        file = asksaveasfilename(filetypes=[("Model Files",".model")])
        mds=ModelDataService()
        issaved=mds.saveModel(file)
        if(issaved):
            messagebox.showinfo('Saved', 'Model is saved to: '+str(file)+'.model')
            self.switch_frame(ShowModelInformationGui)
        else:
            messagebox.showerror('Not Saved', 'There is no model created or loaded to Save')
    def loadModel(self):
        ''' method to load a model and its data
        '''
        file=askopenfilename(filetypes=[("Model Files",".model")])
        mds=ModelDataService()
        isloaded=mds.loadModel(file)
        if(isloaded):
            messagebox.showinfo('Loaded', 'The Model: '+file+', is loaded')
            self.switch_frame(ShowModelInformationGui)
        else:
            messagebox.showerror('Not Loaded', 'The model is not Loaded')
    def topologyTest(self):
        self.topologytest=True
        self.switch_frame(NnWindowGui)
    def perfomanceTest(self):
        self.perfomancetest=True
        self.switch_frame(NnWindowGui)
    def trainNeuralNetwork(self):
        self.switch_frame(NnWindowGui)