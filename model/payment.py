from .base_class import BaseEntity 

class Payment(BaseEntity):
    """
    Class of Payment

    attributes:
        id: Identificator of Payment
        method_payment: Method of Payment
        amount: Amount of payment
        id_inscription: Indentificator of inscription
        created_datetime: Created of date time
    """
    def __init__(self, method_payment: str,amount:int,created_datetime:str,id_inscription:int,id:int=None):
        self.id = id
        self.method_payment = method_payment
        self.amount = amount
        self.id_inscription = id_inscription
        self.created_datetime= created_datetime
        
  

