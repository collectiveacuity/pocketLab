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
:Documentation: https://collectiveacuity.github.io/pocketLab/

============
Installation
============
From PyPi::

    $ pip install pocketlab

From GitHub::

    $ git clone https://github.com/collectiveacuity/pocketLab
    $ cd pocketLab
    $ python setup.py sdist --format=gztar,zip
    $ pip wheel --no-index --no-deps --wheel-dir dist dist/pocketlab-0.*.tar.gz
    $ pip install dist/pocketlab-0.*-py3-none-any.whl

===============
Getting Started
===============
This module is designed to manage the development operations of lab projects and make it easier to deploy code across different platforms. Pocket Lab relies heavily upon Docker to provide consistency across development environments but it also streamlines the Docker workflow without compromising the security of credentials and sensitive code.

**Service-Oriented Architecture**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pocket Lab is built to facilitate a service-oriented architecture. A service can be a data processor, client-side code, a backend server, a job scheduler, a database, etc... But a service also maps one-to-one to many other components of development: a repo, an image, a container, a folder, etc... Importantly, a project or application is typically made up of one or more services and services can also be provided by a third party. This module uses the service as the principle atomic component to manage the compositional process of project development.

Register a service in the working directory::

    $ lab home <service>

Initialize the lab framework in the working directory::

    $ lab init --project

For a list of all the commands, refer to the
`Reference Documentation on GitHub
<https://collectiveacuity.github.io/pocketLab/commands/>`_
