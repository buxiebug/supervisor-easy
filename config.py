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
