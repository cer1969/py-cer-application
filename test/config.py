# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from cer.application030 import Application, AppIni, Translator

#-----------------------------------------------------------------------------------------

name = "test"
version = "0.1.0"

#-----------------------------------------------------------------------------------------
# Application

app = Application(name, version, copyright=u"Cristian Echeverría")

#-----------------------------------------------------------------------------------------
# User options

ini = AppIni(app.toAppDir("%s.ini" % name))
ini.addSection("app")
ini.addInt("app.width",  900, vmin=600, vmax=1000)
ini.addInt("app.height", 700, vmin=400, vmax=1000)
ini.addText("app.name", u'Test Niño')
ini.addSection("locale")
ini.addText("locale.lang", "no_lang")
ini.load(create=True)

#-----------------------------------------------------------------------------------------
# Translation suport

trans = Translator()
trans.folder = app.toAppDir("lang")
trans.lang = ini.locale_lang

#-----------------------------------------------------------------------------------------

app.ini = ini
app.trans = trans
app.register("cerapp")