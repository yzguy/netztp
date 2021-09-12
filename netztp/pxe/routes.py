from flask import request, render_template, current_app, url_for

from netztp.pxe import bp, datastore
from netztp.pxe.datastore import DatastoreExceptionNotFound
from netztp.util import response_with_content_type

@bp.route('/boot')
def boot():
    mac_address = request.args.get('mac')

    try:
        boot = datastore.boot(mac_address)
    except DatastoreExceptionNotFound:
        return response_with_content_type(
                render_template('shell.j2'), 'text/plain')

    try:
        path = {
            'flatcar': url_for('pxe.ignition', mac=mac_address),
            'ubuntu': url_for('pxe.cloud_init', mac=mac_address)
        }[boot]
    except KeyError:
        return response_with_content_type(
                render_template('shell.j2'), 'text/plain')

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
    try:
        ignition = datastore.ignition(mac)
    except DatastoreExceptionNotFound:
        return response_with_content_type(
                render_template('shell.j2'), 'text/plain')

    return response_with_content_type(ignition, 'text/plain')

@bp.route('/cloud-init/<mac>')
def cloud_init(mac):
    return mac

@bp.route('/cloud-init/<mac>/meta-data')
def cloud_init_meta_data(mac):
    try:
        meta_data = datastore.meta_data(mac)
    except DatastoreExceptionNotFound:
        return response_with_content_type(
                render_template('shell.j2'), 'text/plain')

    return response_with_content_type(meta_data, 'text/plain')

@bp.route('/cloud-init/<mac>/user-data')
def cloud_init_user_data(mac):
    try:
        user_data = datastore.user_data(mac)
    except DatastoreExceptionNotFound:
        return response_with_content_type(
                render_template('shell.j2'), 'text/plain')

    return response_with_content_type(user_data, 'text/plain')
