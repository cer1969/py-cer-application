# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import __builtin__
import sys, os
from translator import Translator

#-----------------------------------------------------------------------------------------

#class Application(dict):
class Application(object):
    
    def __init__(self, name, version, copyright=u"-"):
        """
        name      : Application name
        version   : Application version
        copyright : Optional copyright notice
        **kwa     : Keyword argument to include
        """
        #dict.__init__(self)
        self.name = name
        self.version = version
        self.copyright = copyright
        
        self.description = u"%s Application" % name
        self.company = self.copyright
        self.iconpath = None
        
        self._isexe = hasattr(sys,"frozen") # True if compiled with py2exe
        self._argv = sys.argv[1:] # Command line arguments list
        
        app_path = sys.executable if self.isexe else sys.argv[0]
        app_path = os.path.abspath(app_path)
        self._appdir = os.path.dirname(app_path) # directory of caller script or exe        
    
    #def __getattr__(self, name):
    #    return self[name]
    
    #def __setattr__(self, name, value):
    #    self[name] = value
    
    #-------------------------------------------------------------------------------------
    # Readonly properties
    
    def _getIsExe(self):
        return self._isexe
    isexe = property(_getIsExe)
    
    def _getArgv(self):
        return self._argv
    argv = property(_getArgv)
    
    def _getAppDir(self):
        return self._appdir
    appdir = property(_getAppDir)
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def toAppDir(self, mypath):
        """Return mypath joined with appdir"""
        p = os.path.join(self.appdir, mypath)
        return os.path.abspath(p)

a = Application("hola", "1", copyright="CER")
print a.isexe
print a.name
print a.copyright

#-----------------------------------------------------------------------------------------

class _Application(object):
    
    def __init__(self):
        self.info = None
        self.ini = None
        self.resman = None
        self.trans = Translator()
        
        self.isexe = hasattr(sys,"frozen") # True if compiled with py2exe
        self.argv = sys.argv[1:] # Command line arguments list
        
        app_path = sys.executable if self.isexe else sys.argv[0]
        app_path = os.path.abspath(app_path)
        self.appdir = os.path.dirname(app_path) # directory of caller script or exe
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def toAppDir(self, mypath):
        """Return mypath joined with appdir"""
        p = os.path.join(self.appdir, mypath)
        return os.path.abspath(p)

#-----------------------------------------------------------------------------------------

_app = _Application()

__builtin__.__dict__['cerapp'] = _app
__builtin__.__dict__['_'] = _app.trans.translate