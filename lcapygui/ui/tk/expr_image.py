from lcapy.system import tmpfilename, LatexRunner, PDFConverter
from PIL import Image, ImageTk


class ExprImage:

    def __init__(self, expr):

        self.expr = expr

    def image(self):

        tex_filename = tmpfilename('.tex')

        # Need amsmath for operatorname
        template = ('\\documentclass[a4paper]{standalone}\n'
                    '\\usepackage{amsmath}\n'
                    '\\begin{document}\n$%s$\n'
                    '\\end{document}\n')
        content = template % self.e.latex()

        open(tex_filename, 'w').write(content)
        pdf_filename = tex_filename.replace('.tex', '.pdf')
        latexrunner = LatexRunner()
        latexrunner.run(tex_filename)

        png_filename = tex_filename.replace('.tex', '.png')
        pdfconverter = PDFConverter()
        pdfconverter.to_png(pdf_filename, png_filename, dpi=300)

        img = ImageTk.PhotoImage(Image.open(png_filename), master=self.master)
        return img
