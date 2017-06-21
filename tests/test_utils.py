__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

from pocketlab.utils import inject_defaults, compile_model, compile_commands, compile_arguments

if __name__ == '__main__':

    from pocketlab import __module__, __order__
    from pocketlab.commands.home import _home_schema as home_schema
    from labpack.records.settings import load_settings
    folder_path = '../pocketlab/commands/'
    cli_schema = load_settings('../pocketlab/models/lab-cli.json')
    default_schema = load_settings('../pocketlab/models/lab-defaults.json')
    home_schema = inject_defaults(home_schema, default_schema)
    home_model = compile_model(home_schema, cli_schema)
    home_model.validate(home_model.schema)
    command_list = compile_commands(folder_path, cli_schema, __module__, __order__)
    assert command_list
    def_args, pos_args, opt_args, exc_args = compile_arguments(home_model)
    assert def_args
    assert pos_args
    assert opt_args
    defaults_injected = False
    for argument in opt_args:
        if argument['args'][0] == '-q':
            defaults_injected = True
    assert defaults_injected