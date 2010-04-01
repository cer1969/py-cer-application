# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import __builtin__
import sys, os

#-----------------------------------------------------------------------------------------

__all__ = ['Application']

#-----------------------------------------------------------------------------------------

MANIFEST_TPL = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%s"
    type="win32"
/>
<description>%s</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

MANIFEST_RT = 24

#-----------------------------------------------------------------------------------------

isexe = hasattr(sys,"frozen")
argv = sys.argv[1:]

_app_path = sys.executable if isexe else sys.argv[0]
_app_path = os.path.abspath(_app_path)
appdir = os.path.dirname(_app_path)

#-----------------------------------------------------------------------------------------

class Application(object):
    
    _isexe = isexe
    _argv = argv
    _appdir = appdir
    
    def __init__(self, name, version, copyright="", company_name=None, description=None):
        """
        name         : Application name
        version      : Application version
        copyright    : Optional copyright notice
        company_name : Optional company name
        description  : Optional Application description
        
        Read/write members
        iconpath     : Icon path (py2exe)
        script       : Main python script name. Default name.py (py2exe)
        dest_base    : Executable name. Default name (py2exe)
        manifest     : True to embed manifest. Use false for python 2.6 (py2exe)
        ini          : Optional AppIni object. Default None
        trans        : Optional Translator object. Default None
        
        Readonly members (class members: All instance has the same values)
        isexe        : True if compiled with py2exe
        argv         : Command line arguments list
        appdir       : directory of caller script or exe
        """
        self.name = name
        self.version = version
        self.copyright = copyright
        self.company_name = company_name if company_name else copyright
        self.description = description if description else (u"%s Application" % name)
        
        self._iconpath = None
        self.script = "%s.py" % name
        self.dest_base = name
        self._manifest = False 
        self.ini = None
        self._trans = None        
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    @staticmethod
    def toAppDir(pathname):
        """Return pathname joined with appdir"""
        p = os.path.join(Application._appdir, pathname)
        return os.path.abspath(p)
    
    def register(self, name):
        """Register Application object as a globla name"""
        __builtin__.__dict__[name] = self
    
    #-------------------------------------------------------------------------------------
    # Readonly properties
    
    @property
    def isexe(self):
        return self._isexe

    @property
    def argv(self):
        return self._argv    
    
    @property
    def appdir(self):
        return self._appdir
    
    #-------------------------------------------------------------------------------------
    # Read/write properties
    
    def _getIconPath(self):
        return self._iconpath
    
    def _setIconPath(self, iconpath):
        self._iconpath = iconpath
        if (iconpath is None) and hasattr(self, "icon_resources"):
            delattr(self, "icon_resources")
        else:
            self.icon_resources = [(1, iconpath)]
    
    iconpath = property(_getIconPath, _setIconPath)
    
    def _getManifest(self):
        return self._manifest
    
    def _setManifest(self, manifest):
        self._manifest = manifest
        if (manifest is None) and hasattr(self, "other_resources"):
            delattr(self, "other_resources")
        else:
            tpl = MANIFEST_TPL % (self.name, self.description)
            self.other_resources = [(MANIFEST_RT, 1, tpl)]
    
    manifest = property(_getManifest, _setManifest)
        
    def _getTrans(self):
        return self._trans
    
    def _setTrans(self, trans):
        self._trans = trans
        if (trans is None) and ("_" in __builtin__.__dict__):
            del __builtin__.__dict__["_"]
        else:
            __builtin__.__dict__["_"] = self._trans.translate
    
    trans = property(_getTrans, _setTrans)