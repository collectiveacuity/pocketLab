============================
pocketLab Reference Document
============================
*Documentation for pocketLab Tool*

Terminology
-----------
Commands
^^^^^^^^

Objects/Resources
^^^^^^^^^^^^^^^^^

:project: [-p, --project] arrangement of an application or service
:component: [-c, --component] modular component of the project
:container: [-a, --alias] instantiation of a single component
:build: [-b, --build] instantiation of the assembled project components
:platform: [-m, --platform] location where a build is assembled
:image: [-i, --image] docker image with component dependencies
:repo: [-r, --repo] file repository containing a project component
:file: [-f, --file] path (or url) to a file with configuration settings
:virtualbox: [-v, --virtualbox] oracle virtualbox boot2docker image (on Mac & Windows)

Toggles
^^^^^^^

:set: [-s, --set] save current instructions in project configurations
:tag: [-t, --tag] add a tag to an object
:quiet: [-q, --quiet] quiet the stdout from command processes
:log: [-l, --log] enabling of logging of stdout from container
:username: [-u, --username] add a username to a resource request
:password: [-w, --password] add a password to a resource request


