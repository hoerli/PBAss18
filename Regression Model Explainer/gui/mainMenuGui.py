from tkinter import *
#from gui.labelred import labegui
from PIL import ImageTk, Image
from tkinter import messagebox
#from gui.createNeuralNetworkGui import CreateNeuralNetworkGui
from gui.createTrainNNGui import CreateTrainNNGui
from gui.predictTestDataGui import PredictTestDataGui
from gui.failureTestGui import FailureTestGui

class MainMenuGui():
    def __init__(self):
        self.root= Tk()
        self.root.title("Regression Model Explainer")
        #self.root.iconbitmap('icon.ico')
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        #self.root.geometry('%sx%s' % (round(width/2), round(height/2)))
        self.root.minsize(round(width/2), round(height/2))
        windowWidth = width/2
        windowHeight = height/2
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        self.root.configure(bg='white')
        self.root.iconbitmap('gui/icon.ico')
        img = ImageTk.PhotoImage(Image.open("gui/1503825-200.png"))
        panel = Label(self.root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        panel.configure(bg='white')
        self.input=[]
        self.input.append(panel)
        self.createMenu()
    def createMainWindowLabel(self):
        self.delete()
        img = ImageTk.PhotoImage(Image.open("gui/1503825-200.png"))
        panel = Label(self.root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        panel.configure(bg='white')
        self.input.append(panel)
        self.root.mainloop()
    def delete(self):
        self.enableNNMenu("Create/Train neural network")
        for i in range(self.input.__len__()):
            self.input[i].destroy()
    def LoadModel(self):
        self.errorMessage('Not Implemented', 'Load Model isnt implemented Now')
    def SaveModel(self):
        self.errorMessage('Not Implemented', 'Save Model isnt implemented Now')
    def createNeuralNetwork(self):
        ctn = CreateTrainNNGui(self)
        ctn.loadCsv()
    def predictTestData(self):
        ptd = PredictTestDataGui(self)
        ptd.loadCsv()
    def showModelInformation(self):
        ctn = CreateTrainNNGui(self)
        ctn.TrainWindow(False)
    def failureTest(self):
        ftg=FailureTestGui(self)
        ftg.loadCsv()
    def singleInstanceExplanation(self):
        self.errorMessage('Not Implemented', 'Single Instance Explanation with Lime isnt implemented Now')
    def overallExplanation(self):
        self.errorMessage('Not Implemented', 'Overall Explanation isnt implemented Now')
    def explanationFeature(self):
        self.errorMessage('Not Implemented', 'Explanation Feature isnt implemented Now')
    def localyExplanation(self):
        self.errorMessage('Not Implemented', 'Localy Explanation isnt implemented Now')
    def estimateWithMissingValues(self):
        self.errorMessage('Not Implemented', 'Estimate with missing values isnt implemented Now')
    def neuralNetworkPerformanceTest(self):
        self.errorMessage('Not Implemented', 'Neural Network Performance test isnt implemented Now')
    def createMenu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        
        self.main= Menu(menu)
        menu.add_cascade(label="Main",menu=self.main)
        self.main.add_command(label="Main Window", command=self.createMainWindowLabel)
        self.main.add_command(label="Exit", command=exit)
        
        self.nn = Menu(menu)
        menu.add_cascade(label="Neural Network", menu=self.nn)
        self.nn.add_command(label="Save Model", command=self.SaveModel)
        self.nn.add_command(label="Load Model", command=self.LoadModel)
        self.nn.add_command(label="Create/Train neural network", command=self.createNeuralNetwork)
        self.nn.add_command(label='Predict TestData',command=self.predictTestData)
        self.nn.add_command(label='Show Model Information',command=self.showModelInformation)
        
        self.expm= Menu(menu)
        menu.add_cascade(label='Explanation', menu=self.expm)
        self.expm.add_command(label="Failure Test",command=self.failureTest)
        self.expm.add_command(label='Single instance Explanation(Lime)',command=self.singleInstanceExplanation)
        self.expm.add_command(label='Overall explanation',command=self.overallExplanation)
        self.expm.add_command(label='Explanation Feature', command=self.explanationFeature)
        self.expm.add_command(label='Localy Explanation',command=self.localyExplanation)
        
        self.nntest = Menu(menu)
        menu.add_cascade(label='Neural Network Tests', menu=self.nntest)
        self.nntest.add_command(label='Estimate with missing values', command=self.estimateWithMissingValues)
        self.nntest.add_command(label='Neural Network Performance test', command=self.neuralNetworkPerformanceTest)
        self.root.mainloop()
    def disableNNMenu(self,opt):
        self.nn.entryconfig(opt, state="disabled")
    def enableNNMenu(self,opt):
        self.nn.entryconfig(opt, state="normal")
    def errorMessage(self,title,message):
        messagebox.showerror(title, message)