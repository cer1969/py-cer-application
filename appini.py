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
    
    def add_option(self, sectop, default, validator=cval.CerTextValidator()):
        self._cer_validators[sectop] = validator
        self._cer_defaults[sectop] = default
        self.set(sectop, default)
    
    def add_text(self, sectop, default="", format="%s"):
        val = cval.CerTextValidator(format)
        self.add_option(sectop, default, val)
    
    def add_int(self, sectop, default=0, format="%d", vmin=None, vmax=None):
        val = cval.CerIntValidator(format, vmin, vmax)
        self.add_option(sectop, default, val)

    def add_float(self, sectop, default=0.0, format="%.2f", vmin=None, 
                  vmax=None):
        val = cval.CerFloatValidator(format, vmin, vmax)
        self.add_option(sectop, default, val)
    
    def add_time(self, sectop, default=datetime.now().time(),
                 format="%H:%M", vmin=None, vmax=None):
        val = cval.CerTimeValidator(format, vmin, vmax)
        self.add_option(sectop, default, val)
    
    def add_date(self, sectop, default=date.today(),
                 format="%d/%m/%Y", vmin=None, vmax=None):
        val = cval.CerDateValidator(format, vmin, vmax)
        self.add_option(sectop, default, val)
    
    def add_datetime(self, sectop, default=datetime.now(), 
                     format="%d/%m/%Y %H:%M", vmin=None, vmax=None):
        val = cval.CerDateTimeValidator(format, vmin, vmax)
        self.add_option(sectop, default, val)

    #-------------------------------------------------------------------------------------
    # Public method for setting and getting options values
    
    def get_sectops(self):
        sal = []
        for sect in self.sections():
            for op in self.options(sect):
                sectop = ".".join([sect, op])
                sal.append(sectop)
        return sal
    
    def set(self, sectop, value):
        val = self._cer_validators[sectop]
        txt = val.getText(value)
        if isinstance(val, cval.CerTextValidator):
            txt = txt.encode("latin-1")
        section, option = sectop.split(".")
        RawConfigParser.set(self, section, option, txt)
    
    def get_raw(self, sectop):
        # Si la validación falla lanza error
        val = self._cer_validators[sectop]
        section, option = sectop.split(".")
        text = RawConfigParser.get(self, section, option)
        if isinstance(val, cval.CerTextValidator):
            data = val.getData(text.decode("latin-1"))
        else:
            data = val.getData(text)
        return data
    
    def get(self, sectop):
        # Si la validación falla retorna default
        try:
            return self.get_raw(sectop)
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