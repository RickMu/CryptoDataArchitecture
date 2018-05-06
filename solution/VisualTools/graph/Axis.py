import pyqtgraph as pg
import time
class CustomDateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        # if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        string = '%H:%M:%S\n %Y-%m-%d'
        label1 = '%b %d -'
        label2 = ' %b %d, %Y'

        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        # self.setLabel(altcoin=label)
        return strns