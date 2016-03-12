============================
pocketLab Reference Document
============================
*Documentation for pocketLab Tool*

Terminology
-----------
Commands
^^^^^^^^

Objects
^^^^^^^

:project: **[-p, --project]** arrangement of an application or service
:component: **[-c, --component]** modular component of the project
:container: **[-a, --alias]** instantiation of a single component in a docker container
:build: **[-b, --build]** instantiation of the assembled project components in a set of docker containers
:platform: **[--platform]** location where a build of the project is assembled
:image: **[-i, --image]** docker image with component dependencies
:repo: **[-r, --repo]** repository containing files for a project component
:file: **[-f, --file]** path to a file with configuration settings
:virtualbox: **[--virtualbox]** oracle virtualbox boot2docker image (on Mac & Windows)
:tag: **[-t, --tag]** metatag associated with an object

Toggles
^^^^^^^

-s, --set  save current instructions in project configurations
-q, --quiet  quiet the stdout from command processes
-l, --log  enable logging of stdout from container
--username USERNAME  add a USERNAME to a resource request
--password PASSWORD  add a PASSWORD to a resource request


