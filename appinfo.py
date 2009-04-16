# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import sys, os

#-----------------------------------------------------------------------------------------

__all__ = ['AppInfo']

#-----------------------------------------------------------------------------------------

class AppInfo(dict):
    
    def __init__(self, name, version, **kwa):
        """
        name    : Application name
        version : Application version
        **kwa   : Keyword argument to include
        """
        dict.__init__(self)
        self.name = name
        self.version = version
        self.description = u"%s Application" % name
        self.company = u"Cristian Echeverría Rabí"
        self.copyright = u"Cristian Echeverría Rabí"
        self.iconpath = None
        self.update(**kwa)
    
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value