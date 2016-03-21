__author__ = 'rcj1492'
__created__ = '2016.03'

from copy import deepcopy
from pocketLab.clients.registry_client import registryClient

class testClientsRegistryClient(registryClient):

    def __init__(self):
        registryClient.__init__(self)

    def unitTests(self):

    # initialize variables for testing
        from time import time
        registry_file = deepcopy(self.registryRules)
        epoch_time = str(time()).replace('.','')
        resource_name = 'unittest%s' % epoch_time

    # test add
        resource_details = deepcopy(registry_file['schema'])
        resource_details['resource_name'] = resource_name
        resource_details['resource_type'] = 'unittest'
        exit_message, exit_code = self.add(resource_details)
        assert not exit_code

    # test add overwrite
        exit_message, exit_code = self.add(resource_details)
        assert not exit_code

    # test add overwrite error
        exit_message, exit_code = self.add(resource_details, override=False)
        assert exit_code

    # test list for each resource type
        for resource in self.registryModel.keyMap['.resource_type']['discrete_values']:
            resource_list = self.list(resource_type=resource)
            if resource == 'unittest':
                assert resource_list

    # test describe
        resource_details = self.describe(resource_name)
        assert resource_details

    # test describe non-existence
        not_a_name = 'not-%s' % deepcopy(resource_name)
        resource_details = self.describe(not_a_name)
        assert not resource_details

    # test remove
        exit_message, exit_code = self.remove(resource_name)
        assert not exit_code
        assert exit_message.find('deleted from lab registry')

    # test remove non-existence
        exit_message, exit_code = self.remove(resource_name)
        assert not exit_code
        assert exit_message.find('does not exist')

        return self

if __name__ == '__main__':
    testClientsRegistryClient().unitTests()