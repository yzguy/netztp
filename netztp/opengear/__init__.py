from flask import Blueprint

bp = Blueprint('opengear', __name__, template_folder='templates')

from netztp.opengear import routes

# https://opengear.zendesk.com/hc/en-us/articles/216376503-Zero-Touch-Provisioning-ZTP-automating-config-and-firmware-using-DHCP

# option space opengear code width 1 length width 1;
# option opengear.config-url code 1 = text;
# option opengear.firmware-url code 2 = text;
#
# class "OPENGEAR" {
#   match if option vendor-class-identifier ~~ "^Opengear/";
#   vendor-option-space opengear;
#   option opengear.config-url "http://ztp.yzguy.io:5000/opengear/ztp/mac/${mac}/config.sh";
#   option opengear.firmware-url "http://ztp.yzguy.io:5000/firmware/${class}.flash";
# }
