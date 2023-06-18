global_dict = {}
exec('from lcapy import *', global_dict)


class ExprCalc:

    def __init__(self, expr):

        self.expr = expr

    def attribute(self, name):

        global_dict['result'] = self.expr

        command = '(result).%s' % name
        expr = eval(command, global_dict)
        return expr

    def method(self, name):

        global_dict['result'] = self.expr

        command = '(result).%s()' % name
        expr = eval(command, global_dict)
        return expr
