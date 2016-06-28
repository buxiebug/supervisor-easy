# supervisor-easy
## Manage supervisor in a easy way!

[Supervisor](https://github.com/Supervisor/supervisor) is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.

Supervisor provides a web tool to manage programs which looks like ![](http://ww3.sinaimg.cn/large/b8b708a7gw1f5b87cx8nij20mm07k3zl
)

But its default tool just supports single node. Maybe we have hundreds of mechines to deploy out applications using supervisor. 
If we manage these machines one by one, it's a horrible day.

This tool is developed to manage distributed applications centrally.The module used are:
- Flask  web server
- bootstrap + jquery UI

The main features are:
- Easy to deploy:

No need to install other modules like: db, redis ... . Just install Flask and clone the project.Edit config.py to custom your application.

- Group your applications by function or anything what you want.Just edit config.py

A group contains some applications running on same or different servers. You can make operations such as start, stop ,restart on any group.It is useful for batch management.

![](http://ww3.sinaimg.cn/large/b8b708a7gw1f5b8krfyrcj219b0da77l)

- Show all configured hosts and their applications

Show all hosts and theri applications configured in config.py. You can also make batch operations to the host.

![](http://ww3.sinaimg.cn/large/b8b708a7gw1f5b8n8i0t3j21990cb77r)

##Usage
- git clone https://github.com/trytofix/supervisor-easy.git
- edit config.py
```
from Server import Server

SERVERS = [
    Server(
        name='celery1',
        host='127.0.0.1',
        port=12345,
        user='admin',
        password='admin'
    ),
    Server(
        name='celery2',
        host='remote.supervisor.com',
        port=12345,
        user='admin',
        password='admin'
    )
]

GROUPS = [
    {
        'name': 'celery',
        'apps': ['celery1.test:celery', 'celery2.test:celery']
    },
    {
        'name': 'flower',
        'apps': ['celery1.flower']
    }
]
```
As showns below, SERVERS is a list of servers. A server is a supervisor instance.The name attribute is used to identify a server.

> Notice: The name attribute must be unique!

Here is a supervisor sample conf file:
```
[program:test]
command=celery -A main worker -l info -Ofair -Q test

directory=/home/q/celeryTest
user=brianyang
numprocs=1
stdout_logfile=/var/log/common.log
stderr_logfile=/var/log/common_err.log
autostart=true
autorestart=true
startsecs=10

killasgroup=true

priority=1000

[group:test]
programs=celery,test
```

- *GROUPS* is defined to classify applications as you wish. Attribute name is used to name the group. 
- *apps* is a list of applications. 
- Every string in 'apps' is defined as `server_name.group_name:application_name`. 
- *application_name* correspond to 'test' in '[program:test]' in the supervisord.conf. 
- *group_name* correspond to 'test' in '[group:test]'  in the supervisord.conf.
- *server_name* is the custom name defined for the Server such as 'celery1' in 'Server(name='celery1'....

## Run: python webui.py to test your application.
> Don't use `python webui.py` to your product environment。 A better way is to choose a uwsgi server to deploy your application. Such as uwsgi.

## Todos
- Performance Imporve
- UI Improve
- Exception Handling

