

class StoreFSN(object):

    def __init__(self, store_id, fsns_src):
        self.store_id = store_id
        self.fsns_src = fsns_src

    def serialize(self):
        return {
            'store_id': self.store_id,
            'fsns_src': self.fsns_src,
        }
