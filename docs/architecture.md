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