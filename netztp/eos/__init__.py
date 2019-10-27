from flask import Blueprint

bp = Blueprint('eos', __name__, static_folder='static')

from netztp.eos import routes

# class "ARISTA" {
#   match if substring(option vendor-class-identifier, 0, 6) = "Arista";
#   option bootfile-name "http://ztp.yzguy.io:5000/eos/ztp/bootstrap";
# }
