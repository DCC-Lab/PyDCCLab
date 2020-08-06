from tkinter import filedialog, Tk, ttk, END, StringVar


class SpeckleStatsGUI(Tk):

    def __init__(self, *args, **kwargs):
        super(SpeckleStatsGUI, self).__init__(*args, **kwargs)
        self.title("Speckle Analysis DCCLab")
        self.chooseFileButton = ttk.Button(self, text="Speckle image chooser", command=self.__speckleImageChooser)
        self.chooseFileButton.pack()
        self.filename = None
        self.tabPane = ttk.Notebook(self)
        self.tabPane.pack(expand=1, fill="both")
        self.__parametersTab()

    def __speckleImageChooser(self):
        supportedFiles = [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.tif;*.tiff")]
        speckleImagePath = filedialog.askopenfilename(title="Please select a speckle image...",
                                                      filetypes=supportedFiles)
        if self.filename is not None:
            # TODO : Flush tabs, clear notebook and reload stuff?
            pass
        self.filename = speckleImagePath
        self.title(f"Speckle Analysis DCCLab ({self.filename})")

    def __parametersTab(self):
        methodVar = StringVar(self)
        FWHMFindingMethodParamTextDefault = "Error range for including neighbors (0 to 1) : "

        paramsTab = ttk.Frame(self.tabPane)
        self.tabPane.add(paramsTab, text="Analysis parameters")

        ttk.Label(paramsTab, text="Gaussian normalization filter standard deviation : ").grid(column=0, row=0, padx=30,
                                                                                              pady=30)
        gaussianStdDev = ttk.Entry(paramsTab)
        gaussianStdDev.insert(END, "75")
        gaussianStdDev.grid(column=1, row=0, padx=30, pady=30)

        ttk.Label(paramsTab, text="Median filter size : ").grid(column=0, row=1, padx=30, pady=30)
        medianFilterSize = ttk.Entry(paramsTab)
        medianFilterSize.insert(END, "3")
        medianFilterSize.grid(column=1, row=1, padx=30, pady=30)

        ttk.Label(paramsTab, text="Local contrast kernel size : ").grid(column=0, row=2, padx=30, pady=30)
        localContrastKernelSize = ttk.Entry(paramsTab)
        localContrastKernelSize.insert(END, "7")
        localContrastKernelSize.grid(column=1, row=2, padx=30, pady=30)

        ttk.Label(paramsTab, text="Intensity histogram number of bins : ").grid(column=2, row=0, padx=30, pady=30)
        nbBinsIntensityHist = ttk.Entry(paramsTab)
        nbBinsIntensityHist.insert(END, "256")
        nbBinsIntensityHist.grid(column=3, row=0, padx=30, pady=30)

        ttk.Label(paramsTab, text="Local contrast histogram number of bins : ").grid(column=2, row=1, padx=30, pady=30)
        nbBinsLocalContrast = ttk.Entry(paramsTab)
        nbBinsLocalContrast.insert(END, "256")
        nbBinsLocalContrast.grid(column=3, row=1, padx=30, pady=30)

        ttk.Label(paramsTab, text="FWHM/diameter finding method : ").grid(column=2, row=2, padx=30, pady=30)
        choices = ["Neighbors average", "Linear fit"]
        method = ttk.OptionMenu(paramsTab, methodVar, choices[0], *choices)
        method.grid(column=3, row=2, padx=30, pady=30)

        FWHMFindingParamLabel = ttk.Label(paramsTab, text=FWHMFindingMethodParamTextDefault)
        FWHMFindingParamLabel.grid(column=2, row=3, padx=30, pady=30)
        FWHMFindingMethodParam = ttk.Entry(paramsTab)
        FWHMFindingMethodParam.insert(END, "0.2")
        FWHMFindingMethodParam.grid(column=3, row=3, padx=30, pady=30)

        def onFWHMFindingMethodChange(*args):
            if methodVar.get() == "Neighbors average":
                FWHMFindingParamLabel["text"] = FWHMFindingMethodParamTextDefault
                FWHMFindingMethodParam.delete(0, END)
                FWHMFindingMethodParam.insert(END, "0.2")
            else:
                FWHMFindingParamLabel["text"] = "Maximum number of points for the fit : "
                FWHMFindingMethodParam.delete(0, END)
                FWHMFindingMethodParam.insert(END, "10")

        methodVar.trace("w", onFWHMFindingMethodChange)


if __name__ == '__main__':
    app = SpeckleStatsGUI()
    app.mainloop()
