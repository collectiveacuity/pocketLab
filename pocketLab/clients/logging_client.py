__author__ = 'rcj1492'
__created__ = '2016.03'

from os import path, listdir
from re import compile
from jsonmodel.validators import jsonModel
from pocketLab.clients.localhost_session import localhostSession

class loggingClient(localhostSession):

    def __init__(self, client_name=''):
        localhostSession.__init__(self)

    # validate existence of log folder in app data (or create)
        if not client_name:
            client_name = 'Log Data'
        self.logFolder = self.clientData(client_name=client_name)
        if not path.exists(self.logFolder):
            from os import makedirs
            makedirs(self.logFolder)

    # construct supported file type regex patterns
        class _regex_ext(object):
            def __init__(self):
                from re import compile
                self.json = compile('\.json$')
                self.yaml = compile('\.ya?ml$')
                self.jsongz = compile('\.json\.gz$')
                self.yamlgz = compile('\.ya?ml\.gz$')
                self.drep = compile('\.drep$')
                self.types = ['.json','.json.gz','.yaml','.yml','.yaml.gz','.yml.gz','.drep']
                self.names = ['json', 'yaml', 'jsongz', 'yamlgz', 'drep']
        self.ext = _regex_ext()

    # construct field validator model
        class_fields = {
            'schema': {
                'key_string': 'obs-terminal-2016-03-17T17-24-51-687845Z.yaml',
                'body_dict': { 'dT': 1458235492.311154 }
            },
            'components': {
                '.key_string': {
                    'must_not_contain': [ '[^\\w/\\-_\\.]' ]
                },
                '.body_dict': {
                    'extra_fields': True
                },
                '.body_dict.dT': {
                    'required_field': False
                }
            }
        }
        self.valid = jsonModel(class_fields)

    def put(self, key_string, body_dict, override=True):

        __name__ = '%s.put' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)
        _body_arg = '%s(body_dict={...}' % {__name__}

    # validate inputs
    #     file_char = compile('[^\w/\-_\.]')
    #     bad_char = file_char.findall(key_string)
    #     if bad_char:
    #         raise Exception('%s may not contain %s.' % (_key_arg, bad_char))
    #     elif not isinstance(body_dict, dict):
    #         raise Exception('%s must be a dictionary.' % (_body_arg))
        self.valid.string(key_string, '.key_string')
        self.valid.dict(body_dict, self.valid.schema['body_dict'], '.body_dict')

    # construct log file path
        log_path = ''
        log_data = ''.encode('utf-8')
        if self.ext.json.findall(key_string):
            import json
            log_path = path.join(self.logFolder, key_string)
            log_data = json.dumps(body_dict).encode('utf-8')
        elif self.ext.yaml.findall(key_string):
            import yaml
            log_path = path.join(self.logFolder, key_string)
            log_data = yaml.dump(body_dict).encode('utf-8')
        elif self.ext.jsongz.findall(key_string):
            import json
            from gzip import compress
            log_path = path.join(self.logFolder, key_string)
            log_bytes = json.dumps(body_dict).encode('utf-8')
            log_data = compress(log_bytes)
        elif self.ext.yamlgz.findall(key_string):
            import yaml
            from gzip import compress
            log_path = path.join(self.logFolder, key_string)
            log_bytes = yaml.dump(body_dict).encode('utf-8')
            log_data = compress(log_bytes)
        elif self.ext.drep.findall(key_string):
            from pocketLab.compilers import drep
            log_path = path.join(self.logFolder, key_string)
            private_key, log_data, drep_index = drep.dump(body_dict)

        if not log_path:
            raise Exception('%s must end with one of %s file type extensions.' % (_key_arg, self.ext.types))

    # save details to log file
        if not override:
            if path.exists(log_path):
                raise Exception('%s already exists. To overwrite %s, set override=True' % (_key_arg, key_string))
        with open(log_path, 'wb') as f:
            f.write(log_data)
            f.close()

        return self

    def find(self, key_query=None, body_query=None, results=0):

        __name__ = '%s.find' % self.__class__.__name__
        _key_arg = '%s(key_query=[...])' % __name__
        _body_arg = '%s(body_query={...})' % __name__

    # construct regex list for key_query
        if key_query:
            if not isinstance(key_query, list):
                raise Exception('%s must be a list of regex strings.' % key_query)
            elif not key_query:
                raise Exception('%s cannot be empty.' % key_query)

    # construct empty result list and log file list
        parse_list = []
        log_list = listdir(self.logFolder)
        for file in reversed(log_list):
            for extension in self.ext.names:
                regex_pattern = getattr(self.ext, extension)
                if regex_pattern.findall(file):
                    parse_list.append(file)

    # TODO: incorporate key and body queries
        result_list = []
        sorted_list = sorted(parse_list)
        recent_file = sorted_list[-1]

        return recent_file

    def get(self, key_string):

        __name__ = '%s.get' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        file_char = compile('[^\w/\-_\.]')
        bad_char = file_char.findall(key_string)
        if bad_char:
            raise Exception('%s may not contain %s.' % (_key_arg, bad_char))

    # construct path to file
        log_path = path.join(self.logFolder, key_string)

    # validate existence of file
        if not path.exists(log_path):
            raise Exception('%s does not exist.' % _key_arg)

    # retrieve file details
        log_details = {}
        if self.ext.json.findall(key_string):
            import json
            try:
                file_data = open(log_path, 'rt')
                log_details = json.loads(file_data.read())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif self.ext.yaml.findall(key_string):
            import yaml
            try:
                file_data = open(log_path, 'rt')
                log_details = yaml.load(file_data.read())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif self.ext.jsongz.findall(key_string):
            import json
            import gzip
            try:
                file_data = gzip.open(log_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                log_details = json.loads(file_data.read().decode())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif self.ext.yamlgz.findall(key_string):
            import yaml
            import gzip
            try:
                file_data = gzip.open(log_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                log_details = yaml.load(file_data.read().decode())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif self.ext.drep.findall(key_string):
            from pocketLab.compilers import drep
            try:
                file_data = open(log_path)
                log_details = drep.load(private_key='', encrypted_data=file_data)
            except:
                raise Exception('%s is not valid drep data.' % _key_arg)

        if not log_details:
            raise Exception('%s must be one of %s file types.' % (_key_arg, self.ext.types))

        return log_details

    def delete(self, key_string):

        __name__ = '%s.delete' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        file_char = compile('[^\w/\-_\.]')
        bad_char = file_char.findall(key_string)
        if bad_char:
            raise Exception('%s may not contain %s.' % (_key_arg, bad_char))

    # construct path to file
        log_path = path.join(self.logFolder, key_string)

    # validate existence of file
        if not path.exists(log_path):
            return '%s does not exist.' % key_string

        try:
            from os import remove
            remove(log_path)
        except:
            raise Exception('%s failed to delete %s' % (_key_arg, key_string))

        return '%s has been deleted.' % key_string

    def compact(self, total_number=0, cutoff_date=''):

        return True
