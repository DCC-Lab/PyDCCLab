from tkinter import filedialog, Tk, ttk, END, StringVar, messagebox, DISABLED, NORMAL, Text
from dcclab.speckleAnalysis import speckleStatsReport, tkUtils
import matplotlib.pyplot as plt
import warnings

gaussianStdHelp = "The image is normalized with a gaussian filter of a certain standard deviation.\nThis standard " \
                  "deviation can be seen as the 'size' of the filter.\nThe default value might be good enough in a " \
                  "lot of cases.\nThis normalization is good to remove intensity gradient or non uniformity."
medianFilterSizeHelp = "The image is filtered with a median filter of a certain size.\nThis size is important if the" \
                       " noise is intense, because a small filter may not be optimal.\nFor small salt & pepper noise," \
                       " a filter of a few pixels (less than 10) me be good enough.\nThe default value may be good." \
                       "\nThis filter is  important for speckle imaging, because there can be photon noise."
localContrastSizeHelp = "The computation of the local contrast requires a kernel size that determines the number of" \
                        " neighbors used to compute the local contrast.\nThe local contrast may be an interesting and" \
                        " important parameter in speckle imaging.\nThe local contrast kernel is based on the method " \
                        "used by Donald D. Duncan and al. in Statistics of local speckle contrast."
intensityHistBinsHelp = "The image intensity can be represented by an histogram.\nTo do so, a number of bins is " \
                        "required.\nThis number can be seen as the 'precision' of the histogram: if it is a small " \
                        "number, we may not have a good overview of the speckle intensity distribution.\nHowever, " \
                        "using a big number may have the same effect: if it is too large, we may have empty bins." \
                        "\nThe default value may be enough for images encoded in 8 bits unsigned integers, of floats." \
                        "\nWe can extract statistical properties of the speckles with this graph." \
                        "\nWe can extract statistical properties of the speckles with this graph."
localContrastBinsHelp = "The local contrast value can be represented as an histogram.\nTo do so, a number of bins is" \
                        " required.\nThis number can be seen as the 'precision' of the histogram: if it is a small " \
                        "number, we may not have a good overview of the speckle intensity distribution.\nHowever, " \
                        "using a big number may have the same effect: if it is too large, we may have empty bins." \
                        "\nThe default value may be enough for images encoded in 8 bits unsigned integers, of floats." \
                        "\nWe can extract statistical properties of the speckles with this graph."
methodHelp = "There is currently two possible methods that can be used to find the average speckle diameter.\nThe " \
             "speckle diameter is very close to the autocorrelation of the speckle image.\nSince the autocorrelation" \
             " is discrete, there is not an absolute way to find the full or the half width at the half maximum\n(" \
             "since the autocorrelation is normalized at a maximum of approximately 1, the half maximum is considered" \
             " at 0.5).\n\nThe first method uses a certain range of neighbors (define by a percentage) of upper and" \
             " lower neighbors. The mean value is then computed and this is the value that is kept to compute the" \
             " average diameter.\n\nThe second method is close to the first one, but instead of taking the mean, a " \
             "linear fit is done."
methodParamsHelp = "Neighbors method parameters:\nThe maximum range.\nIt is a number between 0 and 1 (a percentage) " \
                   "and it is used to find neighbors within 0.5 ± percentage.\n\n" \
                   "Linear fit method parameters:\nTme maximum number of neighbors.\nIt is an integer and it is used" \
                   " to find half this number of neighbors in the upper part (where y > 0.5) and the other half" \
                   " contains neighbors in the lower part (where y < 0.5).\nIn some cases, there may be not enough" \
                   " neighbors in the upper part, so that is why it is the maximum and not the absolute."


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

        gaussStdLabel = ttk.Label(paramsTab, text="Gaussian normalization filter standard deviation : ")
        gaussStdLabel.grid(column=0, row=0, padx=30, pady=30)
        gaussianStdDev = ttk.Entry(paramsTab)
        gaussianStdDev.insert(END, "75")
        gaussianStdDev.grid(column=1, row=0, padx=30, pady=30)
        tkUtils.ToolTipBind(gaussStdLabel, gaussianStdHelp)

        medianFilterLabel = ttk.Label(paramsTab, text="Median filter size : ")
        medianFilterLabel.grid(column=0, row=1, padx=30, pady=30)
        medianFilterSize = ttk.Entry(paramsTab)
        medianFilterSize.insert(END, "3")
        medianFilterSize.grid(column=1, row=1, padx=30, pady=30)
        tkUtils.ToolTipBind(medianFilterLabel, medianFilterSizeHelp)

        localContrastSizeLabel = ttk.Label(paramsTab, text="Local contrast kernel size : ")
        localContrastSizeLabel.grid(column=0, row=2, padx=30, pady=30)
        localContrastKernelSize = ttk.Entry(paramsTab)
        localContrastKernelSize.insert(END, "7")
        localContrastKernelSize.grid(column=1, row=2, padx=30, pady=30)
        tkUtils.ToolTipBind(localContrastSizeLabel, localContrastSizeHelp)

        intensityHistLabel = ttk.Label(paramsTab, text="Intensity histogram number of bins : ")
        intensityHistLabel.grid(column=2, row=0, padx=30, pady=30)
        nbBinsIntensityHist = ttk.Entry(paramsTab)
        nbBinsIntensityHist.insert(END, "256")
        nbBinsIntensityHist.grid(column=3, row=0, padx=30, pady=30)
        tkUtils.ToolTipBind(intensityHistLabel, intensityHistBinsHelp)

        localContrastBinsLabel = ttk.Label(paramsTab, text="Local contrast histogram number of bins : ")
        localContrastBinsLabel.grid(column=2, row=1, padx=30, pady=30)
        nbBinsLocalContrast = ttk.Entry(paramsTab)
        nbBinsLocalContrast.insert(END, "256")
        nbBinsLocalContrast.grid(column=3, row=1, padx=30, pady=30)
        tkUtils.ToolTipBind(localContrastBinsLabel, localContrastBinsHelp)

        methodLabel = ttk.Label(paramsTab, text="FWHM/diameter finding method : ")
        methodLabel.grid(column=2, row=2, padx=30, pady=30)
        choices = ["Neighbors average", "Linear fit"]
        method = ttk.OptionMenu(paramsTab, methodVar, choices[0], *choices)
        method.grid(column=3, row=2, padx=30, pady=30)
        tkUtils.ToolTipBind(methodLabel, methodHelp)

        FWHMFindingParamLabel = ttk.Label(paramsTab, text=FWHMFindingMethodParamTextDefault)
        FWHMFindingParamLabel.grid(column=2, row=3, padx=30, pady=30)
        FWHMFindingMethodParam = ttk.Entry(paramsTab)
        FWHMFindingMethodParam.insert(END, "0.2")
        FWHMFindingMethodParam.grid(column=3, row=3, padx=30, pady=30)
        tkUtils.ToolTipBind(FWHMFindingParamLabel, methodParamsHelp)

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
            if entry.strip() == "":
                entry = "0"
            entryRightType = supposedType(entry)
        except:
            msg = f"Parameter '{paramName}' of value {entry} cannot be interpreted as '{supposedType}'."
        return entryRightType, msg

    def __speckleAnalysis(self, kwargs: dict):
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                self.__speckleReport = speckleStatsReport.SpeckleStatsReport(**kwargs)
                w = {str(warn): warn.message for warn in w}  # Sometimes two warnings from the "same" source
        except Exception as e:
            messagebox.showerror("Oops!", str(e))
            return
        for warn in w:
            messagebox.showwarning("Watch out!", w[warn])

        # TODO : Progress bar to display generation progress?

        self.__speckleImageStatsTab()
        self.__speckleAutocorrelationStatsTab()
        self.__localContrastStatsTab()
        self.__fullReportPreviewButton["state"] = NORMAL
        self.__saveFullReportButton["state"] = NORMAL

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
        # Clear everything and destroy every widget present (prevents as many memory leaks as possible)
        self.__fullReportPreviewButton["state"] = DISABLED
        self.__saveFullReportButton["state"] = DISABLED
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
