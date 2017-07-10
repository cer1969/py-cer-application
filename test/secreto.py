# -*- coding: utf-8 -*-

from cer.application.licence import get_licence_code, get_serial, get_pre_code

#-----------------------------------------------------------------------------------------

pre1 = "fda6a89c5b2f63dc3a7fec8f4500595fa8f944c7"
pre2 = "2bfd6abf7ec78f8335f19a0613c743b7f74bad12"

print (get_pre_code("c:", "pre-cal1ps0", "crecheverria@colbun.cl"))
print (get_serial("c:"))
print ("--------------------------")
print (get_licence_code("cal1ps0", pre1))
print (get_licence_code("cal1ps0", pre2))