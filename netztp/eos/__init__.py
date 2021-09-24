from flask import Blueprint, current_app

from netztp.inventory import Inventory

bp = Blueprint('eos', __name__, static_folder='static',
                                template_folder='templates')

inventory = Inventory(current_app.config['INVENTORY_API_TOKEN'])

from netztp.eos import routes

# class "ARISTA" {
#   match if substring(option vendor-class-identifier, 0, 6) = "Arista";
#   option bootfile-name "http://ztp.yzguy.io:5000/eos/ztp/bootstrap";
# }
