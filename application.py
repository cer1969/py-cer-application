# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import __builtin__
import sys, os
from translator import Translator

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