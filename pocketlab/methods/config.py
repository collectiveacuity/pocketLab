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

if __name__ == '__main__':
    user_path = '../../tests/lab.yaml'
    standard_path = '../models/lab-config.json'
    from labpack.records.settings import load_settings
    standard_schema = load_settings(standard_path)
    text = compile_yaml(standard_schema, user_path)
    print(text)