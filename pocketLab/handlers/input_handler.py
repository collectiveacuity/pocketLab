__author__ = 'rcj1492'
__created__ = '2016.03'

class inputHandler(object):

    '''
        a class for handling user input events
    '''

    def __init__(self, **kwargs):

    # construct default class methods
        self.labLogging = True
        self.context = {
            'verbose': True,
            'message': '',
            'reaction': '',
            'tprint': None,
            'pprint': None,
            'kwargs': None,
            'exception': None,
            'input_criteria': None,
            'failed_test': '',
            'error_value': '',
            'error_code': 0,
            'operation': '',
            'outcome': 'input',
            'thread': None
        }

    # update class method values from kwargs
        for key, value in kwargs.items():
            if key in self.context.keys():
                self.context[key] = value

    # determine printing and logging toggles from kwargs
        if self.context['kwargs']:
            if 'labLogging' in self.context['kwargs'].keys():
                if not self.context['kwargs']['labLogging']:
                    self.labLogging = False

    # create a log of the event
        if self.labLogging:
            from pocketLab.clients.logging_client import loggingClient
            loggingClient().put(**self.context)

    # format printing
        self.mprint = ''
        self.rprint = ''
        self.tprint = None
        self.pprint = None
        if self.context['message']:
            if isinstance(self.context['message'], str):
                self.mprint = self.context['message']
        if self.context['reaction']:
            if isinstance(self.context['rprint'], str):
                self.rprint = self.context['reaction']
        if self.context['tprint']:
            if isinstance(self.context['tprint'], dict):
                t_keys = self.context['tprint'].keys()
                if not ('headers','rows') in t_keys:
                    if isinstance(self.context['tprint']['headers'], list):
                        if isinstance(self.context['tprint']['rows'], list):
                            if not self.context['tprint']['rows']:
                                self.context['tprint']['rows'] = [{}]
                            if isinstance(self.context['tprint']['rows'][0], dict):
                                from pocketLab.compilers.table_print import tablePrint
                                self.tprint =  tablePrint(self.context['tprint']['headers'], self.context['tprint']['rows'])
        if self.context['pprint']:
            self.pprint = self.context['pprint']

    # print success message
        if self.rprint:
            text = 'Oops! %s' % self.rprint
            print(text)
        if self.tprint:
            print('\n%s' % self.tprint)
        if self.pprint:
            from pprint import pprint
            print('\n')
            pprint(self.pprint)

    def msg(self):
        return self.mprint