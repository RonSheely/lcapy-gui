from .lateximage import LatexImage


class ExprImage:

    def __init__(self, expr):

        self.expr = expr

    def image(self):

        return LatexImage(self.expr.latex()).image()
