ChangeLog
=========

0.9 (2018.09.15)
----------------
* [FEATURE ADDED] --jquery flag for init command to setup a jquery module framework
* [FEATURE ADDED] --node flag for init command to setup a node module framework
* [DEPRECATED] --module flag has been replaced by --python in init command

0.8 (2018.08.27)
----------------
* [COMMAND ADDED] added launch command to start a remote instance (ec2 only)
* [FEATURE ADDED] --ec2 flag for init command to setup ec2 config file for launch
* [FEATURE ADDED] added ec2 platform and certbot ssl to deploy options
* [FEATURE ADDED] added jingo app support for heroku deployment
* [UPDATE] added container:release to heroku-cli commands in deployment
* [UPDATE] added list of certificates to renew during ec2 deploy 
* [BUG FIX] removed requirement for docker-compose.yaml to use connect command
* [BUG FIX] added support for docker-compose.yml extension as well as .yaml
* [BUG FIX] removed auto-generation of "network" field from docker-compose.yaml
* [BUG FIX] migrated proxies field functionality to "labels" in docker-compose.yaml

0.7 (2018.02.15)
----------------
* [COMMAND ADDED] added start command to run services in local docker containers
* [FEATURE ADDED] replaced lab.yaml with docker-compose.yaml
* [FEATURE ADDED] added color to error, success and warning messages
* [UPDATE] list command with instances option
* [BUG FIX] handled running container excepts to docker image removal
* [BUG FIX] updated registry search with upstream changes made to appdataClient

0.6 (2018.02.05)
----------------
* [COMMAND DEPRECATED] stop command removed in preference of native docker stop
* [FEATURE ADDED] removal of stall docker images and containers added to clean
* [UPDATE] deploy command updated with latest heroku-cli methods
* [UPDATE] documentation improvements made

0.5 (2017.06.30)
----------------
* [BUG FIX] fixed element key name error in tags collected for aws instances

0.4 (2017.06.30)
----------------
* [COMMAND ADDED] connect command uses ssh to connect to instances (ec2 only)
* [COMMAND ADDED] put command uses scp to transfer file to instance (ec2 only)
* [COMMAND ADDED] get command uses scp to transfer file from instance (ec2 only)
* [FEATURE ADDED] --html flag to deploy command to deploy html site (heroku only)
* [FEATURE ADDED] --aws flag to init command to setup aws config file
* [FEATURE ADDED] .lab folder created in root directory by init commmand

0.3 (2017.06.04)
----------------
* [COMMAND ADDED] deploy command deploys docker image to remote host (heroku only)
* [COMMAND ADDED] stop command terminates docker containers
* [COMMAND ADDED] start command initiates docker containers
* [FEATURE ADDED] init commmand has option to setup framework for python modules
* [FEATURE ADDED] --heroku flag to init command to setup heroku config file
* [FEATURE ADDED] update command updates the setup.py comments

0.2 (2017.05.27)
----------------
* Upload of Module to PyPi
* Creation of GitHub Repo
* Separation of WIP methods into Mercurial Repo

0.1 (2016.03.03)
----------------
* Local Build of Package
* Creation of BitBucket Repo