__author__ = 'rcj1492'
__created__ = '2016.03'

_devtest_details = {
    'description': 'Devtest provides a method to test the range of cli options, arguments and types.',
    'title': 'Devtest',
    'help': 'tests the range of cli options',
    'benefit': 'Devtest documents command-line interface options',
}

def devtest(project_list, verbose=True, all=False):

    input_fields = {
        'project_list': project_list,
        'verbose': verbose,
        'all': all
    }

    return input_fields


