class BTrDBWrapper(object):
    def __init__(self):
        self.ur = btrdb.UUIDResolver("miranda.cs.berkeley.edu", "uuidresolver", "uuidpass", "upmu")
        self.connection = btrdb.HTTPConnection("miranda.cs.berkeley.edu")

    def get_uuid(self, path):
        return self.ur.resolve(path)

    def get_rawdata(self, path, start, logWindowSize):
        raw = self.connection.get_stat(self.get_uuid(path), start, start + (1<<logWindowSize), 23)
        return [(x[0],x[2]) for x in raw]
