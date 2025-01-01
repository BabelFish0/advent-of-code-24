class Colour:
    Rbg = '\033[41m'
    Gbg = '\033[42m'
    Bbg = '\033[44m'
    Cbg = '\033[46m'
    Mbg = '\033[45m'
    Ybg = '\033[43m'
    Kbg = '\033[40m'
    Rfg = '\033[31m'
    Gfg = '\033[32m'
    Bfg = '\033[34m'
    Cfg = '\033[36m'
    Mfg = '\033[35m'
    Yfg = '\033[33m'
    Kfg = '\033[30m'
    RESET = '\033[0m'

    def RGBbg(self, r, g, b):
        return f'\033[48;2;{r};{g};{b}m'
    
    def RGBfg(self, r, g, b):
        return f'\033[38;2;{r};{g};{b}m'

    def cmapbg(self, current, min=0, max=1, gain=255, set=100, colour='r'):
        mode = {'r':0, 'g':1, 'b':2}
        rgb = [set, set, set]
        rgb[mode[colour]] = int(gain*(current-min)/(max-min))
        # print(rgb, end='')
        return self.RGBbg(rgb[0], rgb[1], rgb[2])
    
    def cmapfg(self, current, min=0, max=1, gain=255, set=100, colour='r'):
        mode = {'r':0, 'g':1, 'b':2}
        rgb = [set, set, set]
        rgb[mode[colour]] = int(gain*(current-min)/(max-min))
        return self.RGBfg(rgb[0], rgb[1], rgb[2])

class Printer:
    def __init__(self):
        self.colours = Colour()
        self.mapping = {}

    def _default(self):
        self.mapping = {-1:self.colours.Kbg, 0:self.colours.Rbg, 1:self.colours.Mbg, 2:self.colours.Bbg, 3:self.colours.Cbg, 4:self.colours.Gbg, 5:self.colours.Ybg}

    def _reset(self):
        print(self.colours.RESET, end='')

    def arrprint(self, array2d, dsp_vals=False, fgmode='r', bgmode='r', width=2):
        import numpy
        max = numpy.max(numpy.array(array2d))
        min = numpy.min(numpy.array(array2d))
        cellwidth = len(str(max))
        self._reset()
        for row in array2d:
            for value in row:
                print(self.colours.cmapbg(value, min, max, colour=bgmode) + self.colours.cmapfg(value, min, max, colour=fgmode) + str(int(value))*dsp_vals + ' '*width*(not dsp_vals) + ' '*dsp_vals*(cellwidth-len(str(value))), end='')
            self._reset()
            print()
    
    def string_arrprint(self, array2d, width=2, dsp_vals=False):
        for row in array2d:
            self.iprint(row, width, dsp_vals=dsp_vals)
            print()

    def iprint(self, values, width=1, dsp_vals=False):
        for value in values:
            print(self.mapping[value] + ' '*width*(not dsp_vals) + str(value)*dsp_vals + Colour.RESET, end='')
    
    def test(self):
        self.clear()
        self.iprint([-1, 0, 1, 2, 3, 4, 5])
        self._reset()
        print()
        for r in range(256):
            print(self.colours.RGBfg(100, r, 100) + self.colours.RGBbg(r, 100, 100) + '━', end='')
        self._reset()
        print()
    
    def clear(self):
        print('\033[2J')

class ProgressBar:
    def __init__(self, min, max, width, colourfg, colourbg):
        self.min = min
        self.max = max
        self.width = width
        self.fg = colourfg
        self.bg = colourbg

    def redraw(self, value):
        barlen = int((value-self.min)/(self.max-self.min)*self.width)
        blanklen = self.width - barlen
        print('\033[2K' + self.fg + '|' + self.bg + '='*barlen, end='')
        # print('\033[u', \033[s end='')# + Colour.RESET, end='')

if __name__ == '__main__':
    import numpy
    # import time
    # bar = ProgressBar(0, 1, 30, Colour.Yfg, Colour.Bbg)
    # print('')
    # for a in numpy.linspace(0, 1, 20):
    #     bar.redraw(a)
    #     time.sleep(0.5)
    # print('')
    p = Printer()
    p._default()
    p.test()
    print()
    A = numpy.array([[1, 2, 3],[3, 2, 1],[5, 7, 10]])
    p.arrprint(A)