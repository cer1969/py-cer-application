# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import os, hmac, hashlib    #, getpass
from cer.data import sqlite2

#-----------------------------------------------------------------------------------------

__all__ = ["get_pre_code", "get_licence_code", "LicenceManager"]

#-----------------------------------------------------------------------------------------

#def _get_user():
#    # Por el momento no lo usamos para permitir instalación portable
#    return getpass.getuser()

def _get_serial():
    drive = os.path.splitdrive(cerapp.appdir)[0]
    if os.path.exists("%s/" % drive):
        x = os.popen("vol %s" % drive, "r").read()
        return x.split()[-1]
    return None

def get_pre_code(key, email):
    maker = hmac.new(key, digestmod=hashlib.sha1)
    #maker.update(self._get_user())
    maker.update(_get_serial())
    maker.update(email)
    return maker.hexdigest()

def get_licence_code(key, pre):
    maker = hmac.new(key, digestmod=hashlib.sha1)
    maker.update(pre)
    return maker.hexdigest()


#-----------------------------------------------------------------------------------------

class LicenceManager(object):
    
    def __init__(self, filename, key1, key2):
        db = sqlite2.connect(filename)
        
        if len(db.tablenames) == 0:
            query = (
                "create table lic (idx text primary key not null, name text, " 
                "company text, email text, key text)"
            )
            db.alter(query)
            db.refresh()
            db["lic"].insertNew(idx=u"USER", name=u"", company=u"", email=u"", key=u"")
            db.commit()
        
        self.db = db
        self.key1 = key1
        self.key2 = key2
    
    def close(self):
        self.db.close()
    
    def set_info(self, **kwa):
        info = self.info
        info.update(kwa)
        self.db["lic"].update(info)
        self.db.commit()
    
    #-------------------------------------------------------------------------------------
    
    def _get_pre_code(self):
        info = self.info
        return get_pre_code(self.key1, info.email)
    
    pre_code = property(_get_pre_code)
    
    def _get_licence_code(self):
        return get_licence_code(self.key2, self.pre_code)
    
    licence_code = property(_get_licence_code)
    
    def _get_info(self):
        return self.db["lic"][u"USER"]
    
    info = property(_get_info)
    
    def _get_check(self):
        info = self.info
        return self.licence_code == info.key
        #return self.get_licence_code(self.get_pre_code(info.email)) == info.key
    
    check = property(_get_check)
    
    def _get_licence_text(self):
        if self.check:
            msg = (
                   u" REGISTRO:\n"
                   u" %s\n"
                   u" %s\n"
            ) % (self.info.name, self.info.company)
            return msg
        return u" APLICACIÓN NO REGISTRADA"
    
    licence_text = property(_get_licence_text)
    
    def _get_licence_status(self):
        if self.check:
            msg = "Registrado: %s - %s" % (self.info.name, self.info.company)
            return msg
        return u"Aplicación no registrada"
    
    licence_status = property(_get_licence_status)
    
    def _get_key_text(self):
        info = self.info
        msg = u"_cercode_ Alloy - %s\n%s - %s\n%s" % (info.company, info.name, info.email, self.pre_code)
        return msg
    
    key_text = property(_get_key_text)
    