from .base_class import BaseEntity

class Inscription(BaseEntity):
    """"
    Class of Academy Inscription
    
    attributes:
        id: Identificator of inscription 
        id_student: Identificator of student
        id_classroom: Identificator of classroom
        year: Year of inscription
        cycle: Cycle of inscription
        date_taken: Date when inscription was taken
        type_material: Type of material
        status: Status of inscription
        date_inscription: Date of Inscription
        status_material: Status of material
    """
    def __init__(self, id_student:int, id_classroom:int, year:int, cycle:str, date_taken:str, 
                 type_material:str, status:bool=True, date_inscription:str=None, 
                 status_material:bool=True, id:int=None):
        self.id = id
        self.id_student = id_student
        self.id_classroom = id_classroom
        self.year = year
        self.cycle = cycle
        self.date_taken = date_taken
        self.type_material = type_material
        self.status = status
        self.date_inscription = date_inscription
        self.status_material = status_material