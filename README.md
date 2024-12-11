### Basic start

-   Install docker and docker-compose
-   `docker-compose build`
-   `docker-compose up`


### How to use GPU?

If you want to enable GPU in docker container to assist Ollama with computation, you need to activate following code in docker-compose.yml
```
# deploy:
#   resources:
#     reservations:
#       devices:
#       - driver: nvidia
#         count: 1
#         capabilities: [gpu]
```

### How to Deploy on EC2 using NGINX?

- go to folder `cd /etc/nginx/sites-enabled`
- create new file (exmample `sudo torch test_ssl`)
    ``` text
    server  {
        listen 80;
        server_name {your ip aws}; (example : 00.000.00.000)
        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }
    ```


### How to have DNS?
 - go to [epik](https://registrar.epik.com/domain/portfolio)

### How to setting https?
 - go to link `https://manage.sslforfree.com/certificates`
 - Document how to install on nginx is [Here](https://help.zerossl.com/hc/en-us/articles/360058295894-Installing-SSL-Certificate-on-NGINX)
 - `cat certificate.crt ca_bundle.crt >> certificate.crt`
 - install file on your project (exammple : `{example_foldername}`)
 ``` bash
    server {

        listen               443 ssl;

        ssl                  on;
        ssl_certificate      /home/ubuntu/fastapi/{example_foldername}/certificate.crt;
        ssl_certificate_key  /home/ubuntu/fastapi/{example_foldername}/private.key;


        server_name  {example_foldername};
        access_log   /var/log/nginx/nginx.vhost.access.log;
        error_log    /var/log/nginx/nginx.vhost.error.log;

        location / {
                proxy_pass http://127.0.0.1:8000;
        }
    }

 ```