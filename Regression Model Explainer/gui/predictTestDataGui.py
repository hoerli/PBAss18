from tkinter import messagebox
from services.loadCsvService import LoadCsvService
from tkinter.filedialog import askopenfilename
from services.modelDataService import ModelDataService
from services.KerasNNService import KerasNNService
from tkinter import ttk
from tkinter.constants import BOTH
class PredictTestDataGui():
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
    def errorMessage(self,title,message):
        messagebox.showerror(title, message)
    def createWindow(self,file):
        print('Main Window')
        nns=KerasNNService()
        mds=ModelDataService()
        lcsvs=LoadCsvService(mds.getDataPath())
        predict=nns.predict(file)
        if(predict.__len__()<1):
            if(mds.getModel()==None):
                self.errorMessage('No Model', 'You have to create a Model first')
            else:
                self.errorMessage('Wrong test Data', 'the Data must have the same shape as the model\nInput dim: '+str(lcsvs.getNumberOfInput())+'\nOutput feature: '+mds.getOutputvar())
        else:
            lcsvs=LoadCsvService(file)
            features=lcsvs.getTagList()
            tags=[]
            for i in range(features.__len__()):
                if(features[i]==mds.getOutputvar()):
                    print('')
                else:
                    tags.append(features[i])
            tags.append('m: '+mds.getOutputvar())
            tags.append('p: '+mds.getOutputvar())
            self.mmgui.delete()
            tree = ttk.Treeview(self.mmgui.root, selectmode='browse')
            tree.pack(side='left',expand=True,fill=BOTH)
            self.mmgui.input.append(tree)
            
            vsb = ttk.Scrollbar(self.mmgui.root, orient="vertical", command=tree.yview)
            vsb.pack(side='right', fill='y')
            self.mmgui.input.append(vsb)
            
            col=[]
            for i in range(tags.__len__()):
                col.append(str(i+1))

            tree["columns"] = col
            tree['show'] = 'headings'
            
            for i in range(tags.__len__()):
                tree.column(col[i],width=100,anchor='c')
            for i in range(tags.__len__()):
                tree.heading(col[i],text=tags[i])
            input=lcsvs.getInputArray(mds.getOutputvar())
            output=lcsvs.getOutputArray(mds.getOutputvar())
            for i in range(input.__len__()):
                innumber=[]
                for x in range(input[i].__len__()):
                    innumber.append(input[i][x])
                innumber.append(output[i])
                innumber.append(predict[i])
                tree.insert("",'end',text="",values=innumber)