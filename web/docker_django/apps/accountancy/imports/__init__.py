from .import_from_file import import_from_file
from .import_from_INGDiBa import import_from_INGDiBa
from .import_from_mBank import import_from_mBank



class ImportMethod(object):
    
    def __init__(self, name, func):
        self.name = name
        self.func = func
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.__repr__()
    
    pass



IMPORT_FROM_FILE = ImportMethod("import_from_file", import_from_file)

IMPORT_FROM_INGDIBA = ImportMethod("import_from_INGDiBa", import_from_INGDiBa)

IMPORT_FROM_MBANK = ImportMethod("import_from_mBank", import_from_mBank)



AVAILABLE_IMPORT_METHODS = {
    "IMPORT_FROM_FILE": IMPORT_FROM_FILE,
    "IMPORT_FROM_INGDIBA": IMPORT_FROM_INGDIBA,
    "IMPORT_FROM_MBANK": IMPORT_FROM_MBANK,
}



__all__ = ("IMPORT_FROM_FILE", "IMPORT_FROM_INGDIBA", "IMPORT_FROM_MBANK", "AVAILABLE_IMPORT_METHODS")


