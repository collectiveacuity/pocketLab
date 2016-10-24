=========
pocketLab
=========
*A Command Line Tool for Managing Laboratory Projects*

:Source: https://bitbucket.org/collectiveacuity/pocketlab.git

Commands
--------

:home: manages the local path information for a project

Roadmap
-------

:init: creates a local lab server, scheduler and database **#TODO**
:create: creates a project architecture in working directory **#TODO**
:register: adds a project to the registry **#TODO**
:list: report a list of project resources of a given type **#TODO**
:add: downloads image and files for a project component **#TODO**
:remove: remove a specific project resource **#TODO**
:start: initiates a container with a project component **#TODO**
:enter: opens up a shell cli inside a running container **#TODO**
:stop: terminates container running a project component **#TODO**
:reboot: restart a container running a project component **#TODO**
:tunnel: creates a local tunnel to <sub-domain>.localtunnel.me **#TODO**
:monitor: creates a scheduled request to url endpoint **#TODO**
:setup: creates required account resources on a remote service **#TODO**
:compose: creates a set of containers from components in project **#TODO**
:connect: opens up a direct ssh connection to remote build **#TODO**
:test: performs tests on a project set to determine health **#TODO**
:deploy: places a project set into production **#TODO**
:renew: retrieves a new ssl certificate for url endpoint **#TODO**
:update: updates the components in an active project set **#TODO**

Low-Level Commands
------------------

:pull: downloads an image or folder from a remote VCS repository **#TODO**
:build: creates a new image from Dockerfile in project component **#TODO**
:clean: removes broken images and stopped containers **#TODO**

Features
--------
- Docker Wrapper
- GitHub & BitBucket Repos
- OS Independence
- AWS Deployment Management
- Let's Encrypt SSL Certificates
- LocalTunnel.me
- PingAPI Monitoring
- Test Sequencing

System Requirements
-------------------
- **docker**: https://www.docker.com
- **virtualbox**: (on Mac & Windows)

Python Requirements
-------------------
- **jsonmodel**: https://pypi.python.org/pypi/jsonmodel
- **labpack**: https://pypi.python.org/pypi/labpack

============
Installation
============
From BitBucket::

    $ git clone https://bitbucket.org/collectiveacuity/pocketlab.git
    $ python setup.py sdist --format=gztar,zip
    $ pip wheel --no-index --no-deps --wheel-dir dist dist/pocketlab-*.tar.gz
    $ python setup.py develop  # for local on-the-fly file updates

Getting Started
---------------
This module is designed to manage lab projects...

Register a project in the working directory::

    $ lab home -p <project-name>

Documentation
-------------
For more details about how to use pocketLab, refer to the
`Reference Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/pocketlab/src/master/REFERENCE.rst>`_
