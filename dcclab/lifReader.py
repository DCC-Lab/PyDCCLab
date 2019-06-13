from read_lif.read_lif import Reader, Serie
import numpy as np
import sys


class LifReader(Reader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getSeries(self):
        if not hasattr(self, '__series'):
            self.__series = [
                LifSerie(s.root, self.f, self.offsets[i]) for i, s in enumerate(self.getSeriesHeaders())
            ]
        return self.__series


class LifSerie(Serie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getStack(self, channels=None):
        if channels is None:
            channels = self.getChannels()
        elif type(channels) is not list:
            channels = [channels]

        channelStacks = []
        for channel in channels:
            channelStacks.append(self.__getStackChannel(channel))

        if len(channelStacks) == 1:
            return channelStacks[0]
        else:
            return np.stack(channelStacks)

    def __getStackChannel(self, channel=0, T=0, dtype=np.uint8):
        """ Renamed custom version of getFrame """
        zcyx = []
        zSize = self.getBoxShape()[-1]
        for z in range(zSize):
            progressBar(z, zSize-1)
            cyx = []
            self.f.seek(self.getOffset(**dict({'T': T, 'Z': z})) + self.getChannelOffset(channel))
            yx = np.fromfile(self.f, dtype=dtype, count=int(self.getNbPixelsPerSlice()))
            yx = yx.reshape(self.get2DShape())
            cyx.append(yx)
            zcyx.append(cyx)
        zcyx = np.array(zcyx)
        xzcy = np.moveaxis(zcyx, -1, 0)
        xyzc = np.moveaxis(xzcy, -1, 1)
        return xyzc[:, :, :, 0]


def progressBar(value, endvalue, bar_length=20):

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\r   [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()
