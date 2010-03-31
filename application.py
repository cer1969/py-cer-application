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

class Application(object):
    
    def __init__(self, name, version, copyright="", company_name=None, description=None,
            iconpath=None, script=None, dest_base=None, manifest=False
        ):
        """
        name         : Application name
        version      : Application version
        copyright    : Optional copyright notice
        company_name : Optional company name
        description  : Optional Application description
        iconpath     : Optional icon path (py2exe)
        script       : Optional main python script name (py2exe)
        dest_base    : Optional executable name (py2exe)
        manifest     : Optional True to embed manifest. Use false for python 2.6 (py2exe)
        """
        self.name = name
        self.version = version
        self.copyright = copyright
        
        self.company_name = company_name if company_name else copyright
        self.description = description if description else (u"%s Application" % name)
        self.iconpath = iconpath
        self.script = script if script else ("%s.py" % name)
        self.dest_base = dest_base if dest_base else name
        self.manifest = manifest 
        
        if iconpath:
            self.icon_resources = [(1, iconpath)]
        if manifest:
            self.other_resources = [(MANIFEST_RT, 1, MANIFEST_TPL % (name, self.description))]
        
        self.ini = None
        self._trans = None
        
        self.isexe = hasattr(sys,"frozen") # True if compiled with py2exe
        self.argv = sys.argv[1:] # Command line arguments list
        
        app_path = sys.executable if self.isexe else sys.argv[0]
        app_path = os.path.abspath(app_path)
        self.appdir = os.path.dirname(app_path) # directory of caller script or exe        
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def toAppDir(self, pathname):
        """Return pathname joined with appdir"""
        p = os.path.join(self.appdir, pathname)
        return os.path.abspath(p)
    
    def register(self, name):
        """Register Application object as a globla name"""
        __builtin__.__dict__[name] = self
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    def _getTrans(self):
        return self._trans
    
    def _setTrans(self, trans):
        self._trans = trans
        if trans is None:
            if "_" in __builtin__.__dict__:
                del __builtin__.__dict__["_"]
        else:
            __builtin__.__dict__["_"] = self._trans.translate
    
    trans = property(_getTrans, _setTrans)