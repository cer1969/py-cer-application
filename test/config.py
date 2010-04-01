# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from cer.application import Application, AppIni, Translator

#-----------------------------------------------------------------------------------------

name = "test"
version = "0.1.0"
copyright = u"Cristian Echeverría"

#-----------------------------------------------------------------------------------------
# Application

app = Application(name, version, copyright)
app.register("cerapp")

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

app.ini = ini

#-----------------------------------------------------------------------------------------
# Translation suport

trans = Translator()
trans.folder = app.toAppDir("lang")
trans.lang = ini.locale_lang

app.trans = trans