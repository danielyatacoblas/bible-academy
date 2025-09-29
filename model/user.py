from .base_class import BaseEntity 

class User(BaseEntity):
    """
    Class of User

    attributes:
        id: Identificator of User
        user: Name of user
        role: Role of user
        pasword: Password of user
        created_at: Date time Stamp Created of user
    """
    def __init__(self,user : str,role : str,password : str, id:int=None , created_at=None):
        self.id = id
        self.created_at = created_at
        self.user = user
        self.role = role
        self.password = password
        self.created_at = created_at
        
  

