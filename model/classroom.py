from .base_class import BaseEntity

class Classroom(BaseEntity):
    """
        Class of  Classroom

        attributes:
            id: Indetificator of classroom
            name: Name of classroom
            start date: Start of Date
            end date: End of Date
            id_teacher: Identificator of teacher
            id_course: Identificator of course
            id_cicle: Identificator of cicle
    """
    def __init__(self,name:str,start_date:str,end_date:str,id_teacher:int,id_course:int,id_cicle:int,id:int=None):
        self.name = name
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.id_teacher=id_teacher
        self.id_course = id_course
        self.id_cicle = id_cicle
        
