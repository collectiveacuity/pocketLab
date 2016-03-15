__author__ = 'rcj1492'
__created__ = '2016.03'

from os import environ
from subprocess import check_output

class localhostSession(object):

    def __init__(self):

    # retrieve OS variable from system
        env_os = environ.get('OS')
        if not env_os:
            sys_command = 'uname -a'
            env_os = check_output(sys_command).decode('utf-8').replace('\n','')

    # determine OS from environment variable
        local_os = ''
        if 'Linux' in env_os:
            local_os = 'Linux'
        elif 'FreeBSD' in env_os:
            local_os = 'FreeBSD'
        elif 'Windows' in env_os:
            local_os = 'Windows'
        elif 'Darwin' in env_os:
            local_os = 'Mac'
        elif 'SunOS' in env_os:
            local_os = 'Solaris'
        self.os = local_os

    # retrieve USERNAME variable from system
        self.username = ''
        env_username = environ.get('USERNAME')
        if env_username:
            self.username = env_username

    def userData(self, org_name, prod_name):

        data_path = ''

        if self.os == 'Windows':
            from re import compile
            xp_pattern = compile('^C:\\Documents and Settings')
            if xp_pattern.findall(environ.get('APPDATA')):
                data_path = 'C:\\Documents and Settings\\%sLocal Settings\\Application Data\\%s\\%s\\User Data' % (self.username, org_name, prod_name)
            else:
                data_path = 'C:\\Users\\%s\\AppData\\Local\\%s\\%s\\User Data' % (self.username, org_name, prod_name)

        elif self.os == 'Mac':
            data_path = '~/Library/Application Support/%s/%s' % (org_name, prod_name)

        elif self.os in ('Linux', 'FreeBSD', 'Solaris'):
            org_format = org_name.replace(' ','-').lower()
            prod_format = prod_name.replace(' ', '-').lower()
            data_path = '~/.config/%s-%s/' % (org_format, prod_format)

        return data_path