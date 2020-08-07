from tkinter import filedialog, Tk, ttk, END, StringVar, messagebox, DISABLED, NORMAL, Text
from dcclab.speckleAnalysis import speckleStatsReport, tkUtils
import matplotlib.pyplot as plt


class SpeckleStatsGUI(Tk):

    def __init__(self, *args, **kwargs):
        super(SpeckleStatsGUI, self).__init__(*args, **kwargs)
        self.protocol('WM_DELETE_WINDOW', self.__close_app)
        # self.resizable(False, False)
        self.title("Speckle Analysis DCCLab")
        header = ttk.Frame(self)
        header.pack()
        self.chooseFileButton = ttk.Button(header, text="Speckle image chooser", command=self.__speckleImageChooser)
        self.chooseFileButton.grid(column=0, row=0, padx=30, pady=30)
        self.filename = None
        self.tabPane = ttk.Notebook(self)
        self.tabPane.pack(expand=1, fill="both")
        self.__parametersTab()
        self.__speckleReport = None
        self.__tabsWidgets = []
        self.__fullReportPreviewButton = ttk.Button(header, text="Full report preview",
                                                    command=self.__fullReportPreview)
        self.__fullReportPreviewButton["state"] = DISABLED
        self.__fullReportPreviewButton.grid(column=1, row=0, padx=30, pady=30)
        self.__saveFullReportButton = ttk.Button(header, text="Save report to PDF", command=self.__saveFullReport)
        self.__saveFullReportButton["state"] = DISABLED
        self.__saveFullReportButton.grid(column=2, row=0, padx=30, pady=30)

    def __speckleImageChooser(self):
        supportedFiles = [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.tif;*.tiff")]
        speckleImagePath = filedialog.askopenfilename(title="Please select a speckle image...",
                                                      filetypes=supportedFiles)
        if self.filename is not None:
            self.__clearTabPaneExceptFirst()
        if speckleImagePath != '':
            self.filename = speckleImagePath
            self.title(f"Speckle Analysis DCCLab ({self.filename})")
            self.continueButton["state"] = NORMAL

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

        def continueButtonMethod(*args):
            method = methodVar.get()
            if method == "Neighbors average":
                method = "mean"
                methodParamName = "averageRange"
                supposedType = float
            else:
                method = "linear"
                methodParamName = "maxNbPoints"
                supposedType = int
            allParamsKwargs = {"imagePath": self.filename, "gaussianFilterNormalizationStdDev": gaussianStdDev.get(),
                               "medianFilterSize": medianFilterSize.get(),
                               "localContrastKernelSize": localContrastKernelSize.get(),
                               "intensityHistogramBins": nbBinsIntensityHist.get(),
                               "localContrastHistogramBins": nbBinsLocalContrast.get(), "FWHMFindingMethod": method,
                               methodParamName: FWHMFindingMethodParam.get()}
            supposedTypes = [str, float, int, int, int, int, str, supposedType]
            allValid = self.validateEntries(allParamsKwargs, supposedTypes)
            if allValid:
                if self.__speckleReport is not None:
                    self.__clearTabPaneExceptFirst()
                self.__speckleAnalysis(allParamsKwargs)
                self.__fullReportPreviewButton["state"] = NORMAL
                self.__saveFullReportButton["state"] = NORMAL

        self.continueButton = ttk.Button(paramsTab, text="Continue", command=continueButtonMethod, state=DISABLED)
        self.continueButton.grid(column=2, row=4, padx=30, pady=30)

    @classmethod
    def validateEntries(cls, entries: dict, supposedTypes: list):
        allValid = True
        allMsg = []
        for index, key in enumerate(entries):
            value = entries[key]
            supposedType = supposedTypes[index]
            entry, msg = cls.validateType(value, key, supposedType)
            entries[key] = entry
            if msg is not None:
                allMsg.append(msg)
        if len(allMsg) != 0:
            msg = '\n'.join(allMsg)
            messagebox.showerror("Invalid paramters(s)", msg)
            allValid = False
        return allValid

    @classmethod
    def validateType(cls, entry: str, paramName: str, supposedType: type):
        entryRightType = None
        msg = None
        try:
            entryRightType = supposedType(entry)
        except:
            msg = f"Parameter '{paramName}' cannot be interpreted as '{supposedType}'."
        return entryRightType, msg

    def __speckleAnalysis(self, kwargs: dict):
        self.__speckleReport = speckleStatsReport.SpeckleStatsReport(**kwargs)
        self.__speckleImageStatsTab()
        self.__speckleAutocorrelationStatsTab()
        self.__localContrastStatsTab()

    def __speckleImageStatsTab(self):
        speckleImageStatsTab = ttk.Frame(self.tabPane)
        self.tabPane.add(speckleImageStatsTab, text=f"Speckle image stats")
        self.tabPane.select(speckleImageStatsTab)
        speckleImageImages = ttk.Frame(speckleImageStatsTab)
        speckleImageImages.pack()
        speckleImageDisplay = ttk.Frame(speckleImageImages)
        intensityHistogram = ttk.Frame(speckleImageImages)
        speckleImageDisplay.grid(column=1, row=0, padx=5, pady=5)
        intensityHistogram.grid(column=2, row=0, padx=5, pady=5)
        imageFig = plt.figure()
        imageAx = imageFig.add_subplot(111)
        self.__speckleReport._displaySpeckleImagePrep(imageAx, "gray")
        embedImage = tkUtils.MatplotlibFigureEmbedder(speckleImageDisplay, imageFig)
        embedImage.embed(False)
        imageDetachButton = ttk.Button(speckleImageImages, text="Detach", command=self.__speckleImageDetach)
        imageDetachButton.grid(column=0, row=0, padx=5, pady=5)
        histDetachButton = ttk.Button(speckleImageImages, text="Detach", command=self.__intensityHistDetach)
        histDetachButton.grid(column=3, row=0, padx=5, pady=5)
        imageHist = plt.figure()
        histAx = imageHist.add_subplot(111)
        self.__speckleReport._intensityHistogramDisplayPrep(histAx)
        embedHist = tkUtils.MatplotlibFigureEmbedder(intensityHistogram, imageHist)
        embedHist.embed(False)
        imageStatsText = self.__speckleReport.speckleImageStats()
        imageStats = Text(speckleImageStatsTab, height=8, width=100)
        imageStats.insert(END, imageStatsText)
        imageStats["state"] = DISABLED
        imageStats.pack()
        self.__tabsWidgets.extend([speckleImageStatsTab, speckleImageImages, speckleImageDisplay, intensityHistogram,
                                   imageDetachButton, histDetachButton, imageStats])

    def __speckleAutocorrelationStatsTab(self):
        speckleAutocorrStatsTab = ttk.Frame(self.tabPane)
        self.tabPane.add(speckleAutocorrStatsTab, text=f"Speckle autocorrelation stats")
        specklAutocorrImages = ttk.Frame(speckleAutocorrStatsTab)
        specklAutocorrImages.pack()
        speckleAutocorrDisplay = ttk.Frame(specklAutocorrImages)
        speckleAutocorrSlices = ttk.Frame(specklAutocorrImages)
        speckleAutocorrDisplay.grid(column=1, row=0, padx=5, pady=5)
        speckleAutocorrSlices.grid(column=2, row=0, padx=5, pady=5)
        autocorrFig = plt.figure()
        autocorrFigAxe = autocorrFig.add_subplot(111)
        self.__speckleReport._displayAutocorrPrep(autocorrFigAxe, None, True, autocorrFig)
        embedImage = tkUtils.MatplotlibFigureEmbedder(speckleAutocorrDisplay, autocorrFig)
        embedImage.embed(False)
        autocorrDetachButton = ttk.Button(specklAutocorrImages, text="Detach", command=self.__fullAutocorrDetach)
        autocorrDetachButton.grid(column=0, row=0, padx=5, pady=5)
        slicesDetachButton = ttk.Button(specklAutocorrImages, text="Detach", command=self.__autocorrSlicesDetach)
        slicesDetachButton.grid(column=3, row=0, padx=5, pady=5)
        slicesFig = plt.figure()
        ax1 = slicesFig.add_subplot(211)
        ax2 = slicesFig.add_subplot(212)
        self.__speckleReport._displayAutocorrSlicesPrep(slicesFig, ax1, ax2)
        embedAutocorrSlices = tkUtils.MatplotlibFigureEmbedder(speckleAutocorrSlices, slicesFig)
        embedAutocorrSlices.embed(False)
        autocorrStatsText = self.__speckleReport.specklesStats()
        autocorrStats = Text(speckleAutocorrStatsTab, height=8, width=100)
        autocorrStats.insert(END, autocorrStatsText)
        autocorrStats["state"] = DISABLED
        autocorrStats.pack()
        self.__tabsWidgets.extend(
            [speckleAutocorrStatsTab, specklAutocorrImages, speckleAutocorrDisplay, speckleAutocorrSlices,
             autocorrDetachButton, slicesDetachButton, autocorrStats])

    def __localContrastStatsTab(self):
        localContrastStatsTab = ttk.Frame(self.tabPane)
        self.tabPane.add(localContrastStatsTab, text=f"Speckle local contrast stats")
        localContrastImages = ttk.Frame(localContrastStatsTab)
        localContrastImages.pack()
        localContrastImage = ttk.Frame(localContrastImages)
        localContrastHist = ttk.Frame(localContrastImages)
        localContrastImage.grid(column=1, row=0, padx=5, pady=5)
        localContrastHist.grid(column=2, row=0, padx=5, pady=5)
        localContrastFig = plt.figure()
        localContrastAx = localContrastFig.add_subplot(111)
        self.__speckleReport._displayLocalContrastPrep(localContrastAx, None)
        embedImage = tkUtils.MatplotlibFigureEmbedder(localContrastImage, localContrastFig)
        embedImage.embed(False)
        imageDetachButton = ttk.Button(localContrastImages, text="Detach", command=self.__localContrastDetach)
        imageDetachButton.grid(column=0, row=0, padx=5, pady=5)
        histDetachButton = ttk.Button(localContrastImages, text="Detach", command=self.__localContrastHistDetach)
        histDetachButton.grid(column=3, row=0, padx=5, pady=5)
        imageHist = plt.figure()
        histAx = imageHist.add_subplot(111)
        self.__speckleReport._localContrastHistogramDisplayPrep(histAx)
        embedHist = tkUtils.MatplotlibFigureEmbedder(localContrastHist, imageHist)
        embedHist.embed(False)
        imageStatsText = self.__speckleReport.localContrastStats()
        imageStats = Text(localContrastStatsTab, height=8, width=100)
        imageStats.insert(END, imageStatsText)
        imageStats["state"] = DISABLED
        imageStats.pack()
        self.__tabsWidgets.extend([localContrastStatsTab, localContrastImages, localContrastImage, localContrastHist,
                                   imageDetachButton, histDetachButton, imageStats])

    def __fullReportPreview(self):
        msg = "When saving the report to pdf, the layout changes a little to fit into 8.5 inches by 11 inches."
        messagebox.showwarning("Final display", message=msg)
        self.__speckleReport.fullGraphicsReportDisplay()

    def __saveFullReport(self):
        savedFname = filedialog.asksaveasfilename(title="Save report...",
                                                  filetypes=[("Portable Document FIle", "*.pdf")])
        if not savedFname.endswith(".pdf"):
            savedFname += ".pdf"
        self.__speckleReport.fullGrahicsReportCreation(savedFname)
        return savedFname

    def __localContrastHistDetach(self):
        self.__speckleReport.displayLocalContrastHistogram()

    def __localContrastDetach(self):
        self.__speckleReport.displayLocalContrast()

    def __speckleImageDetach(self):
        self.__speckleReport.displaySpeckleImage("gray")

    def __intensityHistDetach(self):
        self.__speckleReport.displayIntensityHistogram()

    def __fullAutocorrDetach(self):
        self.__speckleReport.displayFullAutocorrelation()

    def __autocorrSlicesDetach(self):
        self.__speckleReport.displayAutocorrelationSlices()

    def __clearTabPaneExceptFirst(self):
        # Clear everything and destroy every widget present (prevent memory leaks)
        for tab in self.tabPane.tabs()[1:]:
            self.tabPane.forget(tab)
        for widget in self.__tabsWidgets:
            widget.destroy()
        self.__tabsWidgets.clear()

    def __close_app(self):
        if messagebox.askokcancel("Close", "Are you sure you want to quit? All unsaved progress will be lost."):
            self.quit()


if __name__ == '__main__':
    app = SpeckleStatsGUI()
    app.mainloop()
