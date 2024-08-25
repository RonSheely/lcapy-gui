from tkinter import Canvas, TOP
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .window import Window
from .sketcher import Sketcher


class Previewer(Window):

    def __init__(self, ui):

        super(Previewer, self).__init__(ui, None, '')

        self.ui = ui

        # Remove title bar but this places window in top left corner
        # self.overrideredirect(True)

        canvas = Canvas(self)
        canvas.pack(side=TOP, expand=True)

        fig = Figure(figsize=(1, 1), frameon=False)

        graph = FigureCanvasTkAgg(fig, canvas)
        graph.draw()
        graph.get_tk_widget().pack(fill='both', expand=True)

        ax = fig.add_subplot(111)

        self.sketcher = Sketcher(ax, False)

        self.fig = fig
        self.ax = ax

    def show(self, label, arg):

        # FIXME for other styles
        try:
            sketch = self.ui.sketchlib.lookup(arg.cpt_type, 'american')
        except Exception:
            return

        self.ax.clear()
        self.ax.axis('off')
        self.ax.axis('equal')

        self.sketcher.sketch(sketch, None)

        self.deiconify()
        # self.title(label)

        xmin, xmax, ymin, ymax = sketch.minmax()
        self.ax.set_xlim(xmin, xmax)

        self.fig.canvas.draw()

    def hide(self):

        self.withdraw()
