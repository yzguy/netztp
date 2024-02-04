from flask import request, render_template
from netztp.util import response_with_content_type
from netztp.cumulus import bp

# Process (https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-57/Installation-Management/Zero-Touch-Provisioning-ZTP/)

# GET /cumulus/ztp
@bp.route('/ztp')
def ztp():
    device = {
        'serialnum': request.headers.get('Cumulus-Serial', None),
        'mgmt_mac': request.headers.get('Cumulus-Mgmt-Mac', None),
        'base_mac': request.headers.get('Cumulus-Base-Mac', None),
        'version': request.headers.get('Cumulus-Version', None)
    }

    return response_with_content_type(render_template('ztp.j2', device=device),
                                      'text/plain')
