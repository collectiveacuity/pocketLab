# Roadmap

## Features
- Docker Wrapper
- GitHub / BitBucket / Gitlab Repos
- OS Independence
- AWS Deployment Management
- Let's Encrypt SSL Certificates
- LocalTunnel.me / Ngrok
- PingAPI / Uptime Robot Monitoring
- Test Sequencing

## Commands
<table>
<thead>
<tr><th>Command  </th><th>Description                                    </th><th>Status                                   </th></tr>
</thead>
<tbody>
<tr><td>home     </td><td>creates a home for service in workdir          </td><td>available                                </td></tr>
<tr><td>init     </td><td>creates a lab framework in workdir             </td><td>available                                </td></tr>
<tr><td>list     </td><td>lists the instances of a resource type         </td><td>available                                </td></tr>
<tr><td>update   </td><td>updates the config files for a service         </td><td>available                                </td></tr>
<tr><td>remove   </td><td>removes a service from the registry            </td><td>available                                </td></tr>
<tr><td>clean    </td><td>cleans registries of broken resources          </td><td>available                                </td></tr>
<tr><td>build    </td><td>creates a new image from Dockerfile for service</td><td><sup>use <i><b>docker build</b></i></sup></td></tr>
<tr><td>start    </td><td>initiates Docker containers for services       </td><td>available                                </td></tr>
<tr><td>stop     </td><td>terminates a running container for a service   </td><td><sup>use <i><b>docker stop</b></i></sup> </td></tr>
<tr><td>enter    </td><td>opens up a shell cli inside a running container</td><td><sup>use <i><b>docker exec</b></i></sup> </td></tr>
<tr><td>deploy   </td><td>deploys service to a remote platform           </td><td>available                                </td></tr>
<tr><td>connect  </td><td>connects to remote host through ssh            </td><td>available                                </td></tr>
<tr><td>put      </td><td>copy a file to remote host through scp         </td><td>available                                </td></tr>
<tr><td>get      </td><td>copy a file from remote host through scp       </td><td>available                                </td></tr>
<tr><td>setup    </td><td>creates account resources for a remote platform</td><td>                                         </td></tr>
</tbody>
</table>