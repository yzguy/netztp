from flask import render_template
from netztp.util import response_with_content_type
from netztp.opengear import bp
from netztp import inventory

@bp.route('/ztp/mac/<mac>/config.sh')
def ztp_config_mac(mac):
    device = inventory.device(mac)
    return response_with_content_type(render_template('config.j2', device=device),
                                                      'text/plain')
