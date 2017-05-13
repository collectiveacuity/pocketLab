__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

# initialize logging
import logging
logging.basicConfig(level=logging.DEBUG)

# retrieve schemas
from pocketlab import __module__
from jsonmodel.loader import jsonLoader
fields_schema = jsonLoader(__module__, 'models/lab-fields.json')
cli_schema = jsonLoader(__module__, 'models/lab-cli.json')

# construct fields model
from pocketlab.utils import compile_model
fields_model = compile_model(fields_schema, cli_schema)

if __name__ == '__main__':
    print(fields_model.keyMap)