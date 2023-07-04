global_dict = {}
exec('from lcapy import *', global_dict)


class ExprCalc:

    def __init__(self, expr):

        self.expr = expr

    def eval(self, command):

        global_dict['result'] = self.expr

        expr = eval('(result)' + command, global_dict)
        return expr

    def attribute(self, name):

        return self.eval('.%s' % name)

    def method(self, name):

        return self.eval('.%s()' % name)
