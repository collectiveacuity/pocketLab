__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

def validate_heroku(heroku_model, file_path, service_name=''):
    
    '''
        a method to validate heroku.yaml configuration
        
    :param heroku_model: jsonModel object with heroku config schema
    :param file_path: string with path to heroku.yaml file for service
    :param service_name: [optional] string with name of service
    :return: dictionary with heroku configuration
    '''

# construct message insert
    msg_insert = 'working directory'
    if service_name:
        msg_insert = 'root directory for "%s"' % service_name
    msg_insert_2 = 'cred sub-folder of %s' % msg_insert
    
# validate heroku yaml exists
    from os import path
    if not path.exists(file_path):
        raise ValueError('heroku.yaml does not exist in %s.\nTry: "lab init --heroku" in %s.' % (msg_insert_2, msg_insert))

# validate heroku yaml is valid
    from labpack.records.settings import load_settings
    try:
        heroku_details = load_settings(file_path)
    except:
        raise ValueError('heroku.yaml file in %s corrupted.\nTry deleting and running again in %s: "lab init --heroku"' % (msg_insert_2, msg_insert))

# validate heroku yaml keys
    from jsonmodel.exceptions import InputValidationError
    for key, value in heroku_details.items():
        try:
            object_title = 'Field %s in heroku.yaml in %s' % (key, msg_insert_2)
            heroku_model.validate(value, '.%s' % key, object_title)
        except InputValidationError as err:
            error_msg = "Value None for field .%s failed test 'value_datatype': map" % key
            if err.message.find(error_msg) > -1:
                pass
            else:
                raise
        except:
            raise
    
    return heroku_details

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