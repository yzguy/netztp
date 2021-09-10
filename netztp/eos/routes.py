from flask import make_response, jsonify, request, url_for, redirect, abort, \
    render_template, current_app
from netztp.util import response_with_content_type, generate_checksum
from netztp import inventory as inv
from netztp.eos import bp

from datetime import datetime
import os

bash_commands = '''
FastCli -p 15 -c "
extension Aboot-patch-419257.i686.rpm"
'''

cli_commands = ''

# Process (https://ztpserver.readthedocs.io/en/master/api.html)
# GET /eos/ztp/bootstrap HTTP/1.1 200 -
# GET /eos/ztp/bootstrap/config HTTP/1.1 200 -
# POST /eos/ztp/nodes HTTP/1.1 201 -
# GET /eos/ztp/nodes/<serial> HTTP/1.1 200 -
# GET /eos/ztp/actions/install_image HTTP/1.1 200 -
# GET /firmware/<firmware> HTTP/1.1 200
# GET /eos/ztp/actions/replace_config HTTP/1.1 200 -
# GET /eos/ztp/nodes/<serial>/startup-config HTTP/1.1 200 -
# GET /eos/ztp/meta/nodes/<serial>/startup-config HTTP/1.1 200 -
# GET /eos/ztp/actions/copy_file HTTP/1.1 200 -
# GET /eos/ztp/<serial>/ztp_finished HTTP/1.1 200 -
# GET /eos/ztp/meta/<serial>/ztp_finished HTTP/1.1 200 -


# First Step: DHCP tells EOS to request bootstrap
@bp.route('/ztp/bootstrap')
def ztp_bootstrap():
    # TODO: Need to replace $SERVER dynamically
    file = bp.send_static_file('bootstrap')
    return response_with_content_type(file, 'text/x-python')

# Second Step: Bootstrap tells EOS to request config
@bp.route('/ztp/bootstrap/config')
def ztp_bootstrap_config():
    #return jsonify({})
    return jsonify({
      'xmpp': {},
      'logging': current_app.config['LOG_DESTINATIONS']
    })

# Third Step: EOS POSTs information
@bp.route('/ztp/nodes', methods=['POST'])
def ztp_nodes():
    # vEOS does not have serial number
    # {
    # 	"neighbors": {
    # 		"Management1": [{
    # 			"device": "b4fb.e488.56de",
    # 			"port": "0/6"
    # 		}]
    # 	},
    # 	"version": "4.21.8M",
    # 	"systemmac": "00:0c:29:a0:de:4d",
    # 	"model": "vEOS",
    # 	"serialnumber": ""
    # }

    # Lookup device by serial number
    # If no device is found, lookup by MAC Address
    serialnum = request.json['serialnumber']
    if not serialnum:
        serialnum = request.json['systemmac'].replace(':', '')
    return redirect(url_for('eos.ztp_nodes_serial', serialnum=serialnum)), 201

# Fourth Step: We give EOS actions to do, actions are from ztpserver
# install_image - download and install specific firmware
# replace_config - download and install configuration
# copy_file - download and save file
@bp.route('/ztp/nodes/<serialnum>')
def ztp_nodes_serial(serialnum):
    actions = []

    device = inv.device(serialnum)
    # Look for Device
    if not device:
        return jsonify({
            'name': 'Unknown Device',
            'actions': []
        }), 404

    # Get firmware version from inventory or use default
    eos_versions = current_app.config['EOS_VERSIONS']
    version = device.custom_fields['firmware']
    if not version:
        version = eos_versions['default']
    filename = eos_versions[version]

    # Upgrade Software Action
    actions.append({
        'name': 'Upgrade Operating System',
        'action': 'install_image',
        'attributes': {
            'url': f"{current_app.config['FIRMWARE_SERVER']}/eos/{filename}",
            'version': version
        },
        'always_execute': True
    })

    # # Install Aboot extension
    # actions.append({
    #     'name': 'Install Aboot extension',
    #     'action': 'install_extension',
    #     'attributes': {
    #         'url': 'http://192.168.50.74:8000/firmware/Aboot-patch-419257.i686.rpm',
    #     },
    #     'always_execute': True
    # })
    #
    # # Actually Install Aboot extension
    # actions.append({
    #     'name': 'Actually Install Aboot extension',
    #     'action': 'run_bash_script',
    #     'attributes': {
    #         'url': '/bash_commands'
    #     },
    #     'always_execute': True
    # })

    # Get rendered configuration
    actions.append({
        'name': 'Install static startup-config file',
        'action': 'replace_config',
        'attributes': {
            'url': f'/nodes/{serialnum}/startup-config'
        },
        'always_execute': True
    })

    # ZTP Finished Action
    actions.append({
        'name': 'Signal ZTP Completion',
        'action': 'copy_file',
        'attributes': {
            'src_url': f'/{serialnum}/ztp_finished',
            'dst_url': '/mnt/flash',
            'mode': '0644',
            'overwrite': 'replace'
        },
        'always_execute': True
    })

    # JSON Out
    return jsonify({
        'name': 'Autogenerated definition',
        'actions': actions
    })

# Node retrieves specific action file
@bp.route('/ztp/actions/<action>')
def ztp_actions_all(action):
    actions = os.listdir(os.path.join(bp.static_folder, 'actions'))
    if action in actions:
        file = bp.send_static_file(f'actions/{action}')
        return response_with_content_type(file, 'text/x-python')

    return 'Action not found', 404

@bp.route('/ztp/bash_commands')
def ztp_bash_commands():
    return response_with_content_type(bash_commands, 'text/plain')

@bp.route('/ztp/cli_commands')
def ztp_cli_commands():
    return response_with_content_type(cli_commands, 'text/plain')

# Node retreives device-specific startup-config
@bp.route('/ztp/nodes/<serialnum>/startup-config')
def ztp_startup_config(serialnum):
    device = inv.device(serialnum)
    return response_with_content_type(render_template('eos.j2', device=device),
                                      'text/plain')

# Node retrieves checksum for startup-config
@bp.route('/ztp/meta/nodes/<serialnum>/startup-config')
def meta_serial_startup_config(serialnum):
    device = inv.device(serialnum)
    return jsonify(generate_checksum(render_template('eos.j2', device=device)))

# Node retrieves the time it finished ZTP
@bp.route('/ztp/<serialnum>/ztp_finished')
def ztp_serial_ztp_finished(serialnum):
    # TODO: send ZTP finish time. Need to make it persistent across requests
    #now = datetime.now().strftime('%F %T')
    return response_with_content_type('finished', 'text/plain')

# Node retrieves checksum for ZTP finish time
@bp.route('/ztp/meta/<serialnum>/ztp_finished')
def meta_serial_ztp_finished(serialnum):
    return jsonify(generate_checksum('finished'))
