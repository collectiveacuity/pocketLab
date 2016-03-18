__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path
from pocketLab import __module__
import json
from jsonmodel.validators import jsonModel
from importlib.util import find_spec
from copy import deepcopy
from pocketLab.clients.localhost_client import localhostClient

class labBot(localhostClient):

    def __init__(self, **observation_kwargs):
        localhostClient.__init__(self)

    # discover module path
        self.modPath = find_spec(__module__).submodule_search_locations[0]

    # validate existence of labBot folder in app data (or create)
        self.botFolder = self.clientData(client_name='labBot Data')
        if not path.exists(self.botFolder):
            from os import makedirs
            makedirs(self.botFolder)

    # construct context model
        observation_rules = 'rules/lab-observation-model.json'
        observation_path = path.join(self.modPath, observation_rules)
        self.observationFile = json.loads(open(observation_path).read())
        self.observationModel = jsonModel(self.observationFile)

    # ingest & validate context_kwargs
        self.observationDetails = self.observationModel.validate(observation_kwargs)

    # construct initial log data
        self.logData = deepcopy(self.observationDetails)

    # construct initial information
        self.observationHistory = []
        self.expressionHistory = []
        self.researchList = []

    def recall(self, log_type, most_recent=0, date_range=None):

        if log_type == 'observation':
            observation_list = []
            for observation in observation_list:
                self.observationHistory.append(observation)

        if log_type == 'expression':
            expression_list = []
            for expression in expression_list:
                self.expressionHistory.append(expression)

        return self

    def retrieve(self, request_parameters, session_credentials=None):

        research_list = []
        for item in research_list:
            self.researchList.append(item)

        return self

    def reflect(self, starting_nodes, depth=0, search_time=0):

        self.knowledgeGraph = object()

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
        log_key = ''
        log_key += event_string
        log_key += '-%s' % channel_string
        log_key += '-%s' % dT
        log_key += '.yaml'

    # save current log data
        self.logClient.put(log_key, self.logData)

        return True

    def analyze(self):

        if 'logging' in self.observationDetails.keys():
            if self.observationDetails['logging']:
                self.log()

        from time import time

        self.expressionDetails = {
            'event': 'expression',
            'channel': 'terminal',
            'dT': time(),
            'recipients': 'user',
            'msg': '',
            'media': '',
            'tprint': {},
            'pprint': {},
            'metadata': {}
        }
        if 'msg' in self.observationDetails.keys():
            self.expressionDetails['msg'] = self.observationDetails['msg']

        if 'logging' in self.observationDetails.keys():
            if self.observationDetails['logging']:
                self.logData = deepcopy(self.expressionDetails)
                self.log()

        return self.expressionDetails

