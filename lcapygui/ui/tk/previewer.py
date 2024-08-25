from .window import Window


class Previewer(Window):

    def __init__(self, ui):

        super(Previewer, self).__init__(ui, None, '')

    def show(self, label):
        self.deiconify()
        self.title(label)

    def hide(self):
        self.withdraw()
