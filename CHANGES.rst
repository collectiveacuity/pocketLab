ChangeLog
=========

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