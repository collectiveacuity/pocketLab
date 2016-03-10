=========
pocketLab
=========
*A Command Line Tool for Managing Laboratory Projects*

:Source: https://bitbucket.org/collectiveacuity/pocketlab.git

Commands
--------
- **start**: initiates a container with a project component
- **stop**: terminates container running a project component
- **home**: returns active location to project home
- **install**: installs files for a new component in the project
- **tunnel**:
- **monitor**:

Features
--------
-

System Requirements
-------------------
- **docker**: https://www.docker.com
- **virtualbox**: (on Mac & Windows)

Python Requirements
-------------------
- **jsonmodel**: https://pypi.python.org/pypi/jsonmodel

============
Installation
============
From BitBucket::

    $ git clone https://bitbucket.org/collectiveacuity/labmgmt.git
    $ python setup.py sdist --format=gztar,zip bdist_wheel
    $ python setup.py develop  # for local on-the-fly file updates

Getting Started
---------------
This module is designed to manage lab projects...

Change directory to local root for projects::

    $ lab home

Documentation
-------------
For more details about how to use pocketLab, refer to the
`Reference Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/pocketlab/REFERENCE.rst>`_