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
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def toAppDir(self, mypath):
        """Return mypath joined with appdir"""
        p = os.path.join(self.appdir, mypath)
        return os.path.abspath(p)
    
    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def _get_isexe(self):
        # Return true if compiled with py2exe
        return hasattr(sys,"frozen")
    
    def _get_appdir(self):
        # Return directory of caller script or exe
        app_path = sys.executable if self.isexe else sys.argv[0]
        app_path = os.path.abspath(app_path)
        return os.path.dirname(app_path)
    
    def _get_argv(self):
        # Return list with command line arguments
        return sys.argv[1:]
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    isexe  = property(_get_isexe)
    appdir = property(_get_appdir)
    argv   = property(_get_argv)

#-----------------------------------------------------------------------------------------

_app = _Application()

__builtin__.__dict__['cerapp'] = _app
__builtin__.__dict__['_'] = _app.trans.translate