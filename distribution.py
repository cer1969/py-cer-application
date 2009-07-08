# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from distutils.core import setup
import py2exe   # requerido
import sys

#-----------------------------------------------------------------------------------------

__all__ = ["Distribution", "get_options", "make_exe"]

#-----------------------------------------------------------------------------------------

manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(name)s"
    type="win32"
/>
<description>%(name)s Program</description>
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

RT_MANIFEST = 24

#-----------------------------------------------------------------------------------------

class Distribution(object):
    
    def __init__(self, info, manifest=True):
        
        self.name = info.name
        self.version = info.version
        self.description = info.description
        self.company_name = info.company
        self.copyright = info.copyright
        
        # start script 
        self.script = "%(name)s.py" % info
        
        if manifest:
            self.other_resources = [(RT_MANIFEST, 1, manifest_template % info)]
        if info.iconpath:
            self.icon_resources = [(1, info.iconpath)]
        
        # exe name
        self.dest_base = info.name

#-----------------------------------------------------------------------------------------

def get_options(**kwa):
    sal = {}
    sal['py2exe'] = kwa
    return sal

#-----------------------------------------------------------------------------------------

def make_exe(**kwa):
    # Cuando se corre sin argumentos, incorporamos py2exe as argument
    sys.argv.append("py2exe")
    setup(**kwa)
