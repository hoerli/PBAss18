from tkinter.filedialog import asksaveasfilename
from services.modelDataService import ModelDataService
class SaveModelGui():
    def __init__(self,mmgui):
        self.mds=ModelDataService()
        self.mmgui=mmgui
    def setSavePath(self):
        savefilepath = asksaveasfilename(filetypes=[("Model Files",".model")])
        test=self.mds.saveModel(savefilepath)
        if(test):
            self.mmgui.errorMessage('Model Saved','Model Saved at: '+savefilepath)
        else:
            self.mmgui.errorMessage('Failed to save model, something went wrong maybe their is no model created')
        self.mmgui.createMainWindowLabel()