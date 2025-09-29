from .base_class import BaseEntity

class Student(BaseEntity):
    """"
    Class of Student
    
    attributes:
        id: Identificator of student
        name: Name of student
        lastname: Lastname of student
        phone: Phone of student
        date_baptism: Date baptism of student
        date_of_birth: Date of Birth 
        id_team: Identificator to team
    """
    def __init__(self, name:str, lastname:str, phone:str, date_baptism:str, id_team:int,id:int = None, date_of_birth:str=None):
        self.id= id
        self.name = name
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.date_baptism = date_baptism
        self.id_team = id_team


