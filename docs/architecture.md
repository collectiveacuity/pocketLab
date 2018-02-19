# Architecture
Pocket Lab is designed around a service-oriented architecture. A service can be a data processor, client-side code, a backend server, a job scheduler, a database, etc. But a service also maps one-to-one to many other components of development: a repo, an image, a container, a folder, etc. Importantly, a project or application is typically made up of one or more services and services can also be provided by a third party. This module uses the service as the principle atomic component to manage the compositional process of project development and deployment.

## System Resources
<table>
<thead>
<tr><th>Resource   </th><th>Description                                                     </th></tr>
</thead>
<tbody>
<tr><td>service    </td><td>self-contained modular component of an application or project   </td></tr>
<tr><td>project    </td><td>group of interconnected services with user application          </td></tr>
<tr><td>image      </td><td>compilation of code & dependencies for service in a Docker image</td></tr>
<tr><td>container  </td><td>instantiation of a service in a Docker container                </td></tr>
<tr><td>platform   </td><td>computational resources that run a service                      </td></tr>
<tr><td>instance   </td><td>instantiation of a project on a platform                        </td></tr>
<tr><td>region     </td><td>sub-division of platform to manage content distribution         </td></tr>
<tr><td>environment</td><td>sub-division of plaform to manage development process           </td></tr>
<tr><td>repo       </td><td>version control repository containing the files for a service   </td></tr>
<tr><td>file       </td><td>path to a file with configuration settings                      </td></tr>
<tr><td>virtualbox </td><td>oracle virtualbox boot2docker image (on Win7/8)                 </td></tr>
<tr><td>tag        </td><td>metadata associated with a resource                             </td></tr>
<tr><td>log        </td><td>file or service in which to log stdout of service               </td></tr>
</tbody>
</table>
# Configurations

## [Certbot](https://letsencrypt.org/getting-started/)
_A Free SSL Certificate Authority_  
  

**Installation on EC2:**    
```bash
$ sudo yum install -y wget
$ wget https://dl.eff.org/certbot-auto
$ sudo chmod a+x certbot-auto
$ sudo mv certbot-auto /usr/local/bin/certbot-auto
$ sudo service nginx stop # optional
$ sudo su -
$ certbot-auto certonly --standalone -d collectiveacuity.com,www.collectiveacuity.com --debug
> Is this ok [y/d/N]:
> Enter email address: (used … cancel):
> (A)gree/(C)ancel:
> (Y)es/(N)o:
$ sudo service nginx start # optional
```

**Renewal:**(certificate expires every 90 days)
```bash
$ sudo su -
$ certbot-auto renew --standalone --debug --pre-hook "service nginx stop" --post-hook "service nginx start"
$ exit
```

**Modification:** 
```bash
$ sudo su -
$ certbot-auto certonly --standalone --debug -n --cert-name collectiveacuity.com -d collectiveacuity.com,www.collectiveacuity.com,api.collectiveacuity.com --pre-hook "service nginx stop" --post-hook "service nginx start"  --debug
$ exit

```

**Check Certificates:**  
```bash
$ sudo su -
$ certbot-auto certificates --standalone --debug --pre-hook "service nginx stop" --post-hook "service nginx start" 
$ exit
```

**Troubleshooting:**  
1. Due to updates to certbot, python modules may be missing from installation:
```bash
$ sudo su -
$ pip install -U pip
$ /root/.local/share/letsencrypt/bin/pip install {missing module}
```
2. Due to 32bit / 64 bit issues, python venv libs may need to be copied:
```bash
$ sudo su -
$ \cp -r /opt/eff.org/certbot/venv/lib64/* /opt/eff.org/certbot/venv/lib/
$ exit
```
