from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from services.loadCsvService import LoadCsvService
from services.failureTestService import FailureTestService
import matplotlib.pyplot as plt
class FailureTestGui():
    def __init__(self,mmgui):
        self.mmgui=mmgui
    def loadCsv(self):
        file = askopenfilename(filetypes=[("CSV Files",".csv")])
        lcsvs=LoadCsvService(file)
        test=lcsvs.testCsv()
        if(file == '' or not test):
            self.errorMessage('Wrong File', 'The File: '+file+' is not compatible')
            self.mmgui.delete()
            self.mmgui.createMainWindowLabel()
        else:
            self.createWindow(file)
    def createWindow(self,file):
        fts=FailureTestService()
        data=fts.getTestData(file)
        if(data.__len__()==2):
            print(data[0])
            print(data[1])
            prediction=data[0]
            Y=data[1]
            
            fig, ax = plt.subplots()
            ax.scatter(Y, prediction, edgecolors=(0, 0, 0))
            ax.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'k--', lw=1)
            ax.set_xlabel('Measured')
            ax.set_ylabel('Predicted')
            plt.show()
        else:
            self.errorMessage('No Model', 'You have t create or load a Model first')
    def errorMessage(self,title,message):
        messagebox.showerror(title, message)