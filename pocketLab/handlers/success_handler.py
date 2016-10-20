__author__ = 'rcj1492'
__created__ = '2016.03'

class successHandler(object):

    '''
        a class for logging and reporting successful events
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
            'outcome': 'success',
            'thread': None
        }

    # update class method values from kwargs
        for key, value in kwargs.items():
            if key in self.context.keys():
                self.context[key] = value

    # determine printing and logging toggles from kwargs
        if self.context['kwargs']:
            if 'verbose' in self.context['kwargs'].keys():
                if not self.context['kwargs']['verbose']:
                    self.context['verbose'] = False
            if 'labLogging' in self.context['kwargs'].keys():
                if not self.context['kwargs']['labLogging']:
                    self.labLogging = False

    # create a log of the event
        if self.labLogging:
            from pocketlab.clients.logging_client import loggingClient
            loggingClient().put(**self.context)

    # format printing
        if self.context['verbose']:
            self.print = ''
            self.tprint = None
            self.pprint = None
            if self.context['message']:
                if isinstance(self.context['message'], str):
                    self.print = self.context['message']
            if self.context['tprint']:
                if isinstance(self.context['tprint'], dict):
                    t_keys = self.context['tprint'].keys()
                    if not ('headers','rows') in t_keys:
                        if isinstance(self.context['tprint']['headers'], list):
                            if isinstance(self.context['tprint']['rows'], list):
                                if not self.context['tprint']['rows']:
                                    self.context['tprint']['rows'] = [{}]
                                if isinstance(self.context['tprint']['rows'][0], dict):
                                    from pocketlab.compilers.table_print import tablePrint
                                    self.tprint =  tablePrint(self.context['tprint']['headers'], self.context['tprint']['rows'])
            if self.context['pprint']:
                self.pprint = self.context['pprint']

    # print success message
            text = 'Sweet! %s' % self.print
            print(text)
            if self.tprint:
                print('\n%s' % self.tprint)
            if self.pprint:
                from pprint import pprint
                print('\n')
                pprint(self.pprint)