from .base_class import BaseEntity

class Course(BaseEntity):
    """"
    Class of Course
    
    attributes:
        id: Identificator of course
        name: Name of Course
        level: Level of Course
    """
    def __init__(self, name:str, level: int, id:int = None):
        self.id= id
        self.name = name
        self.level = level


