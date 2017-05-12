__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

# construct lab fields model
from pocketlab import __module__
from jsonmodel.loader import jsonLoader
from jsonmodel.validators import jsonModel
fields_schema = jsonLoader(__module__, 'models/lab-fields.json')
fields_model = jsonModel(fields_schema)

# construct cli schema
cli_schema = jsonLoader(__module__, 'models/lab-cli.json')

if __name__ == '__main__':
    print(fields_model.schema)
    print(cli_schema)