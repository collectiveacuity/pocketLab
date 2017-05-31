__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = '©2017 Collective Acuity'

def validate_docker():
    
    '''
        a method to validate docker is installed
    
    :return: True
    '''
    
    from os import devnull
    from subprocess import call
    sys_command = 'docker --help'
    try:
        call(sys_command, stdout=open(devnull, 'wb'))
    except Exception as err:
        raise Exception('"docker" not installed. GoTo: https://www.docker.com')
    
    return True

def validate_virtualbox(virtualbox_name):
    
    '''
        a method to validate that virtualbox is running on Win 7/8 machines
        
    :param virtualbox_name: string with name of virtualbox image 
    :return: boolean indicating whether virtualbox is running
    '''
    
# validate operating system
    from labpack.platforms.localhost import localhostClient
    localhost_client = localhostClient()
    if localhost_client.os.sysname != 'Windows':
        return False
    win_release = float(localhost_client.os.release)
    if win_release >= 10.0:
        return False
    
# validate docker-machine installation
    from os import devnull
    from subprocess import call, check_output        
    sys_command = 'docker-machine --help'
    try:
        call(sys_command, stdout=open(devnull, 'wb'))
    except Exception as err:
        raise Exception('Docker requires docker-machine to run on Win7/8. GoTo: https://www.docker.com')

# validate virtualbox is running
    sys_command = 'docker-machine status %s' % virtualbox_name
    try:
        vbox_status = check_output(sys_command, stderr=open(devnull, 'wb')).decode('utf-8').replace('\n', '')
    except Exception as err:
        if not virtualbox_name:
            raise Exception('Docker requires VirtualBox to run on Win7/8. GoTo: https://www.virtualbox.org')
        elif virtualbox_name == "default":
            raise Exception('Virtualbox "default" not found. Container will not start without a valid virtualbox.')
        else:
            raise Exception('Virtualbox "%s" not found. Try using "default" instead.' % virtualbox_name)
    if 'Stopped' in vbox_status:
        raise Exception('Virtualbox "%s" is stopped. Try first running: docker-machine start %s' % (virtualbox_name, virtualbox_name))
    
    return True

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
    for key, value in lab_details.items():
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