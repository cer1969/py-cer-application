# CRISTIAN ECHEVERRÍA RABÍ 

from distutils.core import setup
import py2exe   # requerido
import sys

#-----------------------------------------------------------------------------------------

__all__ = ["getOptions", "makeExe"]

#-----------------------------------------------------------------------------------------

def getOptions(**kwa):
    sal = {}
    sal['py2exe'] = kwa
    return sal

def makeExe(**kwa):
    # Cuando se corre sin argumentos, incorporamos py2exe as argument
    sys.argv.append("py2exe")
    setup(**kwa)
