from flask import request, render_template, current_app, url_for, \
        abort, json
from netztp.pxe import bp
from netztp.util import response_with_content_type

import os, git

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
            boot_data = json.load(fd)
    except FileNotFoundError:
        abort(404)

    try:
        boot = boot_data[mac_address]
    except KeyError:
        try:
            boot = boot_data['default']
        except KeyError:
            abort(404)

    try:
        path = {
            'flatcar': url_for('pxe.ignition_install', mac=mac_address),
            'ubuntu2004': url_for('pxe.cloud_init', mac=mac_address),
            'ubuntu2204': url_for('pxe.cloud_init', mac=mac_address),
            'debian11': url_for('pxe.preseed', mac=mac_address),
            'proxmox72': '/',
            'proxmox73': '/',
            'vyos132': '/'
        }[boot['image']]
    except KeyError:
        abort(404)

    firmware_server = current_app.config['FIRMWARE_SERVER']
    config_url = '{}{}'.format(request.host_url, path.lstrip('/'))

    return response_with_content_type(
            render_template('boot.j2',
                boot=boot['image'],
                firmware_server=firmware_server,
                config_url=config_url,
                mac_address=mac_address
            ), 'text/plain')

@bp.route('/ignition/<mac>/install')
def ignition_install(mac):
    try:
        install_path = os.path.join(bp.static_folder, 'ignition', 'install')
        with open(install_path, 'r') as fd:
            install_data = json.load(fd)
    except FileNotFoundError:
        abort(404)

    path = url_for('pxe.ignition', mac=mac)
    config_url = '{}{}'.format(request.host_url, path.lstrip('/'))

    install_data['storage']['files'][0]['contents']['source'] = config_url

    return response_with_content_type(install_data, 'application/json')

@bp.route('/ignition/<mac>/config')
def ignition(mac):
    file = bp.send_static_file(f'ignition/hosts/{mac}')
    return response_with_content_type(file, 'application/json')

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

@bp.route('/preseed/<mac>')
def preseed(mac):
    file = bp.send_static_file(f'preseed/{mac}')
    return response_with_content_type(file, 'text/plain')

@bp.route('/refresh')
def refresh():
    branch = request.args.get('branch', default='master')

    repo = git.Repo(bp.static_folder)

    # Fetch from remote
    repo.remotes.origin.fetch()

    # checkout branch and get latest
    repo.git.checkout(branch)
    repo.remotes.origin.pull(branch)

    return render_template('git.j2', repo=repo)
