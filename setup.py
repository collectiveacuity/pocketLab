import re
from setuptools import setup, find_packages

'''
References:
https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/distutils/index.html
https://github.com/jgehrcke/python-cmdline-bootstrap
http://www.pyinstaller.org/

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip
pip wheel --no-index --no-deps --wheel-dir dist dist/pocketlab-0.1.tar.gz

Upload Distributions to PyPi:
twine register dist/*
twine upload dist/[module-version]*

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files

Uninstall:
pip uninstall [module]
python setup.py develop --uninstall # for removing symbolic link
# remove command line tool in ../Python/Python35-32/Scripts/

CLI Installation:
command = 'name of command'
module = 'name of module'
    entry_points = {
        "console_scripts": ['%s = %s.cli:cli' % (command, module)]
    },

System Installation:
# http://www.pyinstaller.org/

Mercurial Dev Setup:
.hgignore (add dist/, *.egg-info/, '.git/')
hgrc [paths] default = ssh://hg@bitbucket.org/collectiveacuity/pocketlab

Git Public Setup:
.gitignore (add dist/, *.egg-info/, dev/, tests_dev/, docs/, .hg/, .hgignore)
git init
git remote add origin https://github.com/collectiveacuity/pocketLab.git

Git Public Updates:
git add -A
git commit -m 'updates' 
git push origin master
'''

config_file = open('pocketlab/__init__.py').read()
version = re.search("^__version__\s*=\s*'(.*)'", config_file, re.M).group(1)
command = re.search("^__command__\s*=\s*'(.*)'", config_file, re.M).group(1)
license_terms = re.search("^__license__\s*=\s*'(.*)'", config_file, re.M).group(1)
module = re.search("^__module__\s*=\s*'(.*)'", config_file, re.M).group(1)
author = re.search("^__author__\s*=\s*'(.*)'", config_file, re.M).group(1)
email = re.search("^__email__\s*=\s*'(.*)'", config_file, re.M).group(1)
url = re.search("^__url__\s*=\s*'(.*)'", config_file, re.M).group(1)
# author_list = re.search("^__authors__\s*=\s*'(.*)'", config_file, re.M).group(1)

setup(
    name=module,
    version=version,
    author=author,
    author_email=email,
    maintainer_email=email,
    url=url,
    entry_points={ "console_scripts": ['%s = %s.cli:cli' % (command, module)] },
    include_package_data=True,  # Checks MANIFEST.in for explicit rules
    packages=find_packages(),  # exclude=['cred','docs','keys','models','notes','tests', 'tinker'] Needed for bdist
    license=license_terms,
    description="A Command Line Tool for Managing Laboratory Projects",
    long_description=open('README.rst').read(),
    install_requires=[
        'jsonmodel',
        'labpack'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
)
