from requests import Session

class DatastoreException(Exception):
    pass

class DatastoreExceptionNotFound(DatastoreException):
    def __init__(self):
        super(DatastoreExceptionNotFound, self).__init__('Not Found')

class Datastore(object):
    BOOT_PATH = '/boot'
    IGNITION_PATH = '/ignition/{}'
    META_DATA_PATH = '/cloud-init/{}/meta-data'
    USER_DATA_PATH = '/cloud-init/{}/user-data'

    def __init__(self, server):
        self._server = server
        self._sess = Session()

    def _request(self, method, path, params=None):
        url = f'{self._server}{path}'
        resp = self._sess.request(method, url, params=params)
        if resp.status_code == 404:
            raise DatastoreExceptionNotFound()

        return resp

    def boot(self, ident):
        resp = self._request('GET', self.BOOT_PATH).json()
        if ident in resp:
            return resp[ident]
        else:
            raise DatastoreExceptionNotFound()

    def ignition(self, ident):
        path = self.IGNITION_PATH.format(ident)
        return self._request('GET', path).text

    def meta_data(self, ident):
        path = self.META_DATA_PATH.format(ident)
        return self._request('GET', path).text

    def user_data(self, ident):
        path = self.USER_DATA_PATH.format(ident)
        return self._request('GET', path).text
        
