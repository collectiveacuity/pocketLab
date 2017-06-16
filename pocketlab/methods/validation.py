__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

def validate_config(config_model, service_root, service_name=''):
    
    '''
        a method to validate yaml configuration file in .lab folder
        
    :param config_model: jsonModel object with config schema
    :param service_root: string with path to root of service
    :param service_name: [optional] string with name of service
    :return: dictionary with file configurations
    '''

# construct message insert
    msg_insert = 'working directory'
    if service_name:
        msg_insert = 'root directory for "%s"' % service_name
    msg_insert_2 = '.lab sub-folder of %s' % msg_insert

# validate config file exists
    from os import path
    file_flag = config_model.metadata['flag']
    file_name = config_model.title
    file_path = path.join(service_root, '.lab/%s' % file_name)
    file_init = 'lab init %s' % file_flag
    if not path.exists(file_path):
        raise ValueError('%s does not exist in %s.\nTry: "%s" in %s.' % (file_name, msg_insert_2, file_init, msg_insert))

# validate yaml file is valid
    from labpack.records.settings import load_settings
    try:
        config_details = load_settings(file_path)
    except:
        raise ValueError('%s file in %s corrupted.\nTry deleting and running again in %s: "%s"' % (file_name, msg_insert_2, msg_insert, file_init))

# validate heroku yaml keys
    from jsonmodel.exceptions import InputValidationError
    for key, value in config_details.items():
        try:
            object_title = 'Field %s in %s in %s' % (key, file_name, msg_insert_2)
            config_model.validate(value, '.%s' % key, object_title)
        except InputValidationError as err:
            error_msg = "Value None for field .%s failed test 'value_datatype': map" % key
            if err.message.find(error_msg) > -1:
                pass
            else:
                raise
        except:
            raise
    
    return config_details

def validate_lab(lab_model, file_path, service_name=''):
    
    '''
        a method to validate lab.yaml configuration for service
        
    :param lab_model: jsonModel object with lab config schema 
    :param file_path: string with path to lab.yaml file for service
    :param service_name: [optional] string with name of service
    :return: dictionary with lab configurations
    '''

# construct message insert
    msg_insert = 'working directory'
    if service_name:
        msg_insert = 'root directory for "%s"' % service_name

# validate lab yaml exists
    from os import path
    if not path.exists(file_path):
        raise ValueError('lab.yaml does not exist in %s. Try: "lab init" in %s.' % (msg_insert, msg_insert))
    
# validate lab yaml is valid
    from labpack.records.settings import load_settings
    try:
        lab_details = load_settings(file_path)
    except:
        raise ValueError('lab.yaml file in %s corrupted. Try deleting and running again: "lab init"' % (msg_insert))

# validate lab yaml keys
    from jsonmodel.exceptions import InputValidationError
    from copy import deepcopy
    test_details = deepcopy(lab_details)
    for key, value in test_details.items():
        try:
            object_title = 'Field %s in lab.yaml in %s' % (key, msg_insert)
            lab_model.validate(value, '.%s' % key, object_title)
        except InputValidationError as err:
            error_msg = "Value None for field .%s failed test 'value_datatype': map" % key
            if err.message.find(error_msg) > -1:
                pass
            else:
                raise
        except:
            raise
    
    return lab_details