# pocketLab Reference Document

## Commands
TBD

## Objects

:project: **[-p, --project]** arrangement of an application or service
:component: **[-c, --component]** modular component of the project
:container: **[-a, --alias]** instantiation of a single component in a docker container
:build: **[-b, --build]** instantiation of the assembled project components in a set of docker containers
:platform: **[--platform]** platform on which a build of the project is assembled
:environment: **[--environment]** sub-division of a platform to manage updating process
:layer: **[--layer]** sub-division of project components to manage updating process
:region: **[--region]** sub-division of platform to manage content distribution
:image: **[-i, --image]** docker image with component dependencies
:repo: **[-r, --repo]** repository containing files for a project component
:file: **[-f, --file]** path to a file with configuration settings
:virtualbox: **[--virtualbox]** oracle virtualbox boot2docker image (on Mac & Windows)
:tag: **[-t, --tag]** metatag associated with a resource
:log: **[-l, --log]** file or service in which to log stdout from container

## Toggles

-s, --set  save current instructions in project configurations
-q, --quiet  turn off stdout lab messages
-z, --zzz  turn off lab logging (logging helps lab bot learn)
--username  add a USERNAME to a resource request
--password  add a PASSWORD to a resource request

## Common Sys Options

-d  run process in background as a daemon
-y  agree to any confirmation requests
-f  force override blocking errors
-h  print out help menu
-v  print out version of program
-e  define an environmental variable
-l  send stdin, stdout, stderr to log file


