__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path, listdir
from pocketLab import __module__
import yaml
import json
from jsonmodel.validators import jsonModel
from importlib.util import find_spec
from re import compile
from pocketLab.clients.localhost_session import localhostSession

class labBot(localhostSession):

    def __init__(self, **event_kwargs):
        localhostSession.__init__(self)

    # discover module path
        self.modPath = find_spec(__module__).submodule_search_locations[0]

    # validate existence of labBot folder in app data (or create)
        self.botFolder = self.sessionData(session_name='labBot Data')
        if not path.exists(self.botFolder):
            from os import makedirs
            makedirs(self.botFolder)

    # construct context model
        event_rules = 'rules/lab-event-model.json'
        event_path = path.join(self.modPath, event_rules)
        self.eventFile = json.loads(open(event_path).read())
        self.eventModel = jsonModel(self.eventFile)

    # ingest & validate context_kwargs
        self.eventDetails = self.eventModel.validate(event_kwargs)

    # construct thread model
        thread_rules = 'rules/lab-thread-model.json'
        thread_path = path.join(self.modPath, thread_rules)
        self.threadFile = json.loads(open(thread_path).read())
        self.threadModel = jsonModel(self.threadFile)

    # ingest & validate current thread
        thread_list = []
        yaml_file = compile('\\.ya?ml$')
        thread_folder = listdir(self.botFolder)
        for file in thread_folder:
             if yaml_file.findall(file):
                thread_list.append(file)
        sorted_list = sorted(thread_list)
        recent_file = sorted_list[-1]

    def save(self, **kwargs):

    # import dependencies
        import yaml
        from datetime import datetime

    # construct metadata
        dT = '%sZ' % datetime.utcnow().isoformat()
        file_name = 'lab-bot-%s.yaml' % dT.replace(':','-').replace('.','-')
        log_path = path.join(self.botFolder, file_name)

    # TODO: incorporate labID into logging system

    # construct log details
        log_details = {
            'dt': dT,
            'op': kwargs
        }

    # save details to log file
        with open(log_path, 'wb') as f:
            f.write(yaml.dump(log_details).encode('utf-8'))
            f.close()

        return self


