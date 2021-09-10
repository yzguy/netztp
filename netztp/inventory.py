
import pynetbox, os

class Inventory(object):
    def __init__(self):
        netbox = pynetbox.api(
            os.getenv('NETBOX_URL'),
            token=os.getenv('NETBOX_TOKEN'),
            threading=True
        )
        self.inv = netbox

    def devices(self):
        devices = self.inv.dcim.devices.all()
        return devices

    def device(self, identifier):
        device = self.inv.dcim.devices.filter(serial=identifier)
        if device:
            device = device[0]
            device['interfaces'] = self._interfaces(device['id'])
            return device
        else:
            return None

    def _interfaces(self, device_id):
        interfaces = self.inv.dcim.interfaces.filter(device_id=device_id)
        return interfaces
