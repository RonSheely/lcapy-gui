from numpy import arange


class Drawing():

    def __init__(self, ui, fig, debug=0):

        self.ui = ui
        self.fig = fig
        self.debug = debug
        self.xsize = ui.model.preferences.xsize
        self.ysize = ui.model.preferences.ysize


        # Maximum limits for drawing size.  Only xsize by ysize
        # is visible.
        self.xmin = 0
        self.ymin = 0
        self.xmax = self.xsize * 2
        self.ymax = self.ysize * 2

        import matplotlib.pyplot as mpl
        
        self.enlarge_scale = 2

        self.ax = self.fig.add_subplot(111)

        self.draw_grid('on')
        self.set_default_view()

    def draw_grid(self, grid, color='lightblue'):

        if self.debug:
            print('draw grid')

        scale = self.ui.model.preferences.grid_spacing
        xticks = arange(self.xmax) * scale
        yticks = arange(self.ymax) * scale


        self.ax.axis('equal')
        self.ax.set_xticks(xticks)
        self.ax.set_yticks(yticks)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        self.ax.set_facecolor(self.ui.model.preferences.color("background"))

        if grid == 'on':
            self.ax.grid(color= self.ui.model.preferences.color("grid"))

        self.ax.tick_params(which='both', left=False, bottom=False,
                            top=False, labelbottom=False)

        self.ax.set_axisbelow(True)

    def savefig(self, filename):

        self.fig.savefig(filename, bbox_inches='tight', pad_inches=0)

    def set_view(self, xmin, ymin, xmax, ymax):

        if self.debug:
            print('view', xmin, ymin, xmax, ymax)

        if False:
            # If restrict values while panning then will get a zoom.
            # It is also confusing to the user if they try to pan
            # but nothing happens.  TODO: limit region that grid is visible
            # to indicate that out of bounds.
            if xmin < self.xmin:
                xmin = self.xmin
            if ymin < self.ymin:
                ymin = self.ymin
            if xmax > self.xmax:
                xmax = self.xmax
            if ymax > self.ymax:
                ymax = self.ymax

        self.ax.set_xlim(xmin, xmax, emit=False)
        self.ax.set_ylim(ymin, ymax, emit=False)

    def set_default_view(self):

        self.set_view(0, 0, self.xsize, self.ysize)

    def clear(self, grid='on'):

        if self.debug:
            print('clear')

        # These are the desired limits and may not be the actual limits
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()

        # This removes the callbacks!
        self.ax.clear()

        self.draw_grid(grid)

        # Set the limits
        self.set_view(xmin, ymin, xmax, ymax)

    def refresh(self):

        if self.debug:
            print('refresh')
        self.fig.canvas.draw()
