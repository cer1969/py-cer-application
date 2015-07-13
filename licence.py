# CRISTIAN ECHEVERRÍA RABÍ

import os, hmac, hashlib, sqlite3    #, getpass

#-----------------------------------------------------------------------------------------

__all__ = ["get_pre_code", "get_licence_code", "LicenceManager"]

#-----------------------------------------------------------------------------------------

class _Record(dict):
    __slots__ = ()
    def __getattr__(self, name):
        return self[name]
    def __setattr__(self, name, value):
        self[name] = value

def _record_factory(cursor, row):
    names = [x[0] for x in cursor.description]
    return _Record(zip(names, row))


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
        db = sqlite3.connect(filename)
        db.row_factory = _record_factory
        
        cur = db.cursor()
        cur.execute("select * from sqlite_master where name='lic'")
        data = cur.fetchall()
        
        if len(data) == 0:
            cur.execute("""create table lic (idx text primary key not null, name text, 
                company text, email text, key text)"""
            )
            cur.execute("""insert into lic (idx, name, company, email, key) 
                values (?, ?, ?, ?, ?)""", ["USER", u"", u"", u"", u""]
            )
            db.commit()
        
        cur.close()
        
        self.db = db
        self.key1 = key1
        self.key2 = key2
    
    def close(self):
        self.db.close()
    
    def set_info(self, **kwa):
        info = self.info
        info.update(kwa)
        del info["idx"]
        
        _query = "update lic set %s where idx='USER'" % ", ".join(["%s=?" % x for x in info.keys()]) 
        cur = self.db.cursor()
        cur.execute(_query, info.values())
        cur.close()
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
        cur = self.db.cursor()
        cur.execute("select * from lic where idx='USER'")
        info = cur.fetchone()
        cur.close()
        return info
    
    info = property(_get_info)
    
    def _get_check(self):
        info = self.info
        return self.licence_code == info.key
    
    check = property(_get_check)
    
    def _get_licence_text(self):
        if self.check:
            msg = (
                   " REGISTRO:\n"
                   " %s\n"
                   " %s\n"
            ) % (self.info.name, self.info.company)
            return msg
        return " APLICACIÓN NO REGISTRADA"
    
    licence_text = property(_get_licence_text)
    
    def _get_licence_status(self):
        if self.check:
            msg = "Registrado: %s - %s" % (self.info.name, self.info.company)
            return msg
        return "Aplicación no registrada"
    
    licence_status = property(_get_licence_status)
    
    def _get_key_text(self):
        info = self.info
        msg = "_cercode_ Alloy - %s\n%s - %s\n%s" % (info.company, info.name, info.email, self.pre_code)
        return msg
    
    key_text = property(_get_key_text)
    