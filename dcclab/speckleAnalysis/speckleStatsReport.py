from dcclab.speckleAnalysis import speckleCaracterization
import matplotlib.pyplot as plt
import numpy as np


class SpeckleStatsReport:

    def __init__(self, imagePath: str, gaussianFilterNormalizationStdDev: float = 75, medianFilterSize: int = 3,
                 localContrastKernelSize: int = 7, intensityHistogramBins: int = 256,
                 localContrastHistogramBins: int = 256, FWHMFindingMethod: str = "mean", *FWHMFindingMethodArgs,
                 **FWHMFindingMethodKwargs):
        self.__imagePath = imagePath
        self.__speckleCaracterizationObj = speckleCaracterization.SpeckleCaracerization(imagePath,
                                                                                        gaussianFilterNormalizationStdDev,
                                                                                        medianFilterSize)
        self.verticalFWHM, self.horizontalFWHM = self.__speckleCaracterizationObj.computeFWHMBothAxes(
            FWHMFindingMethod, *FWHMFindingMethodArgs, **FWHMFindingMethodKwargs)
        self.__autocorrelation = self.__speckleCaracterizationObj.fullAutocorrelation
        self.__verticalSlice, self.__horizontalSlice = self.__speckleCaracterizationObj.autocorrelationSlices
        self.__image = self.__speckleCaracterizationObj.speckleImage
        self.__localContrast = self.__speckleCaracterizationObj.localContrast(localContrastKernelSize)
        self.__localContrastHist, self.__localContrastBins = self.__speckleCaracterizationObj.localContrastHistogram(
            localContrastHistogramBins, localContrastKernelSize, False)
        self.__localContrastKernelSize = localContrastKernelSize
        self.__intensityHist, self.__intensityBins = self.__speckleCaracterizationObj.intensityHistogram(
            intensityHistogramBins, False)
        self.isFullyDevelopped = self.__speckleCaracterizationObj.isFullyDevelopedSpecklePattern(intensityHistogramBins)
        self.meanIntensity = self.__speckleCaracterizationObj.meanIntensity()
        self.stdDevIntensity = self.__speckleCaracterizationObj.stdDevIntensity()
        self.medianIntensity = self.__speckleCaracterizationObj.medianIntensity()
        self.maxIntensity = self.__speckleCaracterizationObj.maxIntensity()
        self.minIntensity = self.__speckleCaracterizationObj.minIntensity()
        self.contrastModulation = self.__speckleCaracterizationObj.contrastModulation()
        self.globalContrast = self.__speckleCaracterizationObj.globalContrast()

    @property
    def speckleImage(self):
        return self.__image

    @property
    def fullAutocorrelation(self):
        return self.__autocorrelation

    @property
    def autocorrelationSlices(self):
        return self.__verticalSlice, self.__horizontalSlice

    @property
    def localContrast(self):
        return self.__localContrast

    @classmethod
    def __imageDisplayPrep(cls, axis, image: np.ndarray, title: str, colorMap: str):
        axis.imshow(image, colorMap)
        axis.set_title(title)
        return axis

    @classmethod
    def __plotDisplayPrep(cls, axis, data: np.ndarray, title: str, xlabel: str, ylabel: str = None):
        axis.plot(data)
        axis.set_title(title)
        axis.set_xlabel(xlabel)
        if ylabel is not None:
            axis.set_ylabel(ylabel)
        return axis

    @classmethod
    def __histogramDisplayPrep(cls, axis, data: np.ndarray, title: str, xlabel: str, ylabel: str, bins):
        if data.ndim != 1:
            data = data.ravel()
        axis.hist(data, bins)
        axis.set_title(title)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        return axis

    def __intensityHistogramDisplayPrep(self, axis):
        title = f"Intensity histogram\n({len(self.__intensityBins) - 1} bins, ranging from {self.__intensityBins[0]} to"
        title += f" {self.__intensityBins[-1]})"
        return self.__histogramDisplayPrep(axis, self.__image, title, "Intensity value [-]", "Count [-]",
                                           self.__intensityBins)

    def __localContrastHistogramDisplayPrep(self, axis):
        title = f"Local contrast histogram\n({len(self.__localContrastBins) - 1} bins, ranging"
        title += f" from {np.round(self.__localContrastBins[0], 2)} to {np.round(self.__localContrastBins[-1], 2)})"
        self.__histogramDisplayPrep(axis, self.__localContrast, title, "Local contrast value [-]", "Count [-]",
                                    self.__localContrastBins)

    def __displaySpeckleImagePrep(self, axis, colorMap: str):
        return self.__imageDisplayPrep(axis, self.__image, "Speckle image", colorMap)

    def __displayAutocorrPrep(self, axis, colorMap: str):
        return self.__imageDisplayPrep(axis, self.__autocorrelation, "Full normalized autocorrelation", colorMap)

    def __displayLocalContrastPrep(self, axis, colorMap: str):
        return self.__imageDisplayPrep(axis, self.__localContrast,
                                       f"Local contrast (kernel size of {self.__localContrastKernelSize})", colorMap)

    def displaySpeckleImage(self, colorMap: str = None):
        self.__displaySpeckleImagePrep(plt.subplots()[-1], colorMap)
        plt.show()

    def displayFullAutocorrelation(self, colorMap: str = None, showColorBar: bool = True):
        self.__displayAutocorrPrep(plt.subplots()[-1], colorMap)
        if showColorBar:
            plt.colorbar()
        plt.show()

    def displayAutocorrelationSlices(self):
        fig, (ax1, ax2) = plt.subplots(2, sharey="col")
        fig.suptitle("Autocorrelation slices")

        self.__plotDisplayPrep(ax1, self.__horizontalSlice, "Central horizontal slice",
                               "Horizontal position $x$ [pixel]")

        self.__plotDisplayPrep(ax2, self.__verticalSlice, "Central vertical slice", "Vertical position $y$ [pixel]")

        ylabel = "Normalized autocorrelation coefficient [-]"
        fig.text(0.06, 0.5, ylabel, ha='center', va='center', rotation='vertical')
        plt.subplots_adjust(hspace=0.32)
        plt.show()

    def displayIntensityHistogram(self):
        self.__intensityHistogramDisplayPrep(plt.subplots()[-1])
        plt.show()

    def displayLocalContrastHistogram(self):
        self.__localContrastHistogramDisplayPrep(plt.subplots()[-1])
        plt.show()

    def speckleImageStats(self):
        intenityStats = f"Mean intensity : {self.meanIntensity}\nIntensity std deviation : {self.stdDevIntensity}\n"
        intenityStats += f"Maximum intensity : {self.maxIntensity}\nMinimum intensity : {self.minIntensity}\n"
        intenityStats += f"Global contrast : {self.globalContrast}\nContrast modulation : {self.contrastModulation}\n"
        return intenityStats

    def specklesStats(self):
        speckleStats = f"Vertical diam. : {self.verticalFWHM} pixels\nHorizontal diam. : {self.horizontalFWHM} pixels\n"
        speckleStats += self.__speckleCaracterizationObj.FWHMFindingMethodInfo() + "\n"
        fullyDeveloped = "This is not a fully developed speckle pattern\n"
        fullyDeveloped += "(based on the intensity histogram, its maximum is not at 0, not assuming exponential " \
                          "distribution)\n"
        if self.isFullyDevelopped:
            fullyDeveloped = "This is a fully developed speckle pattern\n"
            fullyDeveloped += "(based on the intensity histogram, its maximum is at 0, assuming exponential " \
                              "distribution)\n"
        speckleStats += fullyDeveloped
        return speckleStats

    def localContrastStats(self):
        localContrastStats = f"Local contrast mean : {np.mean(self.__localContrast)}\n"
        localContrastStats += f"Local contrast std deviation : {np.std(self.__localContrast)}\n"
        localContrastStats += f"Local contrast median : {np.median(self.__localContrast)}\n"
        localContrastStats += f"Local contrast min : {np.min(self.__localContrast)}\n"
        localContrastStats += f"Local contrast max : {np.max(self.__localContrast)}"
        return localContrastStats

    def textReport(self):
        header = "========== Statistical properties of the speckle image ==========\n"
        midSection = "========== Statistical properties of the speckles ==========\n"
        basicStats = self.speckleImageStats()
        speckleStats = self.specklesStats()
        localContrastStats = self.localContrastStats()
        allText = header + basicStats + midSection + speckleStats + localContrastStats
        return allText

    def __str__(self):
        return self.textReport()

    def fullGraphicsReport(self, saveName: str = None):
        fig, axes = plt.subplots(3, 2)
        fig.subplots_adjust(hspace=0.4, wspace=0.1)
        ax1 = axes[0, 0]  # Top left
        ax2 = axes[0, 1]  # Top right
        ax3 = axes[1, 0]  # Bottom left
        ax4 = axes[1, 1]  # Bottom right
        gs = axes[2, 0].get_gridspec()
        for ax in axes[2, 0:]:
            ax.remove()
        axBig = fig.add_subplot(gs[2, 0:])
        fig.suptitle(f"Speckles statistical report of\n{self.__imagePath}")

        self.__displaySpeckleImagePrep(ax1, None)

        self.__displayLocalContrastPrep(ax2, None)

        self.__intensityHistogramDisplayPrep(ax3)

        self.__localContrastHistogramDisplayPrep(ax4)

        text = self.textReport()
        axBig.text(0.5, -0.1, text, ha="center", fontsize=8)
        axBig.axis("off")
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())  # Works only with Tk backend I think... This is only for aesthetic
        fig.set_size_inches((8.5, 11), forward=False)  # For saving purpose
        if saveName is not None:
            plt.savefig(fname=saveName, dpi=1000)
        plt.show()

    def fullMethodInfo(self):
        raise NotImplementedError("To do")


if __name__ == '__main__':
    path = r"..\speckleAnalysis\circularWithPhasesSimulations\4pixelsCircularWithPhasesSimulations.tiff"
    ssr = SpeckleStatsReport(path, averageRange=20 / 100)
    ssr.fullGraphicsReport("test.pdf")
