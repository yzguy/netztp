from flask import make_response, jsonify, request, url_for, redirect
from app.eos.util import response_with_content_type, generate_checksum
from app.eos import bp

from datetime import datetime

startup_config = '''
hostname veos.lab
ip domain-name yzguy.io
!
username admin privilege 15 role network-admin secret admin
end
'''

log_destination = {
    'destination': '192.168.50.2:514',
    'level': 'DEBUG'
}

# First Step: DHCP tells EOS to request bootstrap
@bp.route('/ztp/bootstrap')
def ztp_bootstrap():
    # TODO: Need to replace $SERVER dynamically
    file = bp.send_static_file('bootstrap')
    return response_with_content_type(file, 'text/x-python')

# Second Step: Bootstrap tells EOS to request config
@bp.route('/ztp/bootstrap/config')
def ztp_bootstrap_config():
    return jsonify({})
    #return jsonify({
    #   'xmpp': {},
    #   'logging': [log_destination]
    #})

# Third Step: EOS POSTs information
@bp.route('/ztp/nodes', methods=['POST'])
def ztp_nodes():
    # vEOS does not have serial number
    '''
    {
    	"neighbors": {
    		"Management1": [{
    			"device": "b4fb.e488.56de",
    			"port": "0/6"
    		}]
    	},
    	"version": "4.21.8M",
    	"systemmac": "00:0c:29:a0:de:4d",
    	"model": "vEOS",
    	"serialnumber": ""
    }
    '''
    # Lookup device by serial number
    # If no device is found, lookup by MAC Address
    serialnum = request.json['serialnumber']
    if not serialnum:
        serialnum = request.json['systemmac'].replace(':', '')
    return redirect(url_for('eos.ztp_nodes_serial', serialnum=serialnum)), 409

# Fourth Step: We give EOS actions to do, actions are from ztpserver
# install_image - download and install specific firmware
# replace_config - download and install configuration
# copy_file - download and save file
@bp.route('/ztp/nodes/<serialnum>')
def ztp_nodes_serial(serialnum):
    # Look for Device

    actions = []

    # If not device, return unknown/no actions
    # return jsonify({
    #     'name': 'Unknown Device',
    #     'actions': []
    # }), 404

    # Upgrade Software Action
    actions.append({
        'name': 'Upgrade Operating System',
        'action': 'install_image',
        'attributes': {
            'url': 'http://192.168.50.74:8000/firmware/vEOS-lab-4.22.2.1F.swi',
            'version': '4.22.2.1F'
        },
        'always_execute': True
    })
    # Get rendered configuration
    actions.append({
        'name': 'Install static startup-config file',
        'action': 'replace_config',
        'attributes': {
            'url': '/nodes/{}/startup-config'.format(serialnum)
        },
        'always_execute': True
    })
    # ZTP Finished Action
    actions.append({
        'name': 'Signal ZTP Completion',
        'action': 'copy_file',
        'attributes': {
            'src_url': '/{}/ztp_finished'.format(serialnum),
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

# Node retrieves install_image action file
@bp.route('/ztp/actions/install_image')
def ztp_actions_install_image():
    file = bp.send_static_file('actions/install_image')
    return response_with_content_type(file, 'text/x-python')

# Node retrieves replace_config action file
@bp.route('/ztp/actions/replace_config')
def ztp_actions_replace_config():
    file = bp.send_static_file('actions/replace_config')
    return response_with_content_type(file, 'text/x-python')

# Node retreives device-specific startup-config
@bp.route('/ztp/nodes/<serialnum>/startup-config')
def ztp_startup_config(serialnum):
    return response_with_content_type(startup_config, 'text/plain')

# Node retrieves checksum for startup-config
@bp.route('/ztp/meta/nodes/<serial>/startup-config')
def meta_serial_startup_config(serial):
    return jsonify(generate_checksum(startup_config))

# Node retrieves copy_file action file
@bp.route('/ztp/actions/copy_file')
def ztp_actions_copy_file():
    file = bp.send_static_file('actions/copy_file')
    return response_with_content_type(file, 'text/x-python')

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
