# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

import glob
from cer.application030.distribution import getOptions, makeExe
from config import app

#-----------------------------------------------------------------------------------------

data_files = [
    ("lang", glob.glob("lang/*.cat")),
]

options = getOptions(
    compressed = 1,
    optimize = 2, 
    bundle_files = 3, # DEBERÍA SER 2, VALOR 3 NECESARIO TEMPORALMENTE POR PROBLEMAS EN wxPython
    #excludes = ["Tkconstants", "Tkinter", "tcl"],
    dll_excludes = ['w9xpopen.exe'], #'MSVCR71.dll']
)

#-----------------------------------------------------------------------------------------

makeExe(
    #windows = [app1],
    console = [app],
    data_files = data_files,
    options = options,
    zipfile = "runtime.zip"
)