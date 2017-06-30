# Commands

## Home
_Home makes it easy to locate your services._  

**Description:**  
Home adds the service name and working directory to the lab registry. On its first run, it also adds the alias 'home' to bash config. As a result, on subsequent terminal sessions, typing ```$ home <service>``` will change the working directory to the folder registered under the service name.  

**Usage:**
```bash
$ lab home [-h] [--print] [--path STRING] [-f] SERVICE
```
**Help:** 
```bash
Home adds the service name and working directory to the lab registry. On its
first run, it also adds the alias 'home' to bash config. As a result, on
subsequent terminal sessions, typing 'home <service>' will change the working
directory to the folder registered under the service name.

positional arguments:
  SERVICE        name of service in lab registry

optional arguments:
  -h, --help     show this help message and exit
  --print        prints path of service root
  --path STRING  path to service root
  -f, --force    overwrite the existing resource
```
  

## Init
_Init adds the config files for other lab commands._  

**Description:**  
Init adds a number of files to the working directory which are required for other lab processes. If not present, it will create a ```lab.yaml``` file and a ```.lab``` folder in the root directory to manage various configuration options. It will also create, if missing, ```cred/``` and ```data/``` folders to store sensitive project information outside version control along with a ```.gitignore``` (or ```.hgignore```) file to escape out standard non-VCS files.

PLEASE NOTE: With the option ```--module <module_name>```, init creates instead a standard framework for publishing a python module.  

**Usage:**
```bash
$ lab init [-h] [--module STRING] [--vcs STRING] [--license STRING] [--heroku] [--aws] [-q]
```
**Help:** 
```bash
Init adds a number of files to the working directory which are required for
other lab processes. If not present, it will create a 'lab.yaml' file and a
'.lab' folder in the root directory to manage various configuration options. It
will also create, if missing, 'cred/' and 'data/' folders to store sensitive
project information outside version control along with a '.gitignore' (or
'.hgignore') file to escape out standard non-VCS files. PLEASE NOTE: With the
option '--module <module_name>', init creates instead a standard framework for
publishing a python module.

optional arguments:
  -h, --help        show this help message and exit
  --module STRING   name for python module
  --vcs STRING      VCS service to generate ignore file
  --license STRING  name of software license type
  --heroku          add heroku config to .lab folder
  --aws             add aws config to .lab folder
  -q, --quiet       turn off lab process messages
```
  

## Clean
_Frees up space by removing superfluous files._  

**Description:**  
Removes broken resources from the registries.  

**Usage:**
```bash
$ lab clean [-h] [-q]
```
**Help:** 
```bash
Removes broken resources from the registries.

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  turn off lab process messages
```
  

## Connect
_Edit settings on remote host manually._  

**Description:**  
Opens up a direct ssh connection to remote host. Connect is currently only available to the Amazon ec2 platform and only on systems running ssh natively. To connect to a remote host on Windows, try using Putty instead.

PLEASE NOTE: connect uses the docker container alias value specified in the lab.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".  

**Usage:**
```bash
$ lab connect [-h] [--env STRING] [--tag STRING] [--region STRING] [-q] PLATFORM [SERVICE]
```
**Help:** 
```bash
Opens up a direct ssh connection to remote host. Connect is currently only
available to the Amazon ec2 platform and only on systems running ssh natively.
To connect to a remote host on Windows, try using Putty instead. PLEASE NOTE:
connect uses the docker container alias value specified in the lab.yaml
configuration file to determine which instance to connect to. A tag must be
added manually to the instance with key "Containers" and value
"<container_alias>".

positional arguments:
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment
  --tag STRING     tag associated with resource
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
```
  

## Deploy
_Makes services available online._  

**Description:**  
Deploys one or more services as Docker containers to a remote platform. Deploy is currently only available for the heroku platform. Deploy can also deploy static html sites and apps using their dependencies if the root folder is added to one of the runtime type flags (ex. lab deploy heroku --html site/)  

**Usage:**
```bash
$ lab deploy [-h] [-q] [--virtualbox STRING] [--html STRING | --php STRING | --python STRING | --java STRING | --ruby STRING | --node STRING] PLATFORM [SERVICES [SERVICES ...]]
```
**Help:** 
```bash
Deploys one or more services as Docker containers to a remote platform. Deploy
is currently only available for the heroku platform. Deploy can also deploy
static html sites and apps using their dependencies if the root folder is added
to one of the runtime type flags (ex. lab deploy heroku --html site/)

positional arguments:
  PLATFORM             name of remote platform
  SERVICES             list of services in lab registry

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          turn off lab process messages
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
  --html STRING        path to folder with index.html
  --php STRING         path to folder with index.php
  --python STRING      path to folder with requirements.txt
  --java STRING        path to folder with Java Procfile
  --ruby STRING        path to folder with Ruby Procfile
  --node STRING        path to folder with package.json
```
  

## Get
_Copies remote files to your local machine._  

**Description:**  
Copies a file or folder on remote host to working directory on localhost. Get is currently only available for the Amazon ec2 platform.

PLEASE NOTE: get uses the docker container alias value specified in the lab.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".  

**Usage:**
```bash
$ lab get [-h] [--env STRING] [--tag STRING] [--region STRING] [-q] [-f] PATH PLATFORM [SERVICE]
```
**Help:** 
```bash
Copies a file or folder on remote host to working directory on localhost. Get is
currently only available for the Amazon ec2 platform. PLEASE NOTE: get uses the
docker container alias value specified in the lab.yaml configuration file to
determine which instance to connect to. A tag must be added manually to the
instance with key "Containers" and value "<container_alias>".

positional arguments:
  PATH             path to file or folder
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment
  --tag STRING     tag associated with resource
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
  -f, --force      overwrite the existing resource
```
  

## List
_Provides a way to find existing resources._  

**Description:**  
Generates a list of the resources of a specific type. Only the service resource type is supported, but docker oriented and remote host kinds of resources are coming.  

**Usage:**
```bash
$ lab list [-h] [--more] RESOURCE
```
**Help:** 
```bash
Generates a list of the resources of a specific type. Only the service resource
type is supported, but docker oriented and remote host kinds of resources are
coming.

positional arguments:
  RESOURCE    type of lab resource. eg. services, images...

optional arguments:
  -h, --help  show this help message and exit
  --more      paginate results longer than console height
```
  

## Put
_Copy files from your local machine._  

**Description:**  
Copies a local file or folder to user home on remote host. Put is currently only available for the Amazon ec2 platform.

PLEASE NOTE: put uses the docker container alias value specified in the lab.yaml configuration file to determine which instance to connect to. A tag must be added manually to the instance with key "Containers" and value "<container_alias>".  

**Usage:**
```bash
$ lab put [-h] [--env STRING] [--tag STRING] [--region STRING] [-q] [-f] PATH PLATFORM [SERVICE]
```
**Help:** 
```bash
Copies a local file or folder to user home on remote host. Put is currently only
available for the Amazon ec2 platform. PLEASE NOTE: put uses the docker
container alias value specified in the lab.yaml configuration file to determine
which instance to connect to. A tag must be added manually to the instance with
key "Containers" and value "<container_alias>".

positional arguments:
  PATH             path to file or folder
  PLATFORM         name of remote platform
  SERVICE          (optional) service in lab registry

optional arguments:
  -h, --help       show this help message and exit
  --env STRING     type of development environment
  --tag STRING     tag associated with resource
  --region STRING  name of platform region
  -q, --quiet      turn off lab process messages
  -f, --force      overwrite the existing resource
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
```
  

## Start
_Makes services available on localhost_  

**Description:**  
Initiates a container with the Docker image for one or more services.  

**Usage:**
```bash
$ lab start [-h] [-q] [--virtualbox STRING] [SERVICES [SERVICES ...]]
```
**Help:** 
```bash
Initiates a container with the Docker image for one or more services.

positional arguments:
  SERVICES             list of services in lab registry

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          turn off lab process messages
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
```
  

## Stop
_Ends service availability on localhost_  

**Description:**  
Stops and removes a running container for one or more services.  

**Usage:**
```bash
$ lab stop [-h] [-q] [--virtualbox STRING] [SERVICES [SERVICES ...]]
```
**Help:** 
```bash
Stops and removes a running container for one or more services.

positional arguments:
  SERVICES             list of services in lab registry

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          turn off lab process messages
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
```
  

## Update
_Keeps your services up-to-date with the latest configurations._  

**Description:**  
Updates the configuration files for a service with the latest pocketlab configurations.  

**Usage:**
```bash
$ lab update [-h] [-a] [-q] [SERVICES [SERVICES ...]]
```
**Help:** 
```bash
Updates the configuration files for a service with the latest pocketlab
configurations.

positional arguments:
  SERVICES     list of services in lab registry

optional arguments:
  -h, --help   show this help message and exit
  -a, --all    apply to all services in registry
  -q, --quiet  turn off lab process messages
```
  