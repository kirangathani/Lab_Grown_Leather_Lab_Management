"""Class for all personnel"""
from typing import List
from pathlib import Path
import pandas as pd

class Person:
    DATABASE_PATH = Path.cwd() / "Databases" / "Personnel.csv"
    
    def __init__(self, id_number: str, first_name: str, last_name: str, database_path = DATABASE_PATH) -> None:
        """Done when a new person is registered onto the sytstem"""
        # Initialised variables
        self.id_number: str = id_number
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.DATABASE_PATH = database_path
        self.database = pd.read_csv(self.DATABASE_PATH, dtype=str)
        
        # Data held by class, added to by the user.
        self.supervised_by: List[str] = []
        self.supervisor_to: List[str] = []
        
    def add_supervisor(self, supervisor_id: str) -> None:
        self._reload_database()
        """Adds a supervisor"""    
        self._modify_database("supervised_by", self.id_number, supervisor_id)
        self._modify_database("supervisor_to", supervisor_id, self.id_number)
    
    def add_supervisee(self, supervisee_id: str) -> None:
        """Adds a supervisee"""
        self._reload_database()
        # modify the database for both employees:
        self._modify_database("supervisor_to", self.id_number, supervisee_id)
        self._modify_database("supervised_by", supervisee_id, self.id_number)
        print(f"Successfully added new supervisee and saved database.")
        
    def _modify_database(self, column_name: str, id_number: str, new_value, ) -> None:
        self._reload_database()
        try:
            # Get the actual value (not Series)
            current_value = self.database.loc[self.database["id_number"] == id_number, column_name].iloc[0]
        except IndexError:
            print(f"Person with id number: {id_number} does not yet exist! Please register them to database first.")
            return
        
        if pd.isna(current_value):
            new_database_entry = str(new_value)
        elif new_value in current_value.split("|"):
            # Don't change the entry in this scenario
            print(f"The database already has value {new_value} within column {column_name} in the database. We will leave as is.")
            return
        else:
            new_database_entry = f"{current_value}|{new_value}"
        
        self.database.loc[self.database["id_number"] == id_number, column_name] = new_database_entry
        self.database.to_csv(self.DATABASE_PATH, index=False)
    
    def register_person_in_database(self) -> None:
        """Responsible for putting the information of the new person into the database"""
        self._reload_database()
        data = {
            "id_number": self.id_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
                        
        if (self.database["id_number"] == self.id_number).any():
            print(f"{self.first_name} {self.last_name} already exists in database.")
            return
        
        print(f"This is the current database: {self.database}")
        
        self.database.loc[len(self.database) + 1] = data
        self.database.to_csv(self.DATABASE_PATH, index=False)
        print(f"Successful registration of {self.first_name} {self.last_name}")
        print(f"This is after adding the new person: \n{self.database}")
    
    def _reload_database(self) -> None:
        self.database = pd.read_csv(self.DATABASE_PATH, dtype=str)
    