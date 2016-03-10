__author__ = 'rcj1492'
__created__ = '2016.03'

'''
    a method to create the docker run script

run_details = {
    'name': 'main',
    'injected_variables': {},
    'mounted_volumes': {},
    'mapped_ports': {},
    'docker_image': 'rc42/flaskServer',
    'image_tag': '',
    'run_command': ''
}
'''

def dockerRun(run_details):

    run_script = 'docker run --name %s' % run_details['name']
    if run_details['injected_variables']:
        for key, value in run_details['injected_variables'].items():
            run_script += ' -e %s=%s' % (key, value)
    if run_details['mounted_volumes']:
        for key, value in run_details['mounted_volumes'].items():
            run_script += ' -v "%s":"%s"' % (key, value)
    run_script += ' -i -d'
    if run_details['mapped_ports']:
        for key, value in run_details['mapped_ports'].items():
            run_script += ' -p %s:%s' % (key, value)
    run_script += ' %s' % run_details['docker_image']
    if run_details['image_tag']:
        run_script += ':%s' % run_details['image_tag']
    if run_details['run_command']:
        run_script += ' %s' % run_details['run_command']

    return run_script