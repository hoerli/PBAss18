from services.modelDataService import ModelDataService
from tkinter.filedialog import askopenfilename
class LoadModelGui():
    def __init__(self,mmgui):
        self.mds=ModelDataService()
        self.mmgui=mmgui
    def setLoadPath(self):
        loadfilepath = askopenfilename(filetypes=[("Model Files",".model")])
        test=self.mds.loadModel(loadfilepath)
        if(test):
            self.mmgui.errorMessage('Model Loaded','Model: '+loadfilepath+' loaded')
        else:
            self.mmgui.errorMessage('Model loaded failed','Could not load Model')
        self.mmgui.createMainWindowLabel()