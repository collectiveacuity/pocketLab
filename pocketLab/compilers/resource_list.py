__author__ = 'rcj1492'
__created__ = '2016.03'

def resourceList(resource_list):

# construct header and resource list
        header_list = [ 'NAME', 'HOME', 'REMOTE' ]
        resource_list = []

    # populate resource list with details from registry
        for i in range(len(reg_details['resource_list'])):
            if resource_type == reg_details['resource_list'][i]['resource_type']:
                resource_details = {
                    'NAME': reg_details['resource_list'][i]['project_name'],
                    'HOME': reg_details['resource_list'][i]['project_home'],
                    'REMOTE': reg_details['resource_list'][i]['project_remote']
                }
                if reg_details['default_resource'] == i:
                    resource_details['NAME'] += ' (default)'
                resource_list.append(resource_details)

    # alphabetize the list and return results
        resource_list = sorted(resource_list, key=lambda k: k['NAME'])

        return header_list, resource_list