from netztp.util import response_with_content_type
from netztp.opengear import bp
from netztp import inventory

configuration_script = '''!/bin/bash

# Configure networking
config -s config.interfaces.wan.mode=static
config -s config.interfaces.wan.address={ip_address}
config -s config.interfaces.wan.netmask={subnet_mask}
config -s config.interfaces.wan.gateway={gateway}

# Configure hostname
config -s config.system.name={hostname}

# Schedule configurators and reboot
touch /etc/config/.run_configurators
reboot
'''

@bp.route('/ztp/mac/<mac>/config.sh')
def ztp_config_mac(mac):
    device = inventory.device(mac)
    return response_with_content_type(configuration_script.format(
        ip_address=device['ip_address'],
        subnet_mask=device['subnet_mask'],
        gateway=device['gateway'],
        hostname=device['hostname']
    ), 'text/plain')
