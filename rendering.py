"""
Created on Wed Sep 25 16:39:22 2024

Script that defines the rendering class used for real-time rendering using MatPlotLib.

brutal_blondie : Altered from LukeBatteas/EncoderTestBench github for dual axis live plot

@author: LukeBatteas and brutal_blondie
"""
#----------------------------------------------------------
# IMPORTS
#----------------------------------------------------------
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

#----------------------------------------------------------
# CLASS DEFINITION
# https://matplotlib.org/stable/users/explain/animations/blitting.html
#----------------------------------------------------------
class PointsInSpace:
    def __init__(
        self,
        title=None,
        title2=None,
        xlabel=None,
        xlabel2 = None,
        ylabel=None,
        ylabel2=None,
        xlim=None,
        ylim=None,
        ylim2=None,
        hide_axis=False,
        tight=False,
        enable_grid=False,
        enable_legend=False,
    ):
        matplotlib.rcParams["toolbar"] = "None"
        
        # original
        #self.fig = plt.figure()
        #self.ax = self.fig.add_subplot()
        
        # attempt at multiplot (it works!)
        self.fig = plt.figure(221)
        self.ax = self.fig.add_subplot(2,2,1)
        self.ax2 = self.fig.add_subplot(2,2,2)

        # if xlim is None:
        if ylim is None:
            ylim = xlim
        if ylim2 is None:
            ylim2 = xlim
        
        self.ax.set_ylim(ylim)
        self.ax.set_xlim(xlim)
        self.ax2.set_ylim(ylim2)
        self.ax2.set_xlim(xlim)
        #self.ax.autoscale_view()
        #self.ax.set_aspect("equal", adjustable="box")

        # plot appearances
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.ticklabel_format(axis ='y', style = 'sci', scilimits=(0,0))
        
        self.ax2.set_title(title2)
        self.ax2.set_xlabel(xlabel2)
        self.ax2.set_ylabel(ylabel2)
        self.ax2.ticklabel_format(axis ='y', style = 'sci', scilimits=(0,0))

        if hide_axis:
            self.ax.set_axis_off()
            
        # From https://stackoverflow.com/a/47893499
        # This also lowers performance for some reason
        # if tight:
        #     self.fig.tight_layout(pad=0)
        #     w, h = self.fig.get_size_inches()
        #     x1, x2 = self.ax.get_xlim()
        #     y1, y2 = self.ax.get_ylim()
        #     self.fig.set_size_inches(
        #         2 * 1.08 * w, 2 * self.ax.get_aspect() * (y2 - y1) / (x2 - x1) * w
        #     )
            
        if enable_grid:
            self.ax.grid()
            
        self.enable_legend = enable_legend

        self.plot_dict = {}

        plt.show(block=False)
        plt.pause(0.1)
        self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        
    def register_plot(self, label, m="o", alpha=1):
        (points,) = self.ax.plot([], [], m, alpha=alpha, animated=True, label=label)
        self.plot_dict[label] = points
        
    def register_plot2(self, label, m="o", alpha=1):
        (points,) = self.ax2.plot([], [], m, alpha=alpha, animated=True, label=label)
        self.plot_dict[label] = points

    def start_drawing(self):
        self.fig.canvas.restore_region(self.bg)

    def draw_points(self, label, x, y):
        self.ax.set_xlim([min(x)-0.1, max(x)+0.1])
        # self.ax.set_xlim([np.amin(x)-1, np.max(x)+1])
        if label not in self.plot_dict:
            raise ValueError(f"Plot {label} not registered")
        self.plot_dict[label].set_data(x, y)
        self.ax.draw_artist(self.plot_dict[label])
        
    def draw_points2(self, label, x, y):
        self.ax2.set_xlim([min(x)-0.1, max(x)+0.1])
        # self.ax.set_xlim([np.amin(x)-1, np.max(x)+1])
        if label not in self.plot_dict:
            raise ValueError(f"Plot {label} not registered")
        self.plot_dict[label].set_data(x, y)
        self.ax2.draw_artist(self.plot_dict[label])
        
    def end_drawing(self, delay=0):
        if self.enable_legend:
            self.ax.draw_artist(self.ax.legend())
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()
        
    def end_drawing2(self, delay=0):
        if self.enable_legend:
            self.ax2.draw_artist(self.ax2.legend())
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()

        if delay > 0:
            plt.pause(delay)
            
#----------------------------------------------------------
# TEST BLOCK
#----------------------------------------------------------
if __name__ == "__main__":
    pp = PointsInSpace("Dots circling", enable_legend=True)
    pp.register_plot("dots")
    pp.register_plot2("lines", m="-")
    frame_count = 50000
    num_dots = 15
    speed = 0.005

    tic = time.time()
    for i in range(frame_count):
        t = (2 * np.pi / num_dots) * np.arange(num_dots)
        t += i * speed

        x = np.cos(t) * np.cos(4 * t)
        y = np.sin(t) * np.cos(4 * t)

        pp.start_drawing()
        pp.draw_points("dots", x, y)
        pp.draw_points2("lines", x, y)
        pp.end_drawing()
        pp.end_drawing2()

    print(f"Average FPS: {frame_count / (time.time() - tic)}")
