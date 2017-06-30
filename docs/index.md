# Pocket Lab
*A Command Line Tool for Managing Laboratory Projects*  
by [Collective Acuity](http://collectiveacuity.com)

<table>
  <tbody>
    <tr>
      <td><b>Downloads</b></td>
      <td><a href="http://pypi.python.org/pypi/pocketLab">http://pypi.python.org/pypi/pocketLab</a></td>
    </tr>
    <tr>
      <td><b>Source</b></td>
      <td><a href="https://github.com/collectiveacuity/pocketLab">https://github.com/collectiveacuity/pocketLab</a></td>
    </tr>
    <tr>
      <td><b>Documentation</b></td>
      <td><a href="https://pocketlab.github.io">https://collectiveacuity.github.io/pocketLab/</a></td>
    </tr>
  </tbody>
</table>

## Introduction
Pocket Lab is a python-based command-line tool which is designed to manage the development operations of lab projects and make it easier to deploy code across different platforms. Pocket Lab relies heavily upon Docker to provide consistency across development environments but it also streamlines the Docker workflow without compromising the security of credentials and sensitive code.  

## Integrated Services
- **Docker**: https://www.docker.com
- **Virtualbox**: (on Windows 7/8)
- **Heroku**: https://devcenter.heroku.com/articles/heroku-cli
- **AWS**: https://console.aws.amazon.com

## Installation
From PyPi
```bash
    $ pip install pocketlab
```
From GitHub
```bash
    $ git clone https://github.com/collectiveacuity/pocketLab
    $ cd pocketLab
    $ python setup.py sdist --format=gztar,zip
    $ pip wheel --no-index --no-deps --wheel-dir dist dist/pocketlab-0.*.tar.gz
    $ pip install dist/pocketlab-0.*-py3-none-any.whl
```

## Getting Started
All commands for Pocket Lab use the 'lab' keyword. So, at any time, you can type ```lab --help``` from the terminal to see the help menu for the module. In order to use the module for building and deployment with docker, you will first need to setup the service framework around your project with a couple of commands. 

Register a service in the working directory::

    $ lab home <service>

Initialize the lab framework in the working directory::

    $ lab init

You can run these commands in a fresh directory at the start of a new project, but they are especially useful for preparing your localhost environment after you have cloned a repo from the remote repository. ```lab init``` will create a couple of local folders for managing credentials and any local data volumes. It will also add placeholder files in those folders from the notes directory and ensure that your version control system ignores these sensitive folders. When you need to update your credentials or edit your configuration, you can simply change the values in these files.

## Further Reading
Once you have setup the lab framework for your project, you can use other commands to build images, run them locally or deploy them to a variety of cloud providers. Descriptions for how to use the other commands can be found on the [Commands page](commands.md).
