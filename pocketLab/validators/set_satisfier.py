__author__ = 'rcj1492'
__created__ = '2016.03'

# pip install sympy

from sympy import symbols, sympify
from sympy.logic.inference import satisfiable

'''
SAGE MATH
https://github.com/sagemath/sage
http://doc.sagemath.org/html/en/reference/logic/sage/logic/propcalc.html

SYMPY
http://docs.sympy.org/latest/modules/logic.html
https://github.com/sympy/sympy
http://docs.sympy.org/latest/tutorial/basic_operations.html#converting-strings-to-sympy-expressions

ITERTOOLS
https://docs.python.org/3.5/library/itertools.html

x = symbols('x')
y = symbols('y')
string_eq = '1/cos(x) + y'
w = sympify(string_eq)
eval_eq = w.subs([(x, .5),(y, 1)])
print(eval_eq)

a, b, c = symbols('a b c')
e = (a | (b & c) | ~c) ^ ~a
eval_bool = e.subs([(a, bool(test_dict['a'])), (b, bool(test_dict['b'])), (c, bool(test_dict['c']))])
print(to_dnf(e, False))
print(eval_bool)
print([i for i in satisfiable(e, all_models=True)])
'''

class setSatisfier(object):

    def __init__(self, model_dict, expression_string):
        self.dict = model_dict
        self.symbols = {}
        for key, value in model_dict.items():
            self.symbols[key] = symbols(key)
        self.expression = sympify(expression_string)
        self.satisfiable = satisfiable(self.expression, all_models=True)
        if not self.satisfiable:
            raise Exception('Boolean expression cannot be satisfied.')

    def evaluate(self, input_dict):
        sub_list = []
        for key in input_dict.keys():
            symbol = self.symbols[key]
            value = bool(input_dict[key])
            sub_list.append((symbol, value))
        eval_bool = self.expression.subs(sub_list)
        return eval_bool

    def options(self, input_dict):
        sat_options = []
        for i in self.satisfiable:
            change_dict = {}
            for key, value in input_dict.items():
                symbol = self.symbols[key]
                if symbol in i.keys():
                    if bool(input_dict[key]) != i[symbol]:
                        replace = 'remove'
                        if i[symbol]:
                            replace = 'add'
                        change_dict[key] = replace
            if change_dict:
                sat_options.append(change_dict)
        return sat_options







