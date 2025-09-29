import json
import os
from typing import Any, Dict, Optional

class LocalStorage:
    """
    Sistema de almacenamiento local para la aplicación Bible Academy
    """
    
    def __init__(self, storage_path: str = "storage/data"):
        self.storage_path = storage_path
        self.ensure_storage_directory()
    
    def ensure_storage_directory(self):
        """Asegura que el directorio de almacenamiento existe"""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)
    
    def save_data(self, key: str, data: Any) -> bool:
        """
        Guarda datos en el almacenamiento local
        
        Args:
            key: Clave única para identificar los datos
            data: Datos a guardar (deben ser serializables a JSON)
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        """
        try:
            file_path = os.path.join(self.storage_path, f"{key}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando datos para la clave '{key}': {e}")
            return False
    
    def load_data(self, key: str, default: Any = None) -> Any:
        """
        Carga datos del almacenamiento local
        
        Args:
            key: Clave única para identificar los datos
            default: Valor por defecto si no se encuentran los datos
        
        Returns:
            Los datos cargados o el valor por defecto
        """
        try:
            file_path = os.path.join(self.storage_path, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Error cargando datos para la clave '{key}': {e}")
            return default
    
    def delete_data(self, key: str) -> bool:
        """
        Elimina datos del almacenamiento local
        
        Args:
            key: Clave única para identificar los datos
        
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            file_path = os.path.join(self.storage_path, f"{key}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error eliminando datos para la clave '{key}': {e}")
            return False
    
    def list_keys(self) -> list:
        """
        Lista todas las claves disponibles en el almacenamiento
        
        Returns:
            list: Lista de claves disponibles
        """
        try:
            keys = []
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    keys.append(filename[:-5])  # Remover la extensión .json
            return keys
        except Exception as e:
            print(f"Error listando claves: {e}")
            return []
    
    def clear_all(self) -> bool:
        """
        Limpia todo el almacenamiento local
        
        Returns:
            bool: True si se limpió exitosamente, False en caso contrario
        """
        try:
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.storage_path, filename)
                    os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error limpiando almacenamiento: {e}")
            return False

class AppState:
    """
    Gestor del estado de la aplicación
    """
    
    def __init__(self, storage: LocalStorage):
        self.storage = storage
        self._state = self.load_state()
    
    def load_state(self) -> Dict[str, Any]:
        """Carga el estado desde el almacenamiento local"""
        return self.storage.load_data("app_state", {
            "user": None,
            "current_route": "login",
            "theme": "light",
            "language": "es",
            "preferences": {}
        })
    
    def save_state(self) -> bool:
        """Guarda el estado actual en el almacenamiento local"""
        return self.storage.save_data("app_state", self._state)
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Obtiene el usuario actual"""
        return self._state.get("user")
    
    def set_user(self, user: Dict[str, Any]) -> bool:
        """Establece el usuario actual"""
        self._state["user"] = user
        return self.save_state()
    
    def clear_user(self) -> bool:
        """Limpia el usuario actual"""
        self._state["user"] = None
        return self.save_state()
    
    def get_current_route(self) -> str:
        """Obtiene la ruta actual"""
        return self._state.get("current_route", "login")
    
    def set_current_route(self, route: str) -> bool:
        """Establece la ruta actual"""
        self._state["current_route"] = route
        return self.save_state()
    
    def get_theme(self) -> str:
        """Obtiene el tema actual"""
        return self._state.get("theme", "light")
    
    def set_theme(self, theme: str) -> bool:
        """Establece el tema"""
        self._state["theme"] = theme
        return self.save_state()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Obtiene una preferencia específica"""
        return self._state.get("preferences", {}).get(key, default)
    
    def set_preference(self, key: str, value: Any) -> bool:
        """Establece una preferencia específica"""
        if "preferences" not in self._state:
            self._state["preferences"] = {}
        self._state["preferences"][key] = value
        return self.save_state()
    
    def is_logged_in(self) -> bool:
        """Verifica si hay un usuario logueado"""
        return self._state.get("user") is not None
