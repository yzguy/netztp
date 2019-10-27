from netztp.util import response_with_content_type
from netztp.opengear import bp

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
    return response_with_content_type(configuration_script.format(
        ip_address='192.168.50.100',
        subnet_mask='255.255.255.0',
        gateway='192.168.50.1',
        hostname='opengear'
    ), 'text/plain')
