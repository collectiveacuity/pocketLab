__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

def command_output(shell_command):

    if isinstance(shell_command, str):
        argument_list = shell_command.split(' ')
    elif isinstance(shell_command, list):
        argument_list = shell_command
    else:
        raise ValueError('shell_command argument must be a list of arguments or string.')

    import subprocess
    command_kwargs = {
        'args': argument_list,
        'stderr': subprocess.PIPE,
        'stdout': subprocess.PIPE
    }
    command_output = subprocess.Popen(**command_kwargs)

    std_out = command_output.stdout.read().decode()
    std_err = command_output.stderr.read().decode()

    if std_err:
        raise Exception(std_err)

    return std_out

def generate_commands(docs_path, template_path, commands_folder, fields_model, module_name, preferred_order, verbose=True):

    import re
    from os import path, makedirs
    from pocketlab.utils import compile_commands

    title = 'generate_commands'

# define regex
    usage_regex = re.compile('(usage:\s.*?)[\r|\n]{2}', re.S)
    markdown_regex = re.compile('(\[\[.*?\]\])')

# retrieve list of commands
    if verbose:
        print('Compiling markdown for commands', end='', flush=True)
    command_list = compile_commands(commands_folder, module_name, fields_model, preferred_order, preserve_markdown=True)

# retrieve docs folder
    docs_folder, file_name = path.split(docs_path)
    if not path.exists(docs_folder):
        if path.isdir(docs_folder):
            makedirs(docs_folder)

# retrieve commands template
    if not path.exists(template_path):
        raise ValueError('%s(template_path=%s) is not a valid path.' % (title, str(template_path)))
    cmd_template = open(template_path, 'rt').read()

# generate initial markdown
    markdown_text = '# Commands'

# add markdown for each command
    from copy import deepcopy
    for command in command_list:
        if verbose:
            print('.', end='', flush=True)

    # retrieve help output
        help_cmd = 'lab %s -h' % command['default_args']['command']
        help_text = command_output(help_cmd)
        command_usage = usage_regex.findall(help_text)[0].replace('usage: ', '')
        command_help = usage_regex.sub('', help_text).strip()

    # define markdown replacement
        def _replace_markdown(x):
            empty_string = ''
            if x.group(0) == '[[cli_usage]]':
                return command_usage
            elif x.group(0) == '[[cli_help]]':
                return command_help
            elif x.group(0) == '[[title]]':
                if not 'title' in command.keys():
                    return empty_string
                return command['title'].capitalize()
            elif x.group(0) == '[[benefit]]':
                if not 'benefit' in command.keys():
                    return empty_string
                return command['benefit']
            elif x.group(0) == '[[description]]':
                if not 'description' in command.keys():
                    return empty_string
                return command['description']
            else:
                return empty_string

    # substitute values in markdown
        cmd_markdown = deepcopy(cmd_template)
        cmd_markdown = markdown_regex.sub(_replace_markdown, cmd_markdown)
        markdown_text += '\n\n%s' % cmd_markdown

# save markdown in docs
    with open(docs_path, 'wt') as f:
        f.write(markdown_text)
        f.close()

    if verbose:
        print(' done.')

    return markdown_text

def generate_roadmap(docs_path, content_path, commands_folder, fields_model, module_name, preferred_order, verbose=True):

    from tabulate import tabulate
    from os import path, makedirs
    from pocketlab.utils import compile_commands
    from labpack.records.settings import load_settings

    title = 'generate_roadmap'

# retrieve list of commands
    if verbose:
        print('Compiling markdown for roadmap...', end='', flush=True)
    command_list = compile_commands(commands_folder, module_name, fields_model, preferred_order, preserve_markdown=True)

# retrieve docs folder
    docs_folder, file_name = path.split(docs_path)
    if not path.exists(docs_folder):
        if path.isdir(docs_folder):
            makedirs(docs_folder)

# retrieve content details
    if not path.exists(content_path):
        raise ValueError('%s(content_path=%s) is not a valid path.' % (title, str(content_path)))
    content_details = load_settings(content_path)

# merge command list into content
    for command in content_details['commands']:
        for key, value in command.items():
            found = False
            for com in command_list:
                if com['name'] == key:
                    command[key] = com['help']
                    found = True
                    break
            if not found:
                command[key] += ' **TODO**'

# generate initial markdown
    markdown_text = '# Roadmap\n'

# add feature list
    markdown_text += '\n## Features\n'
    for feature in content_details['features']:
        markdown_text += '- %s\n' % feature

# add command list
    markdown_text += '\n## Commands\n'
    command_rows = []
    command_headers = ['Command', 'Description', 'Status']
    for command in content_details['commands']:
        name = next(iter(command))
        desc = command[name]
        status = 'available'
        if desc.find('**TODO**') > -1:
            desc = desc.replace('**TODO**', '').strip()
            status = ''
        command_rows.append([name, desc, status])
    table_html = tabulate(command_rows, headers=command_headers, tablefmt='html')
    markdown_text += table_html

# save markdown in docs
    with open(docs_path, 'wt') as f:
        f.write(markdown_text)
        f.close()

    if verbose:
        print(' done.')

    return markdown_text

def generate_architecture(docs_path, content_path, verbose=True):

    from tabulate import tabulate
    from os import path, makedirs
    from labpack.records.settings import load_settings

    title = 'generate_architecture'

# retrieve list of commands
    if verbose:
        print('Compiling markdown for architecture...', end='', flush=True)

# retrieve docs folder
    docs_folder, file_name = path.split(docs_path)
    if not path.exists(docs_folder):
        if path.isdir(docs_folder):
            makedirs(docs_folder)

# retrieve content details
    if not path.exists(content_path):
        raise ValueError('%s(content_path=%s) is not a valid path.' % (title, str(content_path)))
    content_details = load_settings(content_path)

# generate initial markdown
    markdown_text = '# Architecture\n'

# add system architecture
#     markdown_text += '\n## %s\n' % content_details['architecture']['title']
    markdown_text += '%s\n' % content_details['architecture']['section']

# add object list
    markdown_text += '\n## System Resources\n'
    resource_rows = []
    resource_headers = ['Resource', 'Description']
    for resource in content_details['resources']:
        name = next(iter(resource))
        desc = resource[name]
        resource_rows.append([name, desc])
    table_html = tabulate(resource_rows, headers=resource_headers, tablefmt='html')
    markdown_text += table_html

# save markdown in docs
    with open(docs_path, 'wt') as f:
        f.write(markdown_text)
        f.close()

    if verbose:
        print(' done.')

    return markdown_text


if __name__ == '__main__':

    from copy import deepcopy
    from pocketlab import __module__, __order__
    from importlib.util import find_spec
    from pocketlab.init import fields_model
    from pocketlab.utils import compile_commands
    module_path = find_spec(__module__).submodule_search_locations[0]
    commands_kwargs = {
        'docs_path': 'docs/commands.md',
        'template_path': 'templates/commands.md',
        'commands_folder': '%s/commands/' % module_path,
        'fields_model': fields_model,
        'module_name': __module__,
        'preferred_order': __order__
    }
    generate_commands(**commands_kwargs)
    roadmap_kwargs = {
        'content_path': 'content.yaml'
    }
    roadmap_kwargs.update(**commands_kwargs)
    del roadmap_kwargs['template_path']
    roadmap_kwargs['docs_path'] = 'docs/roadmap.md'
    generate_roadmap(**roadmap_kwargs)
    architecture_kwargs = {
        'docs_path': 'docs/architecture.md',
        'content_path': 'content.yaml'
    }
    generate_architecture(**architecture_kwargs)
