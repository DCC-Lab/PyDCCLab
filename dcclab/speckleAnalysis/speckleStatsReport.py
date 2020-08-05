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

    def displaySpeckleImage(self, colorMap: str = None):
        plt.imshow(self.__image, colorMap)
        plt.show()

    def displayFullAutocorrelation(self, colorMap: str = None, showColorBar: bool = True):
        plt.imshow(self.__autocorrelation, colorMap)
        if showColorBar:
            plt.colorbar()
        plt.show()

    def displayAutocorrelationSlices(self):
        fig, (ax1, ax2) = plt.subplots(2, sharey="col")
        fig.suptitle("Autocorrelation slices")

        ax1.plot(self.__horizontalSlice)
        ax1.set_title(f"Central horizontal slice")
        ax1.set_xlabel("Horizontal position $x$ [pixel]")

        ax2.plot(self.__verticalSlice)
        ax2.set_title(f"Central vertical slice")
        ax2.set_xlabel("Vertical position $y$ [pixel]")

        ylabel = "Normalized autocorrelation coefficient [-]"
        fig.text(0.06, 0.5, ylabel, ha='center', va='center', rotation='vertical')
        plt.subplots_adjust(hspace=0.32)
        plt.show()

    def displayIntensityHistogram(self):
        plt.hist(self.__image.ravel(), self.__intensityBins)
        plt.show()

    def displayLocalContrastHistogram(self):
        plt.hist(self.__localContrast.ravel(), self.__localContrastBins)
        plt.show()

    def textReport(self, split: bool = False):
        header = "========== Statistical properties of the speckle image ==========\n"
        basicStats = f"Mean intensity : {self.meanIntensity}\nIntensity std deviation : {self.stdDevIntensity}\n"
        basicStats += f"Maximum intensity : {self.maxIntensity}\nMinimum intensity : {self.minIntensity}\n"
        basicStats += f"Global contrast : {self.globalContrast}\nContrast modulation : {self.contrastModulation}\n"
        midSection = "========== Statistical properties of the speckles ==========\n"
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
        localContrastStats = f"Local contrast mean : {np.mean(self.__localContrast)}\n"
        localContrastStats += f"Local contrast std deviation : {np.std(self.__localContrast)}\n"
        localContrastStats += f"Local contrast median : {np.median(self.__localContrast)}\n"
        localContrastStats += f"Local contrast min : {np.min(self.__localContrast)}\n"
        localContrastStats += f"Local contrast max : {np.max(self.__localContrast)}"
        if split:
            allText = (header + basicStats, midSection + speckleStats + localContrastStats)
        else:
            allText = header + basicStats + midSection + speckleStats + localContrastStats
        return allText

    def __str__(self):
        return self.textReport()

    def speckleStatsReport(self, saveName: str = None):
        fig, axes = plt.subplots(3, 2)
        fig.subplots_adjust(hspace=0.4)
        ax1 = axes[0, 0]  # Top left
        ax2 = axes[0, 1]  # Top right
        ax3 = axes[1, 0]  # Bottom left
        ax4 = axes[1, 1]  # Bottom right
        ##### Text info #####
        gs = axes[2, 0].get_gridspec()
        for ax in axes[2, 0:]:
            ax.remove()
        axBig = fig.add_subplot(gs[2, 0:])
        fig.suptitle(f"Speckles statistical report of\n{self.__imagePath}")

        ax1.imshow(self.__image)
        ax1.set_title("Speckle image")

        ax2.imshow(self.__localContrast)
        ax2.set_title(f"Local contrast (kernel size of {self.__localContrastKernelSize})")

        ax3.hist(self.__image.ravel(), self.__intensityBins)
        title = f"Intensity histogram\n({len(self.__intensityBins) - 1} bins, ranging from {self.__intensityBins[0]} to "
        title += f"{self.__intensityBins[-1]})"
        ax3.set_title(title)
        ax3.set_xlabel("Intensity value [-]")
        ax3.set_ylabel("Count [-]")

        ax4.hist(self.__localContrast.ravel(), self.__localContrastBins)
        title = f"Local contrast histogram\n({len(self.__localContrastBins) - 1} bins, ranging"
        title += f" from {np.round(self.__localContrastBins[0], 2)} to {np.round(self.__localContrastBins[-1], 2)})"
        ax4.set_title(title)
        ax4.set_xlabel("Local contrast value [-]")
        ax4.set_ylabel("Count [-]")

        text = self.textReport(False)
        axBig.text(0.5, -0.1, text, ha="center", fontsize=8)
        axBig.axis("off")
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())  # Works only with Tk backend I think... This is only for aesthetic
        fig.set_size_inches((8.5, 11), forward=False)
        if saveName is not None:
            plt.savefig(fname=saveName, dpi=1000)
        plt.show()

    def fullMethodInfo(self):
        raise NotImplementedError("To do")


if __name__ == '__main__':
    path = r"..\speckleAnalysis\circularWithPhasesSimulations\4pixelsCircularWithPhasesSimulations.tiff"
    ssr = SpeckleStatsReport(path, averageRange=20 / 100)
    ssr.speckleStatsReport("test.pdf")
