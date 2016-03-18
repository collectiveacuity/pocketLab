__author__ = 'rcj1492'
__created__ = '2016.03'

def dump(data, index=None):

# import dependencies
    import yaml
    from gzip import compress

# construct empty returns
    private_key = ''
    encrypted_data = ''
    drep_index = object()

# placeholder pass thru
    encrypted_data = yaml.dump(data).encode('utf-8')

    return private_key, encrypted_data, drep_index

def load(private_key, encrypted_data):

# import dependencies
    import yaml
    from gzip import decompress

# construct empty returns
    data = object()

# placeholder pass thru
    data = yaml.load(encrypted_data.read())

    return data