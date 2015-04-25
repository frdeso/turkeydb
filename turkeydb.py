import pastebin_python
import json


class turkeyDB:
    def __init__(self, name):
        config = {}
        execfile("turkeydb.conf", config) 
        self.pastebin = pastebin_python.PastebinPython(api_dev_key=config["api_dev_key"])
        self.pastebin.createAPIUserKey(config["user"], config["password"])
        self.name = name
    def __repr__(self):
        return "turkeyDB"

    def getDB(self):
        pastes = self.pastebin.listUserPastes()
        for paste in pastes:
            if paste["paste_title"] == self.name:
                return json.loads(self.pastebin.getPasteRawOutput(paste["paste_key"])), paste["paste_key"]


    def __str__(self):
        db, key= self.getDB()
        return json.dumps(db, sort_keys=True, indent=4)

    def CreateDB(self, data):
       url = self.pastebin.createPaste(json.dumps(data, sort_keys=True, indent=4), self.name)
       return url

    def insert(self, key, value):
       db, paste_key=self.getDB()
       db[key] = value
       url = self.CreateDB(db)
       self.pastebin.deletePaste(paste_key)
       return url

    def remove(self, key):
        db, paste_key = self.getDB()
        del db[key]
        url = self.CreateDB(db)
        self.pastebin.deletePaste(paste_key)
        return url
