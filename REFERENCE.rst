============================
pocketLab Reference Document
============================
*Documentation for pocketLab Tool*

Terminology
-----------
Commands
^^^^^^^^

Resources
^^^^^^^^^

:project [-p, --project]: arrangement of an application or service
:component [-c, --component]: modular component of the project
:container [-a, --alias]: instantiation of a single component
:build [-b, --build]: instantiation of the assembled project components
:platform [--platform]: location where a build is assembled
:image [-i, --image]: docker image with component dependencies
:repo [-r, --repo]: file repository containing a project component
:file [-f, --file]: path (or url) to a file with configuration settings
:virtualbox [--virtualbox]: oracle virtualbox boot2docker image (on Mac & Windows)


Toggles
^^^^^^^

-s, --set  save current instructions in project configurations
-t TAG, --tag TAG  add a TAG to an object
-q, --quiet  quiet the stdout from command processes
-l, --log  enabling of logging of stdout from container
--username USERNAME  add a USERNAME to a resource request
--password PASSWORD  add a PASSWORD to a resource request


