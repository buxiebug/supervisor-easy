# encoding:utf8
__author__ = 'brianyang'

from config import SERVERS, GROUPS


def get_server_id_mapping():
    return dict([(server.id, server) for server in SERVERS])


def parse_server_config(server, server_dict):
    parts = server.split('.', 1)
    if len(parts) == 1:
        return server_dict.get(server), ''
    else:
        return server_dict.get(parts[0]), parts[1]


def get_group_mapping():
    server_mapping = dict([(server.name, server) for server in SERVERS])
    group_dict = {}

    for group in GROUPS:
        apps = []
        for server_str in group.get('apps'):
            server, app = parse_server_config(server_str, server_mapping)
            apps.append({
                'server': server,
                'name': app
            })
        group_dict[group.get('name')] = apps

    return group_dict


def get_status(group_mapping):
    group_list = []
    for group in group_mapping:
        apps = []
        for app in group_mapping.get(group):
            app_name = app.get('name')
            server = app.get('server')
            if not app_name:
                apps.extend(server.get_all_process_info())
            else:
                apps.append(server.get_process_info(app_name))
        group_list.append((group, apps))
    return group_list


def batch_group_opt(apps, opt):
    flag = True
    for app in apps:
        server = app.get('server')
        name = app.get('name')
        if not name:
            if opt == 'start':
                flag = flag and server.start_all_apps()
            if opt == 'restart':
                flag = flag and server.restart_all_apps()
            if opt == 'stop':
                flag = flag and server.stop_all_apps()
        else:
            if opt == 'start':
                flag = flag and server.start_process(name)
            if opt == 'restart':
                flag = flag and server.restart_process(name)
            if opt == 'stop':
                flag = flag and server.stop_process(name)
    return flag


def batch_server_opt(server, opt):
    if opt == 'start':
        results = server.start_all_apps()
    if opt == 'restart':
        results = server.restart_all_apps()
    if opt == 'stop':
        results = server.stop_all_apps()
    for result in results:
        if result.get('description') != 'OK':
            return False
    return True
