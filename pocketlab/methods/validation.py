__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

def validate_platform(platform_model, service_root, service_name=''):
    
    '''
        a method to validate a yaml configuration file in .lab folder
        
    :param platform_model: jsonModel object with config schema
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
    file_flag = platform_model.metadata['flag']
    file_name = platform_model.title
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
    for key, value in platform_model.schema.items():
        object_title = 'Field %s in %s in %s' % (key, file_name, msg_insert_2)
        if key in config_details.keys():
            try:
                platform_model.validate(config_details[key], '.%s' % key, object_title)
            except InputValidationError as err:
                error_msg = "Value None for field .%s failed test 'value_datatype': map" % key
                if err.message.find(error_msg) > -1:
                    pass
                else:
                    raise
            except:
                raise
        elif value:
            missing_msg = '%s is missing' % object_title
            raise ValueError(missing_msg)
    
    return config_details

def validate_compose(compose_model, service_model, file_path, service_name=''):

    '''
        a method to validate docker-compose.yaml configuration for service
        
    :param compose_model: jsonModel object with compose config schema
    :param service_model: jsonModel object with service config schema 
    :param file_path: string with path to docker-compose.yaml file for service
    :param service_name: [optional] string with name of service
    :return: dictionary with lab configurations
    '''

# construct message insert
    msg_insert = 'working directory'
    if service_name:
        msg_insert = 'root directory for "%s"' % service_name
    compose_insert = 'docker-compose.yaml file in %s' % msg_insert

# validate lab yaml exists
    from os import path
    if not path.exists(file_path):
        raise ValueError('docker-compose.yaml does not exist in %s.\nTry: "lab init" in %s.' % (msg_insert, msg_insert))
    
# validate lab yaml is valid
    from labpack.records.settings import load_settings
    try:
        compose_details = load_settings(file_path)
    except:
        raise ValueError('%s corrupted.\nTry deleting and running again: "lab init"' % (compose_insert))

# validate compose schema structure
    from jsonmodel.exceptions import InputValidationError
    from copy import deepcopy
    test_details = deepcopy(compose_details)
    for key, value in compose_model.schema.items():
        object_title = 'Field %s in %s' % (key, compose_insert)
        if key in test_details.keys():
            try:
                # object_title = 'Field %s in docker-compose.yaml in %s' % (key, msg_insert)
                compose_model.validate(test_details[key], '.%s' % key, object_title)
            except InputValidationError as err:
                error_msg = "Value None for field .%s failed test 'value_datatype': map" % key
                if err.message.find(error_msg) > -1:
                    pass
                else:
                    raise
            except:
                raise
        elif value:
            missing_msg = '%s is missing' % object_title
            raise ValueError(missing_msg)

# validate services exists
    if not compose_details['services']:
        raise ValueError('%s is missing services.\nTry deleting and running again: "lab init"' % compose_insert)
    elif service_name and not service_name in compose_details['services'].keys():
        raise ValueError('%s is missing settings for "%s" service.' % (service_name, compose_insert))
    elif not service_name and len(compose_details['services'].keys()) > 1:
        raise ValueError('%s contains more than one service option.\nTry specifying service: "lab start [SERVICE]' % compose_insert)

# validate service schema structure
    for key, value in test_details['services'].items():
        for k, v in service_model.schema.items():
            object_title = 'Field services.%s.%s in %s' % (key, k, compose_insert)
            if k in value.keys():
                try:
                    service_model.validate(value[k], '.%s' % k, object_title)
                except InputValidationError as err:
                    error_msg = "Value None for field .%s failed test 'value_datatype': map" % k
                    if err.message.find(error_msg) > -1:
                        pass
                    else:
                        raise
                except:
                    raise
            elif service_model.components['.%s' % k]['required_field']:
                missing_msg = '%s is missing' % object_title
                raise ValueError(missing_msg)

    return compose_details

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
        raise ValueError('lab.yaml does not exist in %s.\nTry: "lab init" in %s.' % (msg_insert, msg_insert))
    
# validate lab yaml is valid
    from labpack.records.settings import load_settings
    try:
        lab_details = load_settings(file_path)
    except:
        raise ValueError('lab.yaml file in %s corrupted.\nTry deleting and running again: "lab init"' % (msg_insert))

# validate lab yaml keys
    from jsonmodel.exceptions import InputValidationError
    from copy import deepcopy
    test_details = deepcopy(lab_details)
    for key, value in lab_model.schema.items():
        object_title = 'Field %s in lab.yaml in %s' % (key, msg_insert)
        if key in test_details.keys():
            try:
                object_title = 'Field %s in lab.yaml in %s' % (key, msg_insert)
                lab_model.validate(test_details[key], '.%s' % key, object_title)
            except InputValidationError as err:
                error_msg = "Value None for field .%s failed test 'value_datatype': map" % key
                if err.message.find(error_msg) > -1:
                    pass
                else:
                    raise
            except:
                raise
        elif value:
            missing_msg = '%s is missing' % object_title
            raise ValueError(missing_msg)
    
    return lab_details