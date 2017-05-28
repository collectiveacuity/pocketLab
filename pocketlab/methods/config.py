__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

def compile_yaml(config_schema, yaml_path=''):

    '''
        a method to compile a yaml file with top-level comments from a json model
        
    :param config_schema: dictionary with json model schema architecture 
    :param yaml_path: [optional] string with path to user yaml file
    :return: string with yaml formatted text
    '''

# construct config model
    from jsonmodel.validators import jsonModel
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

# construct config text
    config_text = ''
    if 'comments' in config_model.metadata.keys():
        if isinstance(config_model.metadata['comments'], str):
            comment_lines = config_model.metadata['comments'].splitlines()
            for comment in comment_lines:
                config_text += '# %s\n' % comment
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
        config_text += line_text

# update user config
    if yaml_path:
        from os import path
        if not path.exists(yaml_path):
            raise ValueError('%s is not a valid path.')
        import ruamel.yaml
        user_text = open(yaml_path).read()
        user_code = ruamel.yaml.load(user_text, ruamel.yaml.RoundTripLoader)
        user_len = len(user_code.keys())
        count = 0
        for item in config_list:
            if item['key'] not in user_code.keys():
                insert_row = user_len + count
                insert_kwargs = {
                    'pos': insert_row,
                    'key': item['key'],
                    'value': item['value']
                }
                if item['comments']:
                    insert_kwargs['comment'] = item['comments']
                user_code.insert(**insert_kwargs)
                count += 1
        config_text = ruamel.yaml.dump(user_code, Dumper=ruamel.yaml.RoundTripDumper)

    return config_text

def inject_init(init_path, readme_path, setup_kwargs):

    import re
    from os import path
    from copy import deepcopy

# retrieve init text
    init_text = ''
    if not path.exists(init_path):
        raise ValueError('%s is not a valid path' % init_path)
    init_text = open(init_path).read()

# retrieve init settings
    init_kwargs = {
        'version': '',
        'author': '',
        'url': '',
        'description': '',
        'license': '',
    }
    for key in init_kwargs.keys():
        key_regex = re.compile("__%s__\s?\=\s?'(.*?)'" % key)
        key_search = key_regex.findall(init_text)
        if key_search:
            init_kwargs[key] = key_search[0]

# retrieve modifiable settings
    mod_kwargs = {
        'module': '',
        'email': '',
        'entry': '',
        'authors': ''
    }
    for key in mod_kwargs.keys():
        key_regex = re.compile("__%s__\s?\=\s?'(.*?)'" % key)
        key_search = key_regex.findall(init_text)
        if key_search:
            mod_kwargs[key] = key_search[0]
    if mod_kwargs['module']:
        init_kwargs['name'] = mod_kwargs['module']
    if mod_kwargs['entry']:
        init_kwargs['entry_points'] = { "console_scripts": [mod_kwargs['entry']] }
    if mod_kwargs['email']:
        init_kwargs['author_email'] = mod_kwargs['email']
        init_kwargs['maintainer_email'] = mod_kwargs['email']
    if mod_kwargs['authors']:
        del init_kwargs['author']
        init_kwargs['author_list'] = mod_kwargs['authors'].split(' ')

# add readme
    if not path.exists(readme_path):
        raise ValueError('%s is not a valid path' % readme_path)
    try:
        readme_text = open(readme_path).read()
        init_kwargs['long_description'] = str(readme_text)
    except:
        raise ValueError('%s is not a valid text file.' % readme_path)

# merge kwargs
    setup_kwargs.update(**init_kwargs)
    updated_kwargs = deepcopy(setup_kwargs)
    for key, value in updated_kwargs.items():
        if not value:
            del setup_kwargs[key]

    return setup_kwargs

def update_setup(setup_text):

# retrieve setup text comments
    from os import path
    from pocketlab import __module__
    from importlib.util import find_spec
    module_path = find_spec(__module__).submodule_search_locations[0]
    file_path = path.join(module_path, 'models/setup.py.txt')
    file_text = open(file_path).read()

# determine module name and version number
    module_name = 'pocketlab'
    version_number = '0.1'
    import re
    init_regex = re.compile("init_path\s\=\s'(.*?)'")
    init_search = init_regex.findall(setup_text)
    if init_search:
        init_path = init_search[0]
        if path.exists(init_path):
            init_text = open(init_path).read()
            module_regex = re.compile("__module__\s\=\s'(.*?)'")
            version_regex = re.compile("__version__\s\=\s'(.*?)'")
            module_search = module_regex.findall(init_text)
            version_search = version_regex.findall(init_text)
            if module_search and version_search:
                module_name = module_search[0]
                version_number = version_search[0]

# find vcs URIs
    hg_regex = re.compile('(hgrc\s\[paths\]\sdefault\s\=\s)(.*?)\n')
    hg_search = hg_regex.findall(setup_text)
    github_regex = re.compile('(git\sremote\sadd\sorigin\s)(.*?)\n')
    github_search = github_regex.findall(setup_text)

# find/replace comments in setup text
    comment_regex = re.compile("'''\sDOCUMENTATION.*?'''", re.S)
    setup_text = comment_regex.sub('', setup_text)
    setup_text = setup_text.strip()
    setup_text += '\n\n%s' % file_text

# replace module and version
    dist_regex = re.compile("pocketlab-0.1")
    new_dist = '%s-%s' % (module_name, version_number)
    setup_text = dist_regex.sub(new_dist, setup_text)

# replace vcs URIs
    if hg_search:
        hg_text = '%s%s\n' % (hg_search[0][0], hg_search[0][1])
        setup_text = hg_regex.sub(hg_text, setup_text)
    if github_search:
        github_text = '%s%s\n' % (github_search[0][0], github_search[0][1])
        setup_text = github_regex.sub(github_text, setup_text)

    return setup_text

if __name__ == '__main__':
    user_path = '../../tests/lab.yaml'
    standard_path = '../models/lab-config.json'
    from labpack.records.settings import load_settings
    standard_schema = load_settings(standard_path)
    text = compile_yaml(standard_schema, user_path)
    print(text)

    init_path = '../__init__.py'
    readme_path = '../../README.rst'
    setup_kwargs = inject_init(init_path, readme_path, {})
    print(setup_kwargs)

    setup_text = open('../../setup.py').read()
    new_text = update_setup(setup_text)
    print(new_text)