from numpy import arange


class Drawing():

    def __init__(self, ui, fig, model, debug=0):

        self.ui = ui
        self.fig = fig
        self.debug = debug
        self.xsize = model.preferences.xsize
        self.ysize = model.preferences.ysize

        self.ax = self.fig.add_subplot(111)

        self.draw_grid('on')
        self.set_default_view()

    def draw_grid(self, grid):

        if self.debug:
            print('draw grid')

        # Enlarge grid by factor of 2 in each direction.
        # Only xsize by ysize is visible.
        xticks = arange(self.xsize * 2)
        yticks = arange(self.ysize * 2)

        self.ax.axis('equal')
        self.ax.set_xticks(xticks)
        self.ax.set_yticks(yticks)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        if grid == 'on':
            self.ax.grid(color='lightblue')

        self.ax.tick_params(which='both', left=False, bottom=False,
                            top=False, labelbottom=False)

        self.ax.set_axisbelow(True)

    def savefig(self, filename):

        self.fig.savefig(filename, bbox_inches='tight', pad_inches=0)

    def set_view(self, xmin, ymin, xmax, ymax):

        if self.debug:
            print('view', xmin, ymin, xmax, ymax)

        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)

    def set_default_view(self):

        self.set_view(0, 0, self.xsize, self.ysize)

    def clear(self, grid='on'):

        if self.debug:
            print('clear')

        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()

        self.ax.clear()

        self.draw_grid(grid)

        self.set_view(xmin, ymin, xmax, ymax)

    def refresh(self):

        if self.debug:
            print('refresh')
        self.fig.canvas.draw()
