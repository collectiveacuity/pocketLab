''' a package of methods to handle nginx configurations '''
__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

def compile_nginx(container_list, domain_name, http_port=80, ssl_port=None, ssl_gateway=''):
    
    '''
        a method to compile nginx configurations for forwarding to containers
        
    :param container_list: list of dictionaries with domain and port keys 
    :param domain_name: string with name of main domain
    :param http_port: integer with port of incoming http requests
    :param ssl_port: integer with port of incoming ssl requests
    :param ssl_gateway: string with name of ssl gateway connecting nginx to internet
    :return: string with nginx config text
    '''
    
    # http://nginx.org/en/docs/http/server_names.html
    # https://www.linode.com/docs/websites/nginx/how-to-configure-nginx/

# validate inputs
    if ssl_port:
        if not isinstance(ssl_port, int):
            raise ValueError('compile_nginx(ssl_port=%s) must be an integer.' % str(ssl_port))
        if not ssl_gateway:
            raise ValueError('compile_nginx(ssl_port=%s) requires an ssl_gateway argument.' % str(ssl_port))
    supported_gateways = ['elb', 'certbot']
    if ssl_gateway and not ssl_gateway in supported_gateways:
        from labpack.parsing.grammar import join_words
        gateway_text = join_words(supported_gateways, operator='disjunction')
        raise ValueError('compile_nginx(ssl_gateway=%s) must be either %s.' % (ssl_gateway, gateway_text))
        
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
    if ssl_gateway == 'elb':
        proxy_headers = 'proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header Host $http_host; '
        nginx_insert += 'server { listen %s; server_name localhost; location / { proxy_pass http://localhost:%s; } } ' % (http_port, web_port)
    elif ssl_gateway == 'certbot':
        ssl_headers = 'ssl_certificate "/etc/letsencrypt/live/%s/fullchain.pem";' % domain_name
        ssl_headers += ' ssl_certificate_key "/etc/letsencrypt/live/%s/privkey.pem";' % domain_name
        ssl_headers += ' ssl_session_cache shared:SSL:1m;'
        ssl_headers += ' ssl_session_timeout 10m;'
        ssl_headers += ' ssl_protocols TLSv1 TLSv1.1 TLSv1.2;'
        ssl_headers += ' ssl_ciphers HIGH:SEED:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!RSAPSK:!aDH:!aECDH:!EDH-DSS-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA:!SRP;'
        ssl_headers += ' ssl_prefer_server_ciphers on;'

# TODO: find nginx syntax for adding ssl reference to request mapping

# construct ssl only properties
    if ssl_port and ssl_gateway:
        nginx_insert += 'server { listen %s; server_name %s; rewrite ^ https://$server_name$request_uri? permanent; } ' % (http_port, domain_name)
        nginx_insert += 'server { listen %s default_server; location / { proxy_pass http://localhost:%s; %s} } ' % (http_port, web_port, proxy_headers)
        ssl_listener = ''

    # add ssl for each container subdomain
        for container in container_list:
            server_details = ''
            if ssl_gateway == 'elb':
                server_details = 'server { listen %s; server_name %s; location / { proxy_pass http://localhost:%s; %s} }' % (ssl_port, container['domain'], container['port'], proxy_headers)
            elif ssl_gateway == 'certbot':
                server_details = 'server { listen %s ssl; server_name %s; %s location / { proxy_pass http://localhost:%s; } }' % (ssl_port, container['domain'], ssl_headers, container['port'])
            if ssl_listener:
                ssl_listener += ' '
            ssl_listener += server_details
    
    # add redirection for all other subdomains
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
    server_regex = re.compile('server\s\{.*?(?=server\s\{)', re.S)
    domain_regex = re.compile('server_name\s([\w\.\-]*%s);.*?\slocation\s/\s\{\sproxy_pass\shttp://localhost:(\d+);' % domain_name, re.S)

# search for matches
    server_search = server_regex.findall(nginx_text)
    if server_search:
        for server_text in server_search:
            domain_search = domain_regex.findall(server_text)
            if domain_search:
                for match in domain_search:
                    name = match[0]
                    port = int(match[1])
                    container_list.append({'domain': name, 'port': port})
    
    return container_list

if __name__ == '__main__':

# test open domains
    container_list = [ { 'domain': 'collectiveacuity.com', 'port': 5000 } ]
    domain_name = 'collectiveacuity.com'
    nginx_text = compile_nginx(container_list, domain_name)
    assert nginx_text.find('listen 80; server_name collectiveacuity.com;') > -1
    new_list = extract_containers(nginx_text, domain_name)
    for i in range(len(container_list)):
        assert container_list[i] == new_list[i]

# test ssl with elb
    nginx_text = compile_nginx(container_list, domain_name, ssl_port=443, ssl_gateway='elb')
    assert nginx_text.find('rewrite ^ https://$server_name$request_uri?') > -1   

# test multiple domains on elb
    container_list.append({'domain': 'api.collectiveacuity.com', 'port': 5001})
    nginx_text = compile_nginx(container_list, domain_name, ssl_port=443, ssl_gateway='elb')
    nginx_readable = nginx_text.replace(';', ';\n').replace('}', '}\n').replace('{', '{\n')
    new_list = extract_containers(nginx_text, domain_name)
    for i in range(len(container_list)):
        assert container_list[i] == new_list[i]

# test multiple domains on certbot
    nginx_text = open('../../../cred/conf/nginx.conf').read()
    nginx_text = compile_nginx(container_list, domain_name, ssl_port=443, ssl_gateway='certbot')
    nginx_readable = nginx_text.replace(';', ';\n').replace('}', '}\n').replace('{', '{\n')
    new_list = extract_containers(nginx_text, domain_name)
    for i in range(len(container_list)):
        assert container_list[i] == new_list[i]

