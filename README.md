# scholarmail

A tool for converting Google Scholar alerting emails to html page.

The Google Scholar provide a convenient alerting service that can push the latest scholar publication to your email. However, you would need to open each email to watch. This tool can fetch all received scholar emails and automatically generate a web page for you.


## Setup

**scholarmail** is available on PyPI:

```console
$ pip install scholarmail
```

Make a configure file

```console
$ pip touch config.json
```

Edit the content like:
```json
{  
    "email": "your_name@gmail.com",  
    "passkey": "your_passkey_of_imap_service",  
    "server": "imap.gmail.com",  
    "port": 993,  
    "remove_mail": 1,  
    "apply_filter": 1,  
    "proxy": 1,  
    "proxy_ip": "127.0.0.1",  
    "proxy_port": 7890,  
    "filter_list": [  
        "keyword1",  
        "keyword2"  
    ]  
}  
```