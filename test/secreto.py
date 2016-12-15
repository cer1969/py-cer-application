# -*- coding: utf-8 -*-

import os
from cer.application.licence import get_licence_code

#-----------------------------------------------------------------------------------------

def get_my_serial():
    drive = os.path.splitdrive("c:/")[0]
    if os.path.exists("%s/" % drive):
        x = os.popen("vol %s" % drive, "r").read()
        return x.split()[-1]
    return None


pre = b"37419a64279105ef081094b904fc6214785893ec"
key = b"cal1ps0"

print (get_licence_code(key, pre))

print (get_licence_code(key, b""))

print (get_my_serial())