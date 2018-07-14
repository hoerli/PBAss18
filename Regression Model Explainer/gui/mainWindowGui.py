from tkinter import Frame
from tkinter import Label
from tkinter import Button
from PIL import ImageTk,Image
from services.modelDataService import ModelDataService
class MainWindowGui(Frame):
    ''' Frame for the start Window
    '''
    def __init__(self,master):
        Frame.__init__(self, master)
        self.img = ImageTk.PhotoImage(Image.open("gui/1503825-200.png"))
        panel = Label(self, image = self.img)
        panel.pack(fill = "both", expand = "yes")
        panel.config(bg='white')
        mds=ModelDataService()
        if(mds.getModel() is None):
            label=Label(panel,text='No Model\nCreate or Load Model',bg='white')
            label.pack()
            createbutton=Button(panel,text='Create Model',bg='white',command=self.master.trainNeuralNetwork)
            createbutton.pack()
            loadmodelbutton=Button(panel,text='Load Model',bg='white',command=self.master.loadModel)
            loadmodelbutton.pack()
        else:
            showmodelbutton=Button(panel,text='Show Model Information',bg='white',command=self.master.showModelInformation)
            showmodelbutton.pack()
            explbutton=Button(panel,text='Explain Model',bg='white',command=self.master.explanation)
            explbutton.pack()