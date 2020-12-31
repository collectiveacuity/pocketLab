# Roadmap

## Features
- Creates VCS Compliant Project Framework
- Creates Python Module Framework
- Runs as Docker Compose Wrapper
- Maintains Compatibility Across OS
- Automates Service Deployment to EC2
- Automates Service Deployment to Heroku
- Automates Let's Encrypt SSL Certificates
- Updates GitHub / BitBucket / Gitlab Repos **TODO**
- Adds PingAPI / Uptime Robot Monitoring **TODO**
- Adds LastPass Credential Sharing **TODO**
- Performs Test Sequencing **TODO**
- Automates AWS / Heroku Account Setup **TODO**

## Commands
<table>
<thead>
<tr><th>Command   </th><th>Description                                           </th><th>Status                                   </th></tr>
</thead>
<tbody>
<tr><td>init      </td><td>creates a lab framework in workdir                    </td><td>available                                </td></tr>
<tr><td>list      </td><td>lists the instances of a resource type                </td><td>available                                </td></tr>
<tr><td>update    </td><td>updates the config files for a service                </td><td>available                                </td></tr>
<tr><td>remove    </td><td>removes a service from the registry                   </td><td>available                                </td></tr>
<tr><td>clean     </td><td>cleans registries of broken resources                 </td><td>available                                </td></tr>
<tr><td>home      </td><td>creates a quicklink to workdir                        </td><td>available                                </td></tr>
<tr><td>build     </td><td>creates a new image from Dockerfile for service       </td><td>&lt;sup&gt;use &lt;i&gt;&lt;b&gt;docker build&lt;/b&gt;&lt;/i&gt;&lt;/sup&gt;</td></tr>
<tr><td>start     </td><td>initiates Docker containers for services              </td><td>available                                </td></tr>
<tr><td>stop      </td><td>terminates a running container for a service          </td><td>&lt;sup&gt;use &lt;i&gt;&lt;b&gt;docker stop&lt;/b&gt;&lt;/i&gt;&lt;/sup&gt; </td></tr>
<tr><td>enter     </td><td>opens up a shell cli inside a running container       </td><td>&lt;sup&gt;use &lt;i&gt;&lt;b&gt;docker exec&lt;/b&gt;&lt;/i&gt;&lt;/sup&gt; </td></tr>
<tr><td>launch    </td><td>starts instances on remote platform                   </td><td>available                                </td></tr>
<tr><td>terminate </td><td>removes an instance from a remote platform            </td><td>                                         </td></tr>
<tr><td>connect   </td><td>connects to remote host through ssh                   </td><td>available                                </td></tr>
<tr><td>put       </td><td>copy a file to remote host through scp                </td><td>available                                </td></tr>
<tr><td>get       </td><td>copy a file from remote host through scp              </td><td>available                                </td></tr>
<tr><td>deploy    </td><td>deploys service to a remote platform                  </td><td>available                                </td></tr>
<tr><td>withdrawal</td><td>removes a service from a live remote host             </td><td>                                         </td></tr>
<tr><td>setup     </td><td>creates account resources for a remote platform       </td><td>                                         </td></tr>
<tr><td>teardown  </td><td>removes an account from a remote platform             </td><td>                                         </td></tr>
<tr><td>renew     </td><td>retrieves a new ssl certificate for url endpoint      </td><td>                                         </td></tr>
<tr><td>monitor   </td><td>creates a monitor of services running on remote host  </td><td>                                         </td></tr>
<tr><td>share     </td><td>transfers service credentials through password manager</td><td>                                         </td></tr>
</tbody>
</table>