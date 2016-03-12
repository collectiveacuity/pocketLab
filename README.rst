=========
pocketLab
=========
*A Command Line Tool for Managing Laboratory Projects*

:Source: https://bitbucket.org/collectiveacuity/pocketlab.git

Commands
--------

:**new**: create a new project
:**home**: changes working directory to project home
:**add**: downloads image and files for a project component
:start: initiates a container with a project component
:enter: opens up a shell cli inside a running container
:stop: terminates container running a project component
:**reboot**: restart a container running a project component
:**tunnel**: creates a local tunnel to <sub-domain>.localtunnel.me
:**monitor**: creates a scheduled request to url endpoint
:**setup**: creates required account resources on a remote service
:**compose**: creates a set of containers from components in project
:**connect**: opens up a direct ssh connection to remote build
:**test**: performs tests on a project set to determine health
:**deploy**: places a project set into production
:**renew**: retrieves a new ssl certificate for url endpoint
:**update**: updates the components in an active project set
:**import**: import a pre-existing project from a remote repo

Low-Level Commands
------------------

:**images**: lists the images installed locally
:**containers**: lists the containers running currently
:**pull**: downloads an image or folder from a remote VCS repository
:**remove**: deletes an image or folder from the local environment
:**build**: creates a new image from Dockerfile in project component
:**clean**: removes broken images and stopped containers

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