from flask import request, render_template, current_app, url_for, \
        abort
from netztp.pxe import bp
from netztp.util import response_with_content_type

import os, yaml, git

@bp.errorhandler(404)
def page_not_found(e):
    return response_with_content_type(
            render_template('shell.j2'), 'text/plain')

@bp.route('/boot')
def boot():
    mac_address = request.args.get('mac')

    try:
        boot_path = os.path.join(bp.static_folder, 'boot.json')
        with open(boot_path, 'r') as fd:
            boot_data = yaml.full_load(fd)
    except FileNotFoundError:
        abort(404)

    if mac_address not in boot_data:
        abort(404)

    try:
        path = {
            'flatcar': url_for('pxe.ignition', mac=mac_address),
            'ubuntu': url_for('pxe.cloud_init', mac=mac_address)
        }[boot_data[mac_address]]
    except KeyError:
        abort(404)

    firmware_server = current_app.config['FIRMWARE_SERVER']
    config_url = '{}{}'.format(request.host_url, path.lstrip('/'))

    return response_with_content_type(
            render_template('boot.j2',
                boot=boot,
                firmware_server=firmware_server,
                config_url=config_url,
                mac_address=mac_address
            ), 'text/plain')

@bp.route('/ignition/<mac>')
def ignition(mac):
    file = bp.send_static_file(f'ignition/{mac}')
    return response_with_content_type(file, 'text/plain')

@bp.route('/cloud-init/<mac>')
def cloud_init(mac):
    return mac

@bp.route('/cloud-init/<mac>/meta-data')
def cloud_init_meta_data(mac):
    file = bp.send_static_file(f'cloud-init/{mac}/meta-data')
    return response_with_content_type(file, 'text/plain')

@bp.route('/cloud-init/<mac>/user-data')
def cloud_init_user_data(mac):
    file = bp.send_static_file(f'cloud-init/{mac}/user-data')
    return response_with_content_type(file, 'text/plain')

@bp.route('/refresh')
def refresh():
    repo = git.Repo(bp.static_folder)
    repo.remotes.origin.pull('master')
    return repo.head.object.hexsha
