from tkinter import Frame
from tkinter import Scrollbar
from tkinter import Canvas
from tkinter import NW

class Scrollable(Frame):
    ''' To add a horizontal scrollbar to a frame
    '''
    def __init__(self, frame):
        scrollbar = Scrollbar(frame,orient='horizontal')
        scrollbar.pack( fill='x', expand=False)
        self.canvas = Canvas(frame, xscrollcommand=scrollbar.set)
        self.canvas.pack( fill='x')
        scrollbar.config(command=self.canvas.xview)
        self.canvas.bind('<Configure>', self.__fill_canvas)
        Frame.__init__(self, frame)         
        self.windows_item = self.canvas.create_window(0,0, window=self,anchor=NW)
    def __fill_canvas(self, event):
        canvas_height = event.height
        self.canvas.itemconfig(self.windows_item, height = canvas_height)        
    def update(self):
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))