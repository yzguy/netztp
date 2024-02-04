from flask import Blueprint, current_app

bp = Blueprint('cumulus', __name__, static_folder='static',
                                template_folder='templates')

from netztp.cumulus import routes

#option cumulus-provision-url code 239 = text;
#subnet 192.0.2.0 netmask 255.255.255.0 {
#  range 192.0.2.100 192.168.0.200;
#  option cumulus-provision-url "http://ztp.yzguy.net/cumulus/ztp";
# }
