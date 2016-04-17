__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab.validators.set_satisfier import setSatisfier

class testValidatorSetSatisfier(setSatisfier):

    def __init__(self, model_dict, expression_string):
        setSatisfier.__init__(self, model_dict, expression_string)

    def unitTests(self):

        self.evaluate(test_dict)
        print(self.options(test_dict))

        return self

if __name__ == '__main__':
    test_dict = {
        'a': 'string', 'b': 1, 'c': [1], 'd': 1.1, 'e': '', 'f': 0, 'g': [], 'h': 0.0
    }
    exp_string = 'Xor((a | (b & c) | ~c),a)'
    testValidatorSetSatisfier(test_dict, exp_string).unitTests()