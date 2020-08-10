from tkinter import TOP, BOTH, Toplevel, Label, Widget, LEFT, SOLID

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class MatplotlibFigureEmbedder:

    def __init__(self, root: Widget, figure: Figure):
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


class ToolTip:

    def __init__(self, rootWidget: Widget, text: str):
        self.root = rootWidget
        self.text = text
        self.ttipWindow = None

    def popTip(self):
        if self.ttipWindow is not None:
            return None
        x, y, width, height = self.root.bbox("insert")
        x += self.root.winfo_rootx() + 57
        y += height + self.root.winfo_rooty() + 27
        self.ttipWindow = Toplevel(self.root)
        self.ttipWindow.wm_overrideredirect(1)
        self.ttipWindow.wm_geometry(f"+{x}+{y}")
        Label(self.ttipWindow, text=self.text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1,
              font=("tahoma", "8", "normal")).pack()

    def hideTip(self):
        if self.ttipWindow is not None:
            self.ttipWindow.destroy()
            self.ttipWindow = None


class ToolTipBind:

    def __init__(self, rootWidget: Widget, text: str):
        ttip = ToolTip(rootWidget, text)

        def enterHover(*args):
            ttip.popTip()

        def leaveHover(*args):
            ttip.hideTip()

        rootWidget.bind("<Enter>", enterHover)
        rootWidget.bind("<Leave>", leaveHover)
