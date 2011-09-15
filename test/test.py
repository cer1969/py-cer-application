# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

import config

#-----------------------------------------------------------------------------------------

print _(u"Nombre = %s") % cerapp.name
print _(u"Versión = %s") % cerapp.version
print _(u"Derechos = %s") % cerapp.copyright

print _(u"Compañía = %s") % cerapp.company_name
print _(u"Descripción = %s") % cerapp.description
print _(u"Ruta ícono = %s") % cerapp.iconpath
print _(u"Nombre guión = %s") % cerapp.script
print _(u"Nombre ejecutable = %s") % cerapp.dest_base 

print cerapp.manifest

print cerapp.isexe
print cerapp.argv
print cerapp.appdir
print cerapp.ini.filepath
print cerapp.ini.getOptions()
print cerapp.ini.app_name
print cerapp.trans.getLangList()

#cerapp.trans.save()