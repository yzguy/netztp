
class Inventory(object):

    DATA = {
        'abc123': {
            'hostname': 'abc123.yzguy.io',
            'ip_address': '192.168.50.200',
            'subnet_mask': '255.255.255.0',
            'gateway': '192.168.50.1'
        },
        '123abc': {
            'hostname': '123abc.yzguy.io',
            'ip_address': '192.168.50.201',
            'subnet_mask': '255.255.255.0',
            'gateway': '192.168.50.1'
        },
        '000c29a0de4d': {
            'hostname': '000c29a0de4d',
            'domain_name': 'yzguy.io',
            'ip_address': '192.168.50.202',
            'subnet_mask': '255.255.255.0',
            'gateway': '192.168.50.1'
        }
    }

    def __init__(self):
        self.api_token = None

    def authenticate(self, api_token):
        self.api_token = api_token

    def device(self, id):
        if id in self.DATA:
            return self.DATA[id]

        return {}
