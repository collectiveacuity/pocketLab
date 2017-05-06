.. image:: https://img.shields.io/pypi/v/pocketlab.svg
    :target: https://pypi.python.org/pypi/pocketlab
.. image:: https://img.shields.io/pypi/l/pocketlab.svg
    :target: https://pypi.python.org/pypi/pocketlab

=========
pocketLab
=========
*A Command Line Tool for Managing Laboratory Projects*

:Downloads: http://pypi.python.org/pypi/pocketLab
:Source: https://github.com/collectiveacuity/pocketLab
:Documentation: https://pocketlab.github.io

============
Installation
============
From PyPi::

    $ pip install pocketlab

From GitHub::

    $ git clone https://github.com/collectiveacuity/pocketLab
    $ cd pocketLab
    $ python setup.py install

===============
Getting Started
===============
This module is designed to manage the development operations of lab projects and make it easier to deploy code across different platforms. Pocket Lab relies heavily upon docker to provide consistency across development environments but it also streamlines the docker workflow without compromising the security of credentials and sensitive code.

Register a project in the working directory::

    $ lab home <project-alias>

Initialize the project framework in the working directory::

    $ lab init

For a list of all the commands, refer to the
`Reference Documentation on GitHub
<https://pocketlab.github.io/commands/>`_
