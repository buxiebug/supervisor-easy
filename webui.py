# encoding:utf8
__author__ = 'brianyang'

import json

from flask import Flask, render_template, Response

from supervisor_manage import get_status, get_server_id_mapping, get_group_mapping, batch_group_opt, batch_server_opt

app = Flask(__name__)

server_id_mapping = get_server_id_mapping()
group_mapping = get_group_mapping()


def common_response(ret):
    return Response(json.dumps({'ret': ret}), content_type='application/json')


@app.route('/')
def index():
    return render_template('index.html', apps=get_status(group_mapping))


@app.route('/servers/')
def servers():
    return render_template('servers.html', servers=server_id_mapping.values())


@app.route('/server/<server_id>/status/')
def server_status(server_id):
    server = server_id_mapping.get(server_id)
    uri = '%s@%s:%s' % (server.user, server.host, server.port)
    return render_template('server_status.html', uri=uri, server_id=server_id, apps=server.get_all_process_info())


@app.route('/<server_id>/<group>/<app>/start/')
def start_app(server_id, group, app):
    app_name = '%s:%s' % (group, app)
    return common_response(server_id_mapping.get(server_id).start_process(app_name))


@app.route('/<server_id>/<group>/<app>/restart/')
def restart_app(server_id, group, app):
    app_name = '%s:%s' % (group, app)
    return common_response(server_id_mapping.get(server_id).restart_process(app_name))


@app.route('/<server_id>/<group>/<app>/stop/')
def stop_app(server_id, group, app):
    app_name = '%s:%s' % (group, app)
    return common_response(server_id_mapping.get(server_id).stop_process(app_name))


def format_log(log):
    return '<div>%s</div>' % (log,)


@app.route('/<server>/<group>/<app>/tail/')
def tail_std_log(server, group, app):
    app_name = '%s:%s' % (group, app)
    return Response(server_id_mapping.get(server).tail_log(app_name, format_log))


@app.route('/group_batch/<group>/<opt>/')
def group_batch(group, opt):
    return common_response(batch_group_opt(group_mapping.get(group, []), opt))


@app.route('/server_batch/<server_id>/<opt>/')
def server_batch(server_id, opt):
    return common_response(batch_server_opt(server_id_mapping.get(server_id), opt))


if __name__ == '__main__':
    app.run(debug=True)
