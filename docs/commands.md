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
Init adds a number of files to the working directory which are required for other lab processes. If not present, it will create a ```lab.yaml``` file in the root directory to manage various configuration options. It will also create, if missing, ```cred/``` and ```data/``` folders to store sensitive information outside version control along with a ```.gitignore``` (or ```.hgignore```) file to escape out standard non-VCS files.  

**Usage:**
```bash
$ lab init [-h] [--module STRING] [--vcs STRING] [--license STRING] [--heroku] [-q]
```
**Help:** 
```bash
Init adds a number of files to the working directory which are required for
other lab processes. If not present, it will create a 'lab.yaml' file in the
root directory to manage various configuration options. It will also create, if
missing, 'cred/' and 'data/' folders to store sensitive information outside
version control along with a '.gitignore' (or '.hgignore') file to escape out
standard non-VCS files.

optional arguments:
  -h, --help        show this help message and exit
  --module STRING   name for python module
  --vcs STRING      VCS service to generate ignore file
  --license STRING  name of software license type
  --heroku          add heroku config to cred folder
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
  

## Deploy
_Makes services available online._  

**Description:**  
Deploys one or more services as Docker containers to a remote platform.  

**Usage:**
```bash
$ lab deploy [-h] [-q] [--virtualbox STRING] PLATFORM [SERVICES [SERVICES ...]]
```
**Help:** 
```bash
Deploys one or more services as Docker containers to a remote platform.

positional arguments:
  PLATFORM             name of remote platform
  SERVICES             list of services in lab registry

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          turn off lab process messages
  --virtualbox STRING  name of docker virtualbox on Win7/8 (default: default)
```
  

## List
_Provides a way to find existing resources._  

**Description:**  
Generates a list of the resources of a specific type.  

**Usage:**
```bash
$ lab list [-h] [--more] RESOURCE
```
**Help:** 
```bash
Generates a list of the resources of a specific type.

positional arguments:
  RESOURCE    type of lab resource. eg. services, images...

optional arguments:
  -h, --help  show this help message and exit
  --more      paginate results longer than console height
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
  