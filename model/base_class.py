from abc import ABC

class BaseEntity(ABC):
    """
        Base class for internal data view

        Methods define here:
            ___str___ : Personalized print data str
    """
    def __str__(self):
        attrs = ", ".join(f"{k} : {v}" for k , v in self.__dict__.items())
        return attrs