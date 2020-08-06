from tkinter import Tk, TOP, BOTH

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class MatplotlibFigureEmbedder:

    def __init__(self, root: Tk, figure: Figure):
        self.root = root
        self.figure = figure

    def embed(self, withToolbar: bool = True):
        canvas = self.__drawCanvas()
        if withToolbar:
            self.__addToolbar(canvas)
        return self.root

    def __drawCanvas(self):
        canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        return canvas

    def __addToolbar(self, canvas: FigureCanvasTkAgg):
        toolbar = NavigationToolbar2Tk(canvas, self.root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        return toolbar
