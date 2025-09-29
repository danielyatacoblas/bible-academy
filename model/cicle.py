from .base_class import BaseEntity 

class Cicle(BaseEntity):
    """
    Class of Cicle

    attributes:
        id: Identificator of Cicle
        cicle: Cicle indentificator
        date_start: date start
        date_end: date end
        manager: manager of inscription
    """
    def __init__(self, cicle: str,date_start:str,date_end:str,manager:str, id:int=None):
        self.id = id
        self.cicle = cicle
        self.date_start = date_start
        self.date_end = date_end
        self.manager = manager
        
  

