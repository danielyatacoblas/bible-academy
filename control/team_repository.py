from .base_repository import BaseRepository
from model.team import Team

class TeamRepository(BaseRepository):
    def __init__(self, conn=None):
        super().__init__("team", conn)

    def create_table(self):
        """
            Create the table 'team' if it does not exist.

            Columns:
                id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier of the team.
                name (VARCHAR(100)): Name of the team.
                age_start (INTEGER): Starting age for the team.
                age_end (INTEGER): Ending age for the team.
                gender (VARCHAR(10)): Gender of the team.
            
            Returns:
                None
        """
        columns = """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            age_start INTEGER,
            age_end INTEGER,
            gender VARCHAR(10)
        """
        return super().create_table(columns)
    
    def create_team(self, team: Team) -> Team:
        """
        Create a new team in the database.
        
        Args:
            team (Team): Team instance to create
            
        Returns:
            Team: Created team with assigned ID
        """
        try:
            team_data = team.to_dict()
            # Remove id for insertion
            team_data.pop("id", None)
            
            self.insert_row(team_data)
            
            # Get the last inserted ID
            if self.conn and self.cursor:
                team.id = self.cursor.lastrowid
            else:
                # If no connection, get the last inserted ID
                conn = self._get_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT last_insert_rowid()")
                    team.id = cursor.fetchone()[0]
                    conn.close()
                else:
                    raise Exception("No se pudo obtener conexión a la base de datos")
            
            return team
        except Exception as e:
            print(f"Error creating team: {e}")
            raise
    
    def update_team(self, team: Team) -> bool:
        """
        Update an existing team in the database.
        
        Args:
            team (Team): Team instance to update
            
        Returns:
            bool: True if update was successful
        """
        try:
            if not team.id:
                raise ValueError("Team ID is required for update")
            
            team_data = team.to_dict()
            # Remove id from update data
            team_data.pop("id", None)
            
            rows_affected = self.update_row(
                new_data=team_data,
                conditions={"id": team.id}
            )
            
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating team: {e}")
            raise
    
    def delete_team(self, team_id: int) -> bool:
        """
        Delete a team from the database.
        
        Args:
            team_id (int): ID of the team to delete
            
        Returns:
            bool: True if deletion was successful
        """
        try:
            rows_affected = self.delete_row({"id": team_id})
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting team: {e}")
            raise
    
    def get_team_by_id(self, team_id: int) -> Team:
        """
        Get a team by its ID.
        
        Args:
            team_id (int): ID of the team
            
        Returns:
            Team: Team instance or None if not found
        """
        try:
            team_data = self.get_row_value({"id": team_id})
            if team_data:
                return Team.from_dict(team_data)
            return None
        except Exception as e:
            print(f"Error getting team by ID: {e}")
            return None
    
    def get_all_teams(self) -> list[Team]:
        """
        Get all teams from the database.
        
        Returns:
            list[Team]: List of Team instances
        """
        try:
            teams_data = self.get_all_rows()
            return [Team.from_dict(team_data) for team_data in teams_data]
        except Exception as e:
            print(f"Error getting all teams: {e}")
            return []
    
    def search_teams(self, search_term: str) -> list[Team]:
        """
        Search teams by name.
        
        Args:
            search_term (str): Search term for team name
            
        Returns:
            list[Team]: List of matching Team instances
        """
        try:
            teams_data = self.get_all_rows({"name": search_term})
            return [Team.from_dict(team_data) for team_data in teams_data]
        except Exception as e:
            print(f"Error searching teams: {e}")
            return []
    
    def get_teams_by_gender(self, gender: str) -> list[Team]:
        """
        Get teams by gender.
        
        Args:
            gender (str): Gender to filter by
            
        Returns:
            list[Team]: List of Team instances with specified gender
        """
        try:
            teams_data = self.get_all_rows({"gender": gender})
            return [Team.from_dict(team_data) for team_data in teams_data]
        except Exception as e:
            print(f"Error getting teams by gender: {e}")
            return []
    
    def get_teams_by_age_range(self, min_age: int, max_age: int) -> list[Team]:
        """
        Get teams that overlap with the specified age range.
        
        Args:
            min_age (int): Minimum age
            max_age (int): Maximum age
            
        Returns:
            list[Team]: List of Team instances that overlap with the age range
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute("""
                    SELECT * FROM team 
                    WHERE (age_start <= ? AND age_end >= ?) 
                    OR (age_start <= ? AND age_end >= ?)
                    OR (age_start >= ? AND age_end <= ?)
                """, (max_age, min_age, max_age, min_age, min_age, max_age))
                teams_data = self.cursor.fetchall()
                columns = [description[0] for description in self.cursor.description]
            else:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT * FROM team 
                        WHERE (age_start <= ? AND age_end >= ?) 
                        OR (age_start <= ? AND age_end >= ?)
                        OR (age_start >= ? AND age_end <= ?)
                    """, (max_age, min_age, max_age, min_age, min_age, max_age))
                    teams_data = cursor.fetchall()
                    columns = [description[0] for description in cursor.description]
            
            if teams_data:
                if not columns:
                    columns = [f"col_{i}" for i in range(len(teams_data[0]))]
                teams_dict = [dict(zip(columns, row)) for row in teams_data] if columns else []
                return [Team.from_dict(team_data) for team_data in teams_dict]
            return []
        except Exception as e:
            print(f"Error getting teams by age range: {e}")
            return []
    
    def _get_connection(self):
        """Get database connection if not already set"""
        from control.bd.db_connection import Connection
        return Connection.connect()