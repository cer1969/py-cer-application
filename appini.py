# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from datetime import datetime, date
from ConfigParser import RawConfigParser
import cer.utils.validators as cval 

#-----------------------------------------------------------------------------------------

__all__ = ['AppIni']

#-----------------------------------------------------------------------------------------

class AppIni(RawConfigParser):
    
    def __init__(self, filepath):
        RawConfigParser.__init__(self)
        self.filepath = filepath
        self._cer_validators = {}
        self._cer_defaults = {}
    
    #-------------------------------------------------------------------------------------
    # Public method for options definition
    
    addSection = RawConfigParser.add_section    # method rename
    
    def addOption(self, sectop, default, validator=None):
        self._cer_validators[sectop] = cval.TextValidator() if validator is None else validator
        self._cer_defaults[sectop] = default
        self.set(sectop, default)
    
    def addText(self, sectop, default="", format="%s"):
        val = cval.TextValidator(format)
        self.addOption(sectop, default, val)
    
    def addInt(self, sectop, default=0, format="%d", vmin=None, vmax=None):
        val = cval.IntValidator(format, vmin, vmax)
        self.addOption(sectop, default, val)
    
    def addFloat(self, sectop, default=0.0, format="%.2f", vmin=None, 
                  vmax=None):
        val = cval.FloatValidator(format, vmin, vmax)
        self.addOption(sectop, default, val)
    
    def addTime(self, sectop, default=None, format="%H:%M", vmin=None, vmax=None):
        val = cval.TimeValidator(format, vmin, vmax)
        dfv = datetime.now().time() if default is None else default
        self.addOption(sectop, dfv, val)
    
    def addDate(self, sectop, default=None, format="%d/%m/%Y", vmin=None, vmax=None):
        val = cval.DateValidator(format, vmin, vmax)
        dfv = date.today() if default is None else default
        self.addOption(sectop, dfv, val)
    
    def addDateTime(self, sectop, default=None, format="%d/%m/%Y %H:%M", vmin=None, vmax=None):
        val = cval.DateTimeValidator(format, vmin, vmax)
        dfv = datetime.now() if default is None else default
        self.addOption(sectop, dfv, val)
    
    #-------------------------------------------------------------------------------------
    # Public method for setting and getting options values
    
    def getOptions(self):
        sal = []
        for sect in self.sections():
            for op in self.options(sect):
                sectop = ".".join([sect, op])
                sal.append(sectop)
        return sal
    
    def set(self, sectop, value):
        val = self._cer_validators[sectop]
        txt = val.getText(value)
        if isinstance(val, cval.TextValidator):
            txt = txt.encode("latin-1")
        section, option = sectop.split(".")
        RawConfigParser.set(self, section, option, txt)
    
    def getRaw(self, sectop):
        # Si la validación falla lanza error
        val = self._cer_validators[sectop]
        section, option = sectop.split(".")
        text = RawConfigParser.get(self, section, option)
        if isinstance(val, cval.TextValidator):
            data = val.getData(text.decode("latin-1"))
        else:
            data = val.getData(text)
        return data
    
    def get(self, sectop):
        # Si la validación falla retorna default
        try:
            return self.getRaw(sectop)
        except ValueError:
            value = self._cer_defaults[sectop]
            self.set(sectop, value)
            return value
    
    #-------------------------------------------------------------------------------------
    # Public method for load and save
    
    def save(self):
        """Save config file"""
        f = open(self.filepath, "w")
        self.write(f)
        f.close()
    
    def load(self, create=True):
        """Load config file.
        If load fail it raises IOError if create=False.
        If create=True the config file will be created
        """
        try:
            f = open(self.filepath, "r")
            self.readfp(f)
            f.close()
        except IOError, e:
            if create:
                self.save()
            else:
                raise IOError(e)
    
    #-------------------------------------------------------------------------------------
    # Permite acceder items como atributos section_option (read-only)
    
    def __getattr__(self, name):
        sectop = ".".join(name.split("_"))
        return self.get(sectop)