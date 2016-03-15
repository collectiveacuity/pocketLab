__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketLab import __team__, __module__
from os import path
from pocketLab.clients.localhost_session import localhostSession

class loggingSession(localhostSession):

    def __init__(self):
        localhostSession.__init__(self)

    # validate existence of module local user data folder (or create)
        self.regFolder = self.userData(org_name=__team__, prod_name=__module__)
        if not path.exists(self.regFolder):
            from os import makedirs
            makedirs(self.regFolder)

    # validate existence of log subfolder in user data folder (or create)
        self.logFolder = path.join(self.regFolder,'logs')
        if not path.exists(self.logFolder):
            from os import makedirs
            makedirs(self.logFolder)

    def save(self, **kwargs):

    # import dependencies
        import yaml
        from datetime import datetime

    # construct metadata
        dT = '%sZ' % datetime.utcnow().isoformat()
        file_name = 'lab-log-%s.yaml' % dT.replace(':','-').replace('.','-')
        log_path = path.join(self.logFolder, file_name)

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

    def details(self, log_name):

        log_details = {}

        return log_details

    def delete(self, log_name):

        return True

    def reduce(self, total_number=0, cutoff_date=''):

        return True