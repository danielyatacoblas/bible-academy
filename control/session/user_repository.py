from control.base_repository import BaseRepository
from control.utils.encrypt_password import encrypt_password, verify_password

class UserRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("user", conn)

    def create_table(self):
        """
            Create the table 'user' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the user.
                user (VARCHAR(100)): Username.
                role (VARCHAR(50)): Role of the user.
                password (VARCHAR(255)): Password of the user.
                created_at (DATETIME) DEFAULT CURRENT_TIMESTAP: Creation date and time of the user.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user VARCHAR(100),
            role VARCHAR(50),
            password VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        """
        return super().create_table(columns)
    
    def login(self, user: str, password: str):
        """
            Login a user.

            Args:
                user (str): Username.
                password (str): Password.

            Returns:
                True or Pass / False to no session.
        """
        user_data = super().get_row_value({"user":user})
        if user_data and verify_password(user_data["password"], password):
            #Password correct
            return True
        else:
            #User not exists or password incorrect
            return False


    def create_user(self, user: str, role: str, password: str):
        """
            Create a new user.

            Args:
                user (str): Username.
                role (str): Role of the user.
                password (str): Password of the user.

            Returns:
                None
        """
        hash = encrypt_password(password)
        super().insert_row({"user": user, "role": role, "password": hash})
    
    def get_user_by_username(self, username: str):
        """
            Get user data by username.

            Args:
                username (str): Username to search for.

            Returns:
                dict or None: User data if found, else None.
        """
        return super().get_row_value({"user": username})
    
    def get_all_users(self):
        """
            Get all users from the database.

            Returns:
                list[dict]: List of all users.
        """
        return super().get_all_rows()
    
    def update_user_password(self, username: str, new_password: str):
        """
            Update user password.

            Args:
                username (str): Username of the user.
                new_password (str): New password.

            Returns:
                int: Number of rows affected.
        """
        hashed_password = encrypt_password(new_password)
        return super().update_row(
            {"password": hashed_password}, 
            {"user": username}
        )
    
    def update_user_role(self, username: str, new_role: str):
        """
            Update user role.

            Args:
                username (str): Username of the user.
                new_role (str): New role.

            Returns:
                int: Number of rows affected.
        """
        return super().update_row(
            {"role": new_role}, 
            {"user": username}
        )
    
    def delete_user(self, username: str):
        """
            Delete user by username.

            Args:
                username (str): Username to delete.

            Returns:
                int: Number of rows affected.
        """
        return super().delete_row({"user": username})
    
    def user_exists(self, username: str):
        """
            Check if user exists.

            Args:
                username (str): Username to check.

            Returns:
                bool: True if user exists, False otherwise.
        """
        user_data = super().get_row_value({"user": username})
        return user_data is not None