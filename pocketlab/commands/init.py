__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

_init_details = {
    'title': 'Init',
    'description': 'Init adds a number of files to the working directory which are required for other lab processes. If not present, it will create a ```lab.yaml``` file in the root directory to manage various configuration options. It will also create, if missing, ```cred/``` and ```data/``` folders to store sensitive information outside version control along with a ```.gitignore``` (or ```.hgignore```) file to escape out standard non-VCS files.',
    'help': 'creates a lab framework in workdir',
    'benefit': 'Init adds the config files for other lab commands.'
}

from pocketlab.init import fields_model

def init(vcs_service=''):

    '''
        a method to add lab framework files to the current directory
    
    :param vcs_service: [optional] string with name of version control service
    :return: string with success exit message
    '''

    title = 'init'

# validate inputs
    input_fields = {
        'vcs_service': vcs_service
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# import dependencies
    from os import path

# determine version control service
    if not vcs_service:
        vcs_service = '.git'
        if path.exists('.git'):
            if path.isdir('.git'):
                vcs_service = 'git'
        elif path.exists('.hg'):
            if path.isdir('.hg'):
                vcs_service = 'mercurial'
    else:
        vcs_service = vcs_service.lower()

# add a vcs ignore file
    from pocketlab.methods.vcs import load_ignore
    if vcs_service == 'git':
        vcs_path = '.gitignore'
        vcs_type = 'git'
    else:
        vcs_path = '.hgignore'
        vcs_type = 'mercurial'
    if not path.exists(vcs_path):
        file_text = load_ignore(vcs=vcs_type)
        with open(vcs_path, 'wt') as f:
            f.write(file_text)
            f.close()

# add a lab config file
    config_path = 'lab.yaml'
    if not path.exists(config_path):

    # retrieve config model
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        config_schema = jsonLoader(__module__, 'models/lab-config.json')
        config_model = jsonModel(config_schema)

    # construct order dict
        config_list = []
        config_details = config_model.ingest()
        for key, value in config_details.items():
            details = {
                'key': key,
                'value': value,
                'position': 0,
                'comments': ''
            }
            comp_key = '.%s' % key
            if comp_key in config_model.keyMap.keys():
                if 'field_metadata' in config_model.keyMap[comp_key].keys():
                    metadata = config_model.keyMap[comp_key]['field_metadata']
                    if 'position' in metadata.keys():
                        if isinstance(metadata['position'], int):
                            details['position'] = metadata['position']
                    if 'comments' in metadata.keys():
                        if isinstance(metadata['comments'], str):
                            details['comments'] = metadata['comments']
            config_list.append(details)
        config_list.sort(key=lambda k: k['position'])

    # save to file with comments
        with open(config_path, 'wt') as f:
            if 'comments' in config_model.metadata.keys():
                if isinstance(config_model.metadata['comments'], str):
                    comment_lines = config_model.metadata['comments'].splitlines()
                    for comment in comment_lines:
                        comment_text = '# %s\n' % comment
                        f.write(comment_text)
            for item in config_list:
                comment_stub = '\n'
                if item['comments']:
                    comment_stub = ' # %s\n' % item['comments']
                if isinstance(item['value'], dict):
                    line_text = '%s:%s' % (item['key'], comment_stub)
                    for key, value in item['value'].items():
                        line_text += '  %s: %s\n' % (key, value)
                elif isinstance(item['value'], list):
                    line_text = '%s:%s' % (item['key'], comment_stub)
                    for sub_item in item['value']:
                        line_text += '  - %s\n' % sub_item
                else:
                    line_text = '%s: %s%s' % (item['key'], str(item['value']), comment_stub)
                f.write(line_text)
            f.close()

# add a data folder
    data_path = 'data'
    from os import makedirs
    if not path.exists(data_path):
        makedirs(data_path)

# add a credential folder
    cred_path = 'cred'
    notes_path = 'notes'
    if not path.exists(cred_path):
        makedirs(cred_path)
        if path.exists(notes_path):
            if path.isdir(notes_path):
                src_list = []
                dst_list = []
                from os import listdir
                from shutil import copyfile
                for file_name in listdir(notes_path):
                    file_path = path.join(notes_path, file_name)
                    if path.isfile(file_path):
                        if file_name.find('.json') > -1 or file_name.find('.yaml') > -1 or file_name.find('.yml') > -1:
                            src_list.append(file_path)
                            dst_list.append(path.join(cred_path, file_name))
                for i in range(len(src_list)):
                    copyfile(src_list[i], dst_list[i])

    exit_msg = 'Lab framework setup in current directory.'

    return exit_msg

if __name__ == "__main__":

    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    config_path = '../models/lab-config.json'
    config_model = jsonModel(load_settings(config_path))
    print(config_model.ingest(**{}))