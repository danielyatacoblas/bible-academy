from .base_class import BaseEntity 

class Team(BaseEntity):
    """
    Class of Team

    attributes:
        id: Identificator of Team
        name: Name of Team
        age_start: age of start for team
        age_end: age of end for team
        gender: Gender of Team
    """
    
    VALID_GENDERS = ["Mixto", "Masculino", "Femenino"]
    
    def __init__(self, name: str, age_start: int, age_end: int, gender: str, id: int = None):
        self.id = id
        self.name = self._validate_name(name)
        self.age_start = self._validate_age_start(age_start)
        self.age_end = self._validate_age_end(age_end)
        self.gender = self._validate_gender(gender)
        
        # Validate age range
        self._validate_age_range()
    
    def _validate_name(self, name: str) -> str:
        """Validate and clean team name"""
        if not name or not isinstance(name, str):
            raise ValueError("El nombre del equipo es obligatorio")
        
        name = name.strip()
        if len(name) < 2:
            raise ValueError("El nombre del equipo debe tener al menos 2 caracteres")
        if len(name) > 100:
            raise ValueError("El nombre del equipo no puede exceder 100 caracteres")
        
        return name
    
    def _validate_age_start(self, age_start: int) -> int:
        """Validate starting age"""
        if not isinstance(age_start, int):
            try:
                age_start = int(age_start)
            except (ValueError, TypeError):
                raise ValueError("La edad de inicio debe ser un número válido")
        
        if age_start < 0:
            raise ValueError("La edad de inicio no puede ser negativa")
        if age_start > 100:
            raise ValueError("La edad de inicio no puede ser mayor a 100")
        
        return age_start
    
    def _validate_age_end(self, age_end: int) -> int:
        """Validate ending age"""
        if not isinstance(age_end, int):
            try:
                age_end = int(age_end)
            except (ValueError, TypeError):
                raise ValueError("La edad de fin debe ser un número válido")
        
        if age_end < 0:
            raise ValueError("La edad de fin no puede ser negativa")
        if age_end > 100:
            raise ValueError("La edad de fin no puede ser mayor a 100")
        
        return age_end
    
    def _validate_gender(self, gender: str) -> str:
        """Validate gender"""
        if not gender or not isinstance(gender, str):
            raise ValueError("El género es obligatorio")
        
        gender = gender.strip()
        if gender not in self.VALID_GENDERS:
            raise ValueError(f"El género debe ser uno de: {', '.join(self.VALID_GENDERS)}")
        
        return gender
    
    def _validate_age_range(self):
        """Validate that age_start < age_end"""
        if self.age_start >= self.age_end:
            raise ValueError("La edad de inicio debe ser menor que la edad de fin")
    
    def to_dict(self) -> dict:
        """Convert team to dictionary for database operations"""
        return {
            "id": self.id,
            "name": self.name,
            "age_start": self.age_start,
            "age_end": self.age_end,
            "gender": self.gender
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Team':
        """Create Team instance from dictionary"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            age_start=data.get("age_start"),
            age_end=data.get("age_end"),
            gender=data.get("gender")
        )
    
    def update(self, **kwargs):
        """Update team attributes with validation"""
        if "name" in kwargs:
            self.name = self._validate_name(kwargs["name"])
        if "age_start" in kwargs:
            self.age_start = self._validate_age_start(kwargs["age_start"])
        if "age_end" in kwargs:
            self.age_end = self._validate_age_end(kwargs["age_end"])
        if "gender" in kwargs:
            self.gender = self._validate_gender(kwargs["gender"])
        
        # Re-validate age range after updates
        self._validate_age_range()
    
    def get_age_range(self) -> str:
        """Get formatted age range string"""
        return f"{self.age_start} - {self.age_end} años"
    
    def __str__(self):
        return f"Team(id={self.id}, name='{self.name}', age_range='{self.get_age_range()}', gender='{self.gender}')"
    
    def __repr__(self):
        return self.__str__()
