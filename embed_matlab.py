import wx
import wx.lib.mixins.inspection as wit
import wx.aui as aui

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Plot(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2, 2))
        ax=self.figure.add_subplot(111, projection='3d')

        n=100
        for c, m, zlow, zhigh in [('r', 'o', 0, 100), ('b', '^', 0, 50)]:
            xs = self.randrange(n, 0, 100)
            ys = self.randrange(n, 0, 100)
            zs = self.randrange(n, zlow, zhigh)
            ax.scatter(xs, ys, zs, c=c, marker=m)

        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # axes=self.figure.gca()
        # axes.plot([1,2,3,0], [2,1,4,0])


    def randrange(self, n, vmin, vmax):    return (vmax - vmin)*np.random.rand(n) + vmin




class PlotNotebook(wx.Panel):
    def __init__(self, parent, id=-1):
        wx.Panel.__init__(self, parent, id=id)
        self.nb = aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def add(self, name="plot"):
        page = Plot(self.nb)
        self.nb.AddPage(page, name)
        return page.figure


def demo():
    # alternatively you could use
    #app = wx.App()
    # InspectableApp is a great debug tool, see:
    # http://wiki.wxpython.org/Widget%20Inspection%20Tool
    app = wit.InspectableApp()
    frame = wx.Frame(None, -1, 'Plotter')
    plotter = Plot(frame)
    # plotter = PlotNotebook(frame)
    # axes1 = plotter.add('figure 1').gca()
    # axes1.plot([1, 2, 3], [2, 1, 4])
    # axes2 = plotter.add('figure 2').gca()
    # axes2.plot([1, 2, 3, 4, 5], [2, 1, 4, 2, 3])
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    demo()