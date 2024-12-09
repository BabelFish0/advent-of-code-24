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

class Printer:
    def __init__(self):
        self.colours = Colour
        self.mapping = {}

    def _default(self):
        self.mapping = {-1:self.colours.Kbg, 0:self.colours.Rbg, 1:self.colours.Mbg, 2:self.colours.Bbg, 3:self.colours.Cbg, 4:self.colours.Gbg, 5:self.colours.Ybg}

    def iprint(self, values):
        for value in values:
            print(self.mapping[value] + ' ' + Colour.RESET, end='')
    
    def test(self):
        self.clear()
        self.iprint([-1, 0, 1, 2, 3, 4, 5])
    
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
    # import numpy
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