from typing import Sequence   
def funkcja(*argv, **kwargs):
    if not isinstance(argv, Sequence):
        raise TypeError
    if 'paradygmat' in kwargs.keys() and 'operacja' in kwargs.keys():
        return [kwargs['operacja'](arg) if kwargs['paradygmat'](arg) else None for arg in argv]
    else:
        raise KeyError


   


