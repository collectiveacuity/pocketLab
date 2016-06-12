__author__ = 'rcj1492'
__created__ = '2016.06'
__license__ = 'MIT'

from copy import deepcopy
from importlib.util import find_spec
from pocketLab import __module__
from labpack.records import labID
from jsonmodel.validators import jsonModel, jsonLoader
from pocketLab.clients.localhost_client import localhostClient

class botClient(localhostClient):

    def __init__(self, action_models=None, log_client=None, knowledge_client=None):
        localhostClient.__init__(self)

    # discover module path
        self.modPath = find_spec(__module__).submodule_search_locations[0]

    # construct event model
        self.eventFile = jsonLoader(__module__, 'rules/bot-event-model.json')
        self.eventModel = jsonModel(self.eventFile)

    # construct action models
        self.actionModels = None
        if action_models:
            self.actionModels = action_models

    # initialize log client
        self.logClient = None
        if log_client:
            self.logClient = log_client

    # initialize knowledge client
        self.knowledgeClient = None
        if knowledge_client:
            self.knowledgeClient = knowledge_client

    # construct empty methods
        self.obsDetails = None
        self.expDetails = None

    def log(self, body_dict):

    # construct log key
        record_id = labID()
        dT = record_id.iso.replace(':', '-').replace('.', '-')
        event_string = 'lab'
        interface_string = 'bot'
        if 'event' in body_dict.keys():
            if body_dict['event']:
                event_string = body_dict['event']
                if len(event_string) > 3:
                    event_string = event_string[0:3]
        if 'interface_id' in body_dict.keys():
            if body_dict['interface_id']:
                interface_string = body_dict['interface_id']
        log_key = '%s-%s-%s.yaml' % (dT, event_string, interface_string)

    # save log data
        self.logClient.put(log_key, body_dict)

        return True

    def analyze(self, **observation_kwargs):

    # ingest observation details
        self.obsDetails = self.eventModel.ingest(**observation_kwargs)

    # log observation
        if self.logClient:
            self.log(self.obsDetails)

    # construct empty expression dictionary
        self.expDetails = {
            'dt': 0.0,
            'event': 'expression',
            'event_details': {
                'actions': []
            },
            'record_id': '',
            'interface_id': '',
            'interface_details': {}
        }

    # determine action from observation details
        if self.actionModels:
            action_name = ''
            action_statement = ''
            event_dict = self.obsDetails['event_details']['json']
            interface_context = event_dict['context']
            interface_details = event_dict['details']
            if 'string' in interface_details.keys():
                if interface_details['string'] in self.actionModels.map.keys():
                    action_name = self.actionModels.map[interface_details['string']]
                    action_statement = interface_details['string']
            action_args = deepcopy(self.actionModels.actions[action_name]['model'].metadata['kwargs'])
            if 'protocols' in action_statement:
                action_args['file'] = action_args['file'].replace('mission','protocols')

    # construct action list for expression
            action_list = []
            if action_name in self.actionModels.actions.keys():
                action_model = self.actionModels.actions[action_name]['model']
                action_list, status_code = self.actionModels.actions[action_name]['method'](action_model, **action_args)
            for action in action_list:
                self.expDetails['event_details']['actions'].append(action)

    # add timestamp to expression details
        record_id = labID()
        self.expDetails['dt'] = record_id.epoch
        self.expDetails['record_id'] = record_id.id48
        self.expDetails['interface_id'] = ''
        self.expDetails['interface_details'] = {
            'channel': self.obsDetails['interface_details']['channel']
        }

    # log expression
        if self.logClient:
            self.log(self.expDetails)

        return self.expDetails

if __name__ == '__main__':
    botClient()