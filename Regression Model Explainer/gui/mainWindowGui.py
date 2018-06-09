from tkinter import Frame
from tkinter import Label
from PIL import ImageTk,Image
class MainWindowGui(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.img = ImageTk.PhotoImage(Image.open("gui/1503825-200.png"))
        panel = Label(self, image = self.img)
        panel.pack(fill = "both", expand = "yes")
        panel.config(bg='white')