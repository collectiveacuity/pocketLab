__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path
from pocketLab import __module__
from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from importlib.util import find_spec
from copy import deepcopy
from pocketLab.clients.localhost_client import localhostClient

class labBotClient(localhostClient):

    def __init__(self, **observation_kwargs):
        localhostClient.__init__(self)

    # discover module path
        self.modPath = find_spec(__module__).submodule_search_locations[0]

    # validate existence of labBot folder in app data (or create)
        self.botFolder = self.clientData(client_name='labBot Data')
        if not path.exists(self.botFolder):
            from os import makedirs
            makedirs(self.botFolder)

    # construct observation model
        self.eventFile = jsonLoader(__module__, 'rules/lab-event-model.json')
        self.eventModel = jsonModel(self.eventFile)

    # ingest & validate observation kwargs
        self.obsDetails = self.eventModel.ingest(**observation_kwargs)

    # construct initial log data
        self.logData = deepcopy(self.obsDetails)

    # construct initial information lists
        self.obsHistory = []
        self.expHistory = []
        self.researchList = []

    def recall(self, log_type, most_recent=0, date_range=None):

        if log_type == 'observation':
            observation_list = []
            for observation in observation_list:
                self.obsHistory.append(observation)

        if log_type == 'expression':
            expression_list = []
            for expression in expression_list:
                self.expHistory.append(expression)

        return self

    def retrieve(self, request_parameters, session_credentials=None):

        research_results = []
        for item in research_results:
            self.researchList.append(item)

        return self

    def reflect(self, starting_nodes, depth=0, search_time=0):

        self.knowledgeGraph = object()

        return self

    def request(self):

        '''
            placeholder for input request method
        '''

        return self

    def learn(self):

        '''
            placeholder for spawning separate system thread to update knowledge
        '''

        return self

    def log(self):

    # import dependencies
        from pocketLab.clients.logging_client import loggingClient

    # initialize log client
        self.logClient = loggingClient(client_name='Log Data')

    # construct log key
        from datetime import datetime
        dT = datetime.utcnow().isoformat().replace(':','-').replace('.','-')
        dT = '%sZ' % dT
        event_string = 'lab'
        channel_string = 'bot'
        if 'event' in self.logData.keys():
            if self.logData['event']:
                event_string = self.logData['event']
                if len(event_string) > 3:
                    event_string = event_string[0:3]
        if 'channel' in self.logData.keys():
            if self.logData['channel']:
                channel_string = self.logData['channel']
        log_key = '%s-%s-%s.yaml' % (dT, event_string, channel_string)

    # save current log data
        self.logClient.put(log_key, self.logData)

        return True

    def analyze(self):

    # log incoming observation
        if 'logging' in self.obsDetails.keys():
            if self.obsDetails['logging']:
                self.log()

    # construct placeholder (developer) expression
        self.expDetails = deepcopy(self.obsDetails)
        self.expDetails['event'] = 'expression'

    # add superlative to message
        if self.expDetails['outcome'] == 'success':
            self.expDetails['msg'] = 'Sweet! %s' % self.expDetails['msg']
        elif self.expDetails['outcome'] == 'error':
            self.expDetails['msg'] = 'Err! %s' % self.expDetails['msg']

    # handle request for further input
        elif self.expDetails['outcome'] == 'input':
            if self.expDetails['logging']:
                self.logData = deepcopy(self.expDetails)
                self.log()
            input_text = input(self.expDetails['msg'])
            return input_text

    # conduct unspecified modeling logic

    # request additional information

    # compose expression

    # initiate learning processes

    # log outgoing expression
        if self.expDetails['logging']:
            self.logData = deepcopy(self.expDetails)
            self.log()

        if self.expDetails['verbose']:
            if self.expDetails['msg']:
                print(self.expDetails['msg'])

        return self.expDetails

