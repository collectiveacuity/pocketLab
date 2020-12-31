''' a package of methods to handle node file generation '''
__author__ = 'rcj1492'
__created__ = '2020.12'
__license__ = '©2020 Collective Acuity'


def generate_json(template_path, model_path, fields_map, replacement_map, printer):
    from os import path
    if not path.exists(template_path):
        import json
        from pocketlab.methods.config import retrieve_template, replace_text
        template_text = retrieve_template(model_path)
        template_json = json.loads(template_text)
        for key, value in fields_map.items():
            if key in template_json.keys():
                template_json[key] = value
        template_text = json.dumps(template_json, indent=2)
        template_text = replace_text(template_text, replacement_map=replacement_map)
        with open(template_path, 'wt', encoding='utf-8') as f:
            f.write(template_text)
            f.close()
        printer(template_path)

def generate_package(package_path, package_text, dependency_text, replacement_map, printer):

    from os import path
    if not path.exists(package_path):
        import json
        from pocketlab.methods.config import replace_text
        replacement_map['<global-dependencies>'] = ''
        replacement_map['<local-dependencies>'] = ''
        package_text = replace_text(package_text, replacement_map=replacement_map)
        package_json = json.loads(package_text)
        package_local = package_json['devDependencies']
        package_global = json.loads(dependency_text)
        for key in package_local.keys():
            if replacement_map['<local-dependencies>']:
                replacement_map['<local-dependencies>'] += ' '
            replacement_map['<local-dependencies>'] += key
        for key, value in package_global.items():
            if replacement_map['<global-dependencies>']:
                replacement_map['<global-dependencies>'] += ' '
            replacement_map['<global-dependencies>'] += key
            package_json['devDependencies'][key] = value
        package_text = json.dumps(package_json, indent=2)
        with open(package_path, 'wt', encoding='utf-8') as f:
            f.write(package_text)
            f.close()
        printer(package_path)