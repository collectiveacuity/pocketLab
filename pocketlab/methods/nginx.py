''' a package of methods to handle nginx configurations '''
__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

def compile_nginx(container_list, domain_name, http_port=80, ssl_port=None, elb=False):
    
    '''
        a method to compile nginx configurations for forwarding to containers
        
    :param container_list: list of dictionaries with domain and port keys 
    :param domain_name: string with name of main domain
    :param http_port: integer with port of incoming http requests
    :param ssl_port: integer with port of incoming ssl requests
    :param elb: boolean to indicate nginx is behind another load-balance
    :return: string with nginx config text
    '''
    
    # http://nginx.org/en/docs/http/server_names.html
    # https://www.linode.com/docs/websites/nginx/how-to-configure-nginx/

# validate inputs
    if ssl_port:
        if not isinstance(ssl_port, int):
            raise ValueError('compile_nginx(ssl_port=%s) must be an integer.' % str(ssl_port))
        
# determine http port destination
    web_port = 80
    for container in container_list:
        if container['domain'] == domain_name:
            web_port = container['port']

# construct default nginx insert    
    nginx_insert = ''
    proxy_headers = ''
    ssl_headers = ''

# determine proxy headers
    if elb:
        proxy_headers = 'proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header Host $http_host; '
        nginx_insert += 'server { listen %s; server_name localhost; location / { proxy_pass http://localhost:%s; } } ' % (http_port, web_port)

# TODO: find nginx syntax for adding ssl reference to request mapping

# construct ssl only properties
    if ssl_port:
        nginx_insert += 'server { listen %s; server_name .%s; rewrite ^ https://$server_name$request_uri? permanent; } ' % (http_port, domain_name)
        nginx_insert += 'server { listen %s default_server; location / { proxy_pass http://localhost:%s; %s} } ' % (http_port, web_port, proxy_headers)
        ssl_listener = ''
        for container in container_list:
            server_details = 'server { listen %s; server_name %s; location / { proxy_pass http://localhost:%s; %s} }' % (ssl_port, container['domain'], container['port'], proxy_headers)
            if ssl_listener:
                ssl_listener += ' '
            ssl_listener += server_details
        ssl_listener += ' server { listen %s; server_name www.%s; return 301 https://%s; }' % (ssl_port, domain_name, domain_name)
        ssl_listener += ' server { listen %s default_server; rewrite ^ https://%s permanent; }' % (ssl_port, domain_name)
        nginx_insert += ssl_listener

# construct http properties
    else:
        open_listener = ''
        for container in container_list:
            server_details = 'server { listen %s; server_name %s; location / { proxy_pass http://localhost:%s; %s} }' % (http_port, container['domain'], container['port'], proxy_headers)
            if open_listener:
                open_listener += ' '
            open_listener += server_details
        open_listener += ' server { listen %s; server_name www.%s; return 301 http://%s; }' % (http_port, domain_name, domain_name)
        open_listener += ' server { listen %s; server_name *.%s; rewrite ^ http://%s permanent; }' % (http_port, domain_name, domain_name)
        open_listener += ' server { listen %s default_server; location / { proxy_pass http://localhost:%s; %s} }' % (http_port, web_port, proxy_headers)
        nginx_insert += open_listener

# construct nginx properties
    nginx_text = 'user nginx; worker_processes auto; events { worker_connections 1024; } pid /var/run/nginx.pid; http { %s }' % nginx_insert
    
    return nginx_text

def extract_containers(nginx_text, domain_name):
    
    container_list = []

# define regex
    import re
    domain_regex = re.compile('server_name\s([\w\.\-]*%s);\slocation\s/\s\{\sproxy_pass\shttp://localhost:(\d+);' % domain_name)

# search for matches
    domain_search = domain_regex.findall(nginx_text)
    if domain_search:
        print(domain_search)
        for match in domain_search:
            name = match[0]
            port = int(match[1])
            container_list.append({'domain': name, 'port': port})
    
    return container_list

if __name__ == '__main__':
    
    container_list = [ { 'domain': 'collectiveacuity.com', 'port': 5000 } ]
    domain_name = 'collectiveacuity.com'
    nginx_text = compile_nginx(container_list, domain_name)
    assert nginx_text.find('listen 80; server_name collectiveacuity.com;') > -1
    
    nginx_text = compile_nginx(container_list, domain_name, ssl_port=443)
    assert nginx_text.find('rewrite ^ https://$server_name$request_uri?') > -1
    
    container_list.append({'domain': 'api.collectiveacuity.com', 'port': 5001})
    nginx_text = compile_nginx(container_list, domain_name, ssl_port=443)
    new_list = extract_containers(nginx_text, domain_name)
    for i in range(len(container_list)):
        assert container_list[i] == new_list[i]
    
