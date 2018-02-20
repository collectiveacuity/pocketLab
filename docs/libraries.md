# Libraries
Configuration Settings for Third-Party Libraries

## [Nginx](https://nginx.org/en/docs/)
_A Reverse Proxy Server_  
  
**Installation on EC2:**    
```bash

```

**Modification:** 
```bash
nano /etc/nginx/nginx.conf
sudo service nginx restart
```

**Troubleshooting:**  


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
$ exit
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
A. Due to updates to certbot, python modules may be missing from installation:
```bash
$ sudo su -
$ pip install -U pip
$ /root/.local/share/letsencrypt/bin/pip install {missing module}
```
B. Due to 32bit / 64 bit issues, python venv libs may need to be copied:
```bash
$ sudo su -
$ \cp -r /opt/eff.org/certbot/venv/lib64/* /opt/eff.org/certbot/venv/lib/
$ exit
```

## [Keytool](https://docs.oracle.com/javase/8/docs/technotes/tools/windows/keytool.html)
_A Keystore Generator for Self-Signed SSL Trust Rings_

**Create Folder for Keys:**
```bash
mkdir keys
cd keys
```

**Generate Root RSA Key:**
```bash
openssl req -newkey rsa:2048 -x509 -nodes -keyout root.key \
 -out root.crt -days 36500 -passout pass:mysecretpassword \
 -subj /CN=root/OU=None/O=None/L=None/C=None
```

**Generate Node Key:**
```bash
keytool -genkey -keyalg RSA -alias 123.456.789.0 \
 -validity 36500 -keystore 123.456.789.0.jks \
 -storepass mysecretpassword -keypass mysecretpassword -keysize 4096 \
 -dname "CN=123.456.789.0, OU=None, O=None, L=None, C=None"
keytool -importkeystore -srckeystore 123.456.789.0.jks \
 -destkeystore 123.456.789.0.jks -deststoretype pkcs12 \
 -storepass mysecretpassword -keypass mysecretpassword
```

**Generate Cert Request:**
```bash
keytool -certreq -alias 123.456.789.0 -file 123.456.789.0.csr \
 -keystore 123.456.789.0.jks -storepass mysecretpassword -keypass mysecretpassword \
 -dname "CN=123.456.789.0, OU=None, O=None, L=None, C=None"
```

**Sign Cert with Root Cert:**
```bash
openssl x509 -req -CA root.crt -CAkey root.key \
 -in 123.456.789.0.csr -out 123.456.789.0.crt -days 36500 \
 -CAcreateserial -passin pass:mysecretpassword
```

**Add Certs to Node Keystore:**
```bash
keytool -importcert -keystore 123.456.789.0.jks -alias root \
 -file root.crt -noprompt -keypass mysecretpassword -storepass mysecretpassword
keytool -importcert -keystore 123.456.789.0.jks \
 -alias 123.456.789.0 -file 123.456.789.0.crt -noprompt \
 -keypass mysecretpassword -storepass mysecretpassword
```

**Add Root Cert to Truststore:**
```bash
keytool -importcert -keystore truststore.jks -alias root \
 -file root.crt -noprompt -keypass mysecretpassword -storepass mysecretpassword
```

**Add Node Certs to Truststore (for each node):**
```bash
keytool -importcert -keystore truststore.jks \
 -alias 123.456.789.0 -file 123.456.789.0.crt -noprompt \
 -keypass mysecretpassword -storepass mysecretpassword
```

**Verify Certificates:**
```bash
openssl x509 -in root.crt -text -noout
keytool -list -keystore 123.456.789.0.jks -storepass mysecretpassword
openssl verify -CAfile root.crt 123.456.789.0.crt
keytool -list -keystore truststore.jks -storepass mysecretpassword
```

**Generate PEM Files:**
```bash
openssl pkcs12 -in 123.456.789.0.jks -nokeys \
 -out 123.456.789.0.cer.pem -passin pass:mysecretpassword
openssl pkcs12 -in 123.456.789.0.jks -nodes  \
 -nocerts -out 123.456.789.0.key.pem -passin pass:mysecretpassword
```

**Generate Certificate Chain:**
```bash
cat root.crt 123.456.789.0.crt > 123.456.789.0.chain
```

