# Roadmap

## Components
<table>
<thead>
<tr><th>Name           </th><th> Description                                          </th><th> Status  </th></tr>
</thead>
<tbody>
<tr><td>smtp key       </td><td>create a password key for email client smtp forwarding</td><td>done     </td></tr>
<tr><td>sending domain </td><td>retrieve spf and dkim records from smtp host          </td><td>         </td></tr>
<tr><td>DNS update     </td><td>add spf and dkim records from smtp host to DNS record </td><td>         </td></tr>
<tr><td>Send-from alias</td><td>register smtp host login details with email client    </td><td>         </td></tr>
</tbody>
</table>

## Roadmap Help
The generate.py script in docs_dev uses entries in docs_dev/components.csv and the template file docs_dev/roadmap.md to automatically generate the roadmap page. If you wish to update the roadmap page, make changes to the roadmap template file in docs_dev and edit the entries in the components file using your favorite csv editor. Then run generate.py to update those changes to the official page in the docs folder.
NOTE: If you make changes to docs/roadmap.md, they will be overwritten whenever you run generate.py
