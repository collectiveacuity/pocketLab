# Commands

## Init
_Init adds the config files for other lab commands._  

**Description:**  
Init adds files to the working directory which are required for lab projects.

To create a framework for a webapp project, use the option ```--flask``` for a flask service, ```--webpack``` for a client-side ES6 framework using webpack or ```--express``` for a service-side ES6 server using node.js. With the options ```--pypi```, ```--npm``` or ```--jquery```, init creates instead a standard framework for publishing a module in python, node or jquery (respectively).  The options ```--heroku```, ```--ec2``` and ```--gae``` create configuration files used by other lab processes for cloud deployment on heroku, ec2 and gae (respectively).

NOTE: Init only creates files which are not already present.  

**Usage:**
```bash
$ lab init [-h] [--vcs STRING] [--license STRING] [--flask] [--webpack] [--express] [--jquery] [--pypi] [--npm] [--heroku] [--ec2] [--gae] [--docker] [--aws] [--asg] [-q] [-f] [SERVICE]
```
**Help:** 
```bash
Init adds files to the working directory which are required for lab projects.

To create a framework for a webapp project, use the option '--flask' for a flask
service, '--webpack' for a client-side ES6 framework using webpack or '--
express' for a service-side ES6 server using node.js. With the options '--pypi',
'--npm' or '--jquery', init creates instead a standard framework for publishing
a module in python, node or jquery (respectively).  The options '--heroku', '--
ec2' and '--gae' create configuration files used by other lab processes for
cloud deployment on heroku, ec2 and gae (respectively).

NOTE: Init only creates files which are not already present.

positional arguments:
  SERVICE           (optional) service in lab registry

optional arguments:
  -h, --help        show this help message and exit
  --vcs STRING      VCS service to generate ignore file
  --license STRING  name of software license type
  --flask           create flask service framework
  --webpack         create webpack client framework
  --express         create express service framework
  --jquery          create jquery service framework
  --pypi, --python  create python module framework
  --npm, --node     create node module framework
  --heroku          add heroku configs to workdir
  --ec2             add ec2 configs to workdir
  --gae             add gae configs to workdir
  --docker          add docker configs to workdir
  --aws             add aws config to .lab folder
  --asg             add asg config to workdir
  -q, --quiet       turn off lab process messages
  -f, --force       overwrite the existing resource
[0m
```
  

## Clean
_Frees up space by removing superfluous files._  

**Description:**  
Removes broken resources from the registries.  

**Usage:**
```bash
$ lab clean [-h] [-q] [--virtualbox STRING]
```
**Help:** 
```bash
Removes broken resources from the registries.

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          turn off lab process messages
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
[0m
```
  

## Connect
_Edit settings on remote host manually._  

**Description:**  
Opens up a direct ssh connection to remote host. Connect is currently only available to the Amazon ec2 platform and only on systems running ssh natively. To connect to a remote host on Windows, try using Putty instead.

PLEASE NOTE: connect uses the service name and other tags associated with remote instances to determine which instance to connect to. The service name will be added as part of ```lab launch ec2```. Otherwise, a tag must be added to the instance with key "Services" and value "<service1>,<service2>".  

**Usage:**
```bash
$ lab connect [-h] [--env STRING] [--tags STRING] [--region STRING] [-q] PLATFORM [SERVICE]
```
**Help:** 
```bash
Opens up a direct ssh connection to remote host. Connect is currently only
available to the Amazon ec2 platform and only on systems running ssh natively.
To connect to a remote host on Windows, try using Putty instead.

PLEASE NOTE: connect uses the service name and other tags associated with remote
instances to determine which instance to connect to. The service name will be
added as part of 'lab launch ec2'. Otherwise, a tag must be added to the
instance with key "Services" and value "<service1>,<service2>".

positional arguments:
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment (default: test)
  --tags STRING    tags associated with resource (comma sep)
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
[0m
```
  

## Deploy
_Makes a service available online._  

**Description:**  
Deploys a service to a remote platform. Deploy is currently only available for the heroku and ec2 platforms. Deploy can also deploy static html sites and apps using their dependencies if the root folder is added to one of the runtime type flags (ex. lab deploy heroku --html site/)

PLEASE NOTE: deploy uses the service name specified in the docker-compose.yaml configuration file to determine which instance to connect to. The service name will be added as part of ```lab launch ec2```. Otherwise, a tag must be added to the instance with key "Services" and value "<service1>,<service2>".  

**Usage:**
```bash
$ lab deploy [-h] [--env STRING] [--tags STRING] [--region STRING] [-q] [-f] [--resume] [--print] [--mount] [--virtualbox STRING] [--html STRING | --php STRING | --python STRING | --java STRING | --ruby STRING | --node STRING | --jingo STRING] PLATFORM [SERVICE]
```
**Help:** 
```bash
Deploys a service to a remote platform. Deploy is currently only available for
the heroku and ec2 platforms. Deploy can also deploy static html sites and apps
using their dependencies if the root folder is added to one of the runtime type
flags (ex. lab deploy heroku --html site/)

PLEASE NOTE: deploy uses the service name specified in the docker-compose.yaml
configuration file to determine which instance to connect to. The service name
will be added as part of 'lab launch ec2'. Otherwise, a tag must be added to the
instance with key "Services" and value "<service1>,<service2>".

positional arguments:
  PLATFORM             name of remote platform
  SERVICE              (optional) service in lab registry

optional arguments:
  -h, --help           show this help message and exit
  --env STRING         type of development environment (default: test)
  --tags STRING        tags associated with resource (comma sep)
  --region STRING      name of platform region
  -q, --quiet          turn off lab process messages
  -f, --force          overwrite the existing resource
  --resume             resume from prior progress point
  --print              prints command(s) without running
  --mount              mount volumes onto container
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
  --html STRING        path to folder with index.html
  --php STRING         path to folder with index.php
  --python STRING      path to folder with requirements.txt
  --java STRING        path to folder with Java Procfile
  --ruby STRING        path to folder with Ruby Procfile
  --node STRING        path to folder with package.json
  --jingo STRING       path to folder with jingo Procfile
[0m
```
  

## Get
_Copies remote files to your local machine._  

**Description:**  
Copies a file or folder on remote host to working directory on localhost. Get is currently only available for the Amazon ec2 platform.

PLEASE NOTE: get uses the service name specified in the docker-compose.yaml configuration file to determine which instance to connect to. The service name will be added as part of ```lab launch ec2```. Otherwise, a tag must be added to the instance with key "Services" and value "<service1>,<service2>".  

**Usage:**
```bash
$ lab get [-h] [--env STRING] [--tags STRING] [--region STRING] [-q] [-f] PATH PLATFORM [SERVICE]
```
**Help:** 
```bash
Copies a file or folder on remote host to working directory on localhost. Get is
currently only available for the Amazon ec2 platform.

PLEASE NOTE: get uses the service name specified in the docker-compose.yaml
configuration file to determine which instance to connect to. The service name
will be added as part of 'lab launch ec2'. Otherwise, a tag must be added to the
instance with key "Services" and value "<service1>,<service2>".

positional arguments:
  PATH             path to file or folder
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment (default: test)
  --tags STRING    tags associated with resource (comma sep)
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
  -f, --force      overwrite the existing resource
[0m
```
  

## Home
_Home makes it easy to locate your services._  

**Description:**  
Home adds the service name and working directory to the lab registry. On its first run, it also adds the alias 'home' to bash config. As a result, on subsequent terminal sessions, typing ```$ home <service>``` will change the working directory to the folder registered under the service name. A quicklink to the workdir is also added by ```lab init <service>```  

**Usage:**
```bash
$ lab home [-h] [--print] [--path STRING] [-f] SERVICE
```
**Help:** 
```bash
Home adds the service name and working directory to the lab registry. On its
first run, it also adds the alias 'home' to bash config. As a result, on
subsequent terminal sessions, typing 'home <service>' will change the working
directory to the folder registered under the service name. A quicklink to the
workdir is also added by 'lab init <service>'

positional arguments:
  SERVICE        name of service in lab registry

optional arguments:
  -h, --help     show this help message and exit
  --print        prints path of service root
  --path STRING  path to service root
  -f, --force    overwrite the existing resource
[0m
```
  

## Install
_Install adds a fully-configured software package to a remote platform._  

**Description:**  
Installs a software package on a running instance on a remote platform. Install is currently only available for the ec2 platform and supports the following packages:
nginx
certbot  

**Usage:**
```bash
$ lab install [-h] [--env STRING] [--region STRING] [--tags STRING] [--print] [-q] PACKAGE PLATFORM [SERVICE]
```
**Help:** 
```bash
Installs a software package on a running instance on a remote platform. Install
is currently only available for the ec2 platform and supports the following
packages:
nginx
certbot

positional arguments:
  PACKAGE          name of software package
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment (default: test)
  --region STRING  name of platform region
  --tags STRING    tags associated with resource (comma sep)
  --print          prints command(s) without running
  -q, --quiet      turn off lab process messages
[0m
```
  

## Launch
_Launch creates one or more remote instances to host services._  

**Description:**  
Launches an instance or an auto-scaling group on a remote platform. Launch is currently only available for the ec2 platform. To create an configuration file to launch an ec2 instance, run ```lab init --ec2``` and adjust the settings appropriately.  

**Usage:**
```bash
$ lab launch [-h] [--region STRING] [-q] [-f] PLATFORM [SERVICE]
```
**Help:** 
```bash
Launches an instance or an auto-scaling group on a remote platform. Launch is
currently only available for the ec2 platform. To create an configuration file
to launch an ec2 instance, run 'lab init --ec2' and adjust the settings
appropriately.

positional arguments:
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
  -f, --force      overwrite the existing resource
[0m
```
  

## List
_Provides a way to find existing resources._  

**Description:**  
Generates a list of the resources of a specific type. Only the service resource type is supported, but docker oriented and remote host kinds of resources are coming.  

**Usage:**
```bash
$ lab list [-h] [--region STRING] [--more] [-a] RESOURCE [PLATFORM]
```
**Help:** 
```bash
Generates a list of the resources of a specific type. Only the service resource
type is supported, but docker oriented and remote host kinds of resources are
coming.

positional arguments:
  RESOURCE         type of lab resource. eg. services, images...
  PLATFORM         (optional) name of remote platfrom

optional arguments:
  -h, --help       show this help message and exit
  --region STRING  name of platform region
  --more           paginate results longer than console height
  -a, --all        include all details in results
[0m
```
  

## Put
_Copy files from your local machine._  

**Description:**  
Copies a local file or folder to user home on remote host. Put is currently only available for the Amazon ec2 platform.

PLEASE NOTE: put uses the service name specified in the docker-compose.yaml configuration file to determine which instance to connect to. The service name will be added as part of ```lab launch ec2```. Otherwise, a tag must be added to the instance with key "Services" and value "<service1>,<service2>".  

**Usage:**
```bash
$ lab put [-h] [--env STRING] [--tags STRING] [--region STRING] [-q] [-f] PATH PLATFORM [SERVICE]
```
**Help:** 
```bash
Copies a local file or folder to user home on remote host. Put is currently only
available for the Amazon ec2 platform.

PLEASE NOTE: put uses the service name specified in the docker-compose.yaml
configuration file to determine which instance to connect to. The service name
will be added as part of 'lab launch ec2'. Otherwise, a tag must be added to the
instance with key "Services" and value "<service1>,<service2>".

positional arguments:
  PATH             path to file or folder
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment (default: test)
  --tags STRING    tags associated with resource (comma sep)
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
  -f, --force      overwrite the existing resource
[0m
```
  

## Remove
_Removes a service listing from the lab registry._  

**Description:**  
Removes clutter from your records.  

**Usage:**
```bash
$ lab remove [-h] SERVICE
```
**Help:** 
```bash
Removes clutter from your records.

positional arguments:
  SERVICE     name of service in lab registry

optional arguments:
  -h, --help  show this help message and exit
[0m
```
  

## Start
_Makes services available on localhost_  

**Description:**  
Initiates a container with the Docker image for one or more services. Unless overridden by flags, lab automatically adds the environmental variables SYSTEM_IP, SYSTEM_ENVIRONMENT, SYSTEM_PLATFORM and PUBLIC_IP of the host machine to the container.  

**Usage:**
```bash
$ lab start [-h] [-q] [--virtualbox STRING] [--env STRING] [--print] [SERVICES [SERVICES ...]]
```
**Help:** 
```bash
Initiates a container with the Docker image for one or more services. Unless
overridden by flags, lab automatically adds the environmental variables
SYSTEM_IP, SYSTEM_ENVIRONMENT, SYSTEM_PLATFORM and PUBLIC_IP of the host machine
to the container.

positional arguments:
  SERVICES             list of services in lab registry

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          turn off lab process messages
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
  --env STRING         type of development environment (default: dev)
  --print              prints command(s) without running
[0m
```
  

## Update
_Keeps your services up-to-date with the latest configurations._  

**Description:**  
Updates the configuration files for a service. When a package and platform are specified, update adds (or updates) the service to the configuration files for the package on the platform. Otherwise, update only updates the local configuration files for a service with the latest pocketlab configurations.  

**Usage:**
```bash
$ lab update [-h] [--env STRING] [--region STRING] [--tags STRING] [--print] [-a] [--ssl] [-q] [PACKAGE] [PLATFORM] [SERVICE]
```
**Help:** 
```bash
Updates the configuration files for a service. When a package and platform are
specified, update adds (or updates) the service to the configuration files for
the package on the platform. Otherwise, update only updates the local
configuration files for a service with the latest pocketlab configurations.

positional arguments:
  PACKAGE          (optional) name of software package
  PLATFORM         (optional) name of remote platfrom
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment (default: test)
  --region STRING  name of platform region
  --tags STRING    tags associated with resource (comma sep)
  --print          prints command(s) without running
  -a, --all        apply to all services in registry
  --ssl            turn off ssl everywhere
  -q, --quiet      turn off lab process messages
[0m
```
  