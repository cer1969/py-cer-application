# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

import config

#-----------------------------------------------------------------------------------------

print( _("Nombre = %s") % cerapp.name )
print( _("Versión = %s") % cerapp.version )
print( _("Derechos = %s") % cerapp.copyright )

print( _("Compañía = %s") % cerapp.company_name )
print( _("Descripción = %s") % cerapp.description )
print( _("Ruta ícono = %s") % cerapp.iconpath )
print( _("Nombre guión = %s") % cerapp.script )
print( _("Nombre ejecutable = %s") % cerapp.dest_base ) 

print( cerapp.manifest )

print( cerapp.isexe )
print( cerapp.argv )
print( cerapp.appdir )
print( cerapp.ini.filepath )
print( cerapp.ini.getOptions() )
print( ">>>", cerapp.ini.app_name )
print( cerapp.trans.getLangList() )
print( cerapp.ini.app_name )
print( "Niño Canción".encode().decode("Latin-1") )
#cerapp.trans.save()