from .base_class import BaseEntity 

class Teacher(BaseEntity):
    """"
    Class of Teacher
    
    attributes:
        id: Identificator of user
        name: Name of user
        role: Role of user
        pasword: Password of user
        created_at: Date time Stamp Created of user
        id_team: Identificator of team
    """
    def __init__(self, name:str, lastname:str, phone:str,  id_team:int ,id:int = None,date_baptism:str = None, date_of_birth:str=None):
        self.id= id
        self.name = name
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.date_baptism = date_baptism
        self.id_team = id_team



