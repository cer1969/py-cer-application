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

def get_serial(drive):
    """Retorna número de serie del disco duro
    """
    if os.path.exists("%s/" % drive):
        x = os.popen("vol %s" % drive, "r").read()
        return x.split()[-1]
    return None

def get_pre_code(drive, key, email):
    maker = hmac.new(key.encode("utf-8"), digestmod=hashlib.sha1)
    #maker.update(self._get_user())
    maker.update(get_serial(drive).encode("utf-8"))
    maker.update(email.encode("utf-8"))
    return maker.hexdigest()

def get_licence_code(key, pre):
    maker = hmac.new(key.encode("utf-8"), digestmod=hashlib.sha1)
    maker.update(pre.encode("utf-8"))
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
                values (?, ?, ?, ?, ?)""", ["USER", u"", u"", u"", b""]
            )
            db.commit()
        
        cur.close()
        
        self.drive = os.path.splitdrive(filename)[0]
        self.db = db
        self.key1 = key1
        self.key2 = key2
    
    def close(self):
        self.db.close()
    
    def set_info(self, **kwa):
        info = self.info
        info.update(kwa)
        
        _query = "update lic set email=?, key=?, name=?, company=? where idx='USER'"
        cur = self.db.cursor()
        cur.execute(_query, [info.email, info.key, info.name, info.company])
        cur.close()
        self.db.commit()
    
    #-------------------------------------------------------------------------------------
    
    @property
    def info(self):
        """"Retorna datos almacenados de licencia
        """
        cur = self.db.cursor()
        cur.execute("select * from lic where idx='USER'")
        info = cur.fetchone()
        cur.close()
        return info

    @property
    def pre_code(self):
        """Retorna pre code construido con key1 y email
        """
        info = self.info
        return get_pre_code(self.drive, self.key1, info.email)
    
    @property
    def licence_code(self):
        """Retorna licence code usando key2 y pre_code
        """
        return get_licence_code(self.key2, self.pre_code)
    
    @property
    def check(self):
        info = self.info
        return self.licence_code == info.key
    
    @property
    def licence_text(self):
        if self.check:
            msg = (
                   " REGISTRO:\n"
                   " %s\n"
                   " %s\n"
            ) % (self.info.name, self.info.company)
            return msg
        return " APLICACIÓN NO REGISTRADA"
    
    @property
    def licence_status(self):
        if self.check:
            msg = "Registrado: %s - %s" % (self.info.name, self.info.company)
            return msg
        return "Aplicación no registrada"
    
    @property
    def key_text(self):
        info = self.info
        msg = "_cercode_ Alloy - %s\n%s - %s\n%s" % (info.company, info.name, info.email, self.pre_code)
        return msg