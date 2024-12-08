class Colour:
    Rbg = '\033[41'
    Gbg = '\033[42'
    Bbg = '\033[44'
    Cbg = '\033[46'
    Mbg = '\033[45'
    Ybg = '\033[43'
    Kbg = '\033[40'
    Rfg = '\033[31'
    Gfg = '\033[32'
    Bfg = '\033[34'
    Cfg = '\033[36'
    Mfg = '\033[35'
    Yfg = '\033[33'
    Kfg = '\033[30'
    RESET = '\033[0m'

class ProgressBar:
    def __init__(self, min, max, width, colourfg, colourbg):
        self.min = min
        self.max = max
        self.width = width
        self.fg = colourfg
        self.bg = colourbg

    def redraw(self, value):
        # print('\033[s' + Colour.RESET + self.fg, end='')
        barlen = int((value-self.min)/(self.max-self.min)*self.width)
        blanklen = self.width - barlen
        print('|' + self.bg + ' '*barlen + Colour.RESET, end='\n')
        # print('\033[u' + Colour.RESET, end='')

if __name__ == '__main__':
    import numpy
    import time
    bar = ProgressBar(0, 1, 30, Colour.Yfg, Colour.Rbg)
    print('')
    for a in numpy.linspace(0, 1, 20):
        bar.redraw(a)
        time.sleep(0.5)
    print('')
        