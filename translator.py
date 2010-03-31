# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

import os, glob

#-----------------------------------------------------------------------------------------

__all__ = ['Translator', 'NO_LANG']

#-----------------------------------------------------------------------------------------

NO_LANG = "no_lang"

#-----------------------------------------------------------------------------------------

class Translator(dict):
    
    def __init__(self):
        dict.__init__(self)
        self._folder = None
        self._lang = NO_LANG
        self.name = None
        self._nocat = {} # To store missing keys
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def translate(self, key):
        if self._lang == NO_LANG:
            return key
        try:
            return self[key]
        except KeyError:
            self._nocat[key] = key
            return key
    
    def save(self):
        if self._lang == NO_LANG:
            raise AttributeError("'no_lang' is not a valid catalog name")
        if self._folder is None:
            raise AttributeError("None is not a valid folder name")
        
        if not(os.path.exists(self._folder)):
            os.mkdir(self._folder)
        
        langfile = os.path.join(self.folder, "%s.cat" % self._lang)
        f = open(langfile, "w")
        f.write(self._getText())
        f.close()
    
    def getLangList(self):
        if self._folder is None:
            raise AttributeError("None is not a valid folder name")
        lcats = glob.glob(os.path.join(self._folder, "*.cat"))
        lcats = [os.path.split(x)[1] for x in lcats]
        lcats = [os.path.splitext(x)[0] for x in lcats]
        sal = []
        for i in lcats:
            name, _cat = self._getCatalog(i)
            sal.append((i, name))
        return sal
    
    #-------------------------------------------------------------------------------------
    # Private methods
    
    def _getCatalog(self, lang):
        langfile = os.path.join(self.folder, "%s.cat" % lang)
        mydict = {"name": None, "cat": {}}
        try:
            execfile(langfile, {}, mydict)
        except IOError:
            pass
        return mydict["name"], mydict["cat"]
    
    def _getText(self):
        tpl = ("# -*- coding: utf-8 -*-\n"
               "# Language catalog\n\n"
               "name = %s\n\n"
               "cat  = {\n%s\n}\n\n"
               "new  = {\n%s\n}"
        )
        
        tname = repr(self.name)
        
        catitems = self.items()
        catitems.sort()
        catkeys = ["    %s: %s" % (repr(key), repr(value)) for (key,value) in catitems]
        tcat  = ",\n".join(catkeys)
        
        newitems = self._nocat.items()
        newitems.sort()
        newkeys = ["    %s: %s" % (repr(key), repr(value)) for (key,value) in newitems]
        tnew = ",\n".join(newkeys)
        
        sal = tpl % (tname, tcat, tnew)
        return sal
    
    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def _getFolder(self):
        return self._folder
    
    def _setFolder(self, folder):
        self._folder = os.path.abspath(folder)
    
    def _getLang(self):
        return self._lang
    
    def _setLang(self, lang):
        self.clear()
        self._lang = lang
        if lang == NO_LANG:
            self.name = None
        else:
            name, cat = self._getCatalog(lang)
            self.name = name
            self.update(cat)
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    folder = property(_getFolder, _setFolder)
    lang   = property(_getLang,   _setLang)
