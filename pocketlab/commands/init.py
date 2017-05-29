__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
add .ignore file
add lab.yaml file
add cred & data folders
copy cred files from notes to cred
TODO: python module setup (setup.py, docs folder, <module> folder, __init__)
'''

_init_details = {
    'title': 'Init',
    'description': 'Init adds a number of files to the working directory which are required for other lab processes. If not present, it will create a ```lab.yaml``` file in the root directory to manage various configuration options. It will also create, if missing, ```cred/``` and ```data/``` folders to store sensitive information outside version control along with a ```.gitignore``` (or ```.hgignore```) file to escape out standard non-VCS files.',
    'help': 'creates a lab framework in workdir',
    'benefit': 'Init adds the config files for other lab commands.'
}

from pocketlab.init import fields_model

def init(module_name='', vcs_service=''):

    '''
        a method to add lab framework files to the current directory
    
    :param module_name: [optional] string with name of module to create
    :param vcs_service: [optional] string with name of version control service
    :return: string with success exit message
    '''

    title = 'init'

# validate inputs
    input_fields = {
        'module_name': module_name,
        'vcs_service': vcs_service
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# import dependencies
    from os import path


# setup module architecture
    exit_msg = ''
    if module_name:

    # create vcs ignore files
        import re
        from pocketlab.methods.vcs import load_ignore
        vcs_regex = re.compile('#+\s\sversion\scontrol\s\s#+')
        git_insert = '#############  version control  ################\n.hgignore\n.hg/\ndev/\ntests_dev/'
        hg_insert = '#############  version control  ################\n\\\.git'
        git_path = '.gitignore'
        hg_path = '.hgignore'
        if not path.exists(git_path):
            git_text = load_ignore()
            git_text = vcs_regex.sub(git_insert, git_text)
            with open(git_path, 'wt') as f:
                f.write(git_text)
                f.close()
        if not path.exists(hg_path):
            hg_text = load_ignore(vcs='mercurial')
            hg_text = vcs_regex.sub(hg_insert, hg_text)
            with open(hg_path, 'wt') as f:
                f.write(hg_text)
                f.close()

    # create module file
        if not path.exists(module_name):
            from os import makedirs
            makedirs(module_name)

    # create init file
        init_path = path.join(module_name, '__init__.py')
        if not path.exists(init_path):
            from pocketlab.methods.config import construct_init
            init_text = construct_init(module_name)
            with open(init_path, 'wt') as f:
                f.write(init_text)
                f.close()

    # create other root files


        exit_msg = 'Module framework setup in current directory.'

# setup service architecture
    else:

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
            config_schema = jsonLoader(__module__, 'models/lab-config.json')

        # compile yaml
            from pocketlab.methods.config import compile_yaml
            config_text = compile_yaml(config_schema)

        # save config text
            with open(config_path, 'wt') as f:
                f.write(config_text)
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
    print(config_model.ingest())
