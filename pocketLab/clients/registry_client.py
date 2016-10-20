__author__ = 'rcj1492'
__created__ = '2016.03'

from pocketlab import __module__
from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
from pocketlab.clients.logging_client import loggingClient

class registryClient(object):

    def __init__(self):

    # initialize registry table
        self.registryTable = loggingClient(client_name='Registry Data')

    # initialize registry model
        self.registryRules = jsonLoader(__module__, 'rules/lab-registry-model.json')
        self.registryModel = jsonModel(self.registryRules)

    def add(self, resource_details, override=True):

    # validate input
        resource_details = self.registryModel.validate(resource_details)

    # construct key name from registry details
        registry_key = '%s-%s.yaml' % (resource_details['resource_name'], resource_details['resource_type'])

    # check for existing file overwrite
        if not override:
            if self.registryTable.query(key_query=[registry_key]):
                exit_message = 'A record already exists for %s. To overwrite, make override=True' % registry_key
                exit_code = 1
                return exit_message, exit_code

    # save details in registry
        self.registryTable.put(key_string=registry_key, body_dict=resource_details)
        exit_message = '%s added to lab registry.' % resource_details['resource_name']
        exit_code = 0

        return exit_message, exit_code

    def list(self, resource_type):

        resource_list = []

    # validate input
        resource_type = self.registryModel.validate(resource_type, '.resource_type')

    # query registry table for resource keys
        key_query = '%s.yaml' % resource_type
        result_list = self.registryTable.query(key_query=[key_query])

    # construct resource list from resource details
        for resource in result_list:
            resource_details = self.registryTable.get(key_string=resource)
            resource_list.append(resource_details)

        return resource_list

    def describe(self, resource_name):

        resource_details = {}

    # validate input
        resource_name = self.registryModel.validate(resource_name, '.resource_name')

    # query registry table for resource key
        key_query = '%s-' % resource_name
        result_list = self.registryTable.query(key_query=[key_query])

    # construct resource details from result list
        if result_list:
            resource_details = self.registryTable.get(key_string=result_list[0])

        return resource_details

    def remove(self, resource_name):

        exit_code = 0

    # validate input
        resource_name = self.registryModel.validate(resource_name, '.resource_name')

    # query registry table for resource key
        key_query = '%s-' % resource_name
        result_list = self.registryTable.query(key_query=[key_query])

    # construct resource details from result list
        if result_list:
            self.registryTable.delete(key_string=result_list[0])
            exit_message = '%s deleted from lab registry.' % resource_name
        else:
            exit_message = '%s does not exist.' % resource_name

        return exit_message, exit_code
