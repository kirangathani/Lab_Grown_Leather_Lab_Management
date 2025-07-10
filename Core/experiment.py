"""class for every experiment inherits from"""
from typing import List
from datetime import datetime
from pathlib import Path 
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

class Experiment:
    DATABASE_PATH = Path.cwd() / "Databases" / "Experiments.json"
    
    def __init__(self, id_number: str, existing_experiment: bool = False, start_time: str = None, end_time: str = None, operators: List = [], database_path: Path = DATABASE_PATH) -> None:
        """This is what is done at the start of the experiment. To load an existing experiment, use the `existing_experiment=True` kwarg"""
        
        # Do this regardless
        self.id_number: str = id_number
        self.DATABASE_PATH: Path = database_path
        
        # Loading or initialising the database (needed only for first time)
        try:
            with open(self.DATABASE_PATH, "r") as file:
                self.database: dict = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # File doesn't exist or is empty - create empty database
            self.database = {}
        
        # Part of the initialisation dependant on whether exp is new.
        if existing_experiment:
            self._load_existing_experiment()
        else:
            # if exp is new, lets initialise!
            self.database[id_number] = {}
            self.start_time: str = start_time
            self.end_time: str = end_time
            self.operators: List = operators # Order of operatros in the list == relative proximity to the bioreactor run
            
            # Save initialised values to the database.
            self.database[self.id_number]["start_time"] = start_time
            self.database[self.id_number]["end_time"] = end_time
            self.database[self.id_number]["operators"] = operators
            self.database[self.id_number]["results"] = []
            
            with open(self.DATABASE_PATH, "w") as file:
                json.dump(self.database, file, indent=4)
    
                
        # Added attributes
        self.reading: float # This is what the scientist will input each day. We should add the time to this as another element in the tuple then append the tuple to the results for graphing. 
    
    def add_reading(self, reading: float):
        """Use this function to add a reading"""
        self.reading = reading
        self._add_daily_result_to_total()
        print(f"Reading added!")

    def _add_daily_result_to_total(self):
        """Responsible fro appending the daily result to the overall result list"""
        self._reload_database()
        self.database[self.id_number]["results"].append((self.reading, datetime.now().strftime("%Y%m%d%H%M%S"))) 
        
        # Save to file after appending
        with open(self.DATABASE_PATH, "w") as file:
            json.dump(self.database, file, indent=4)
        
        print(f"Have added result: {self.reading} to the results section for the experiment. Here is the total results thus far: {self.database[self.id_number]["results"]}")
        
    def _reload_database(self):
        """If experiment in the database, will load. Searches by id."""
        with open(self.DATABASE_PATH, "r") as file:
            self.database = json.load(file)
    
    def _load_existing_experiment(self):
        """If we already have the experiment existing, then lets load in the data"""
        self._reload_database()    
        if self.id_number in self.database:
            self.start_time = self.database[self.id_number]["start_time"]
            self.end_time = self.database[self.id_number]["end_time"]
            self.operators = self.database[self.id_number]["operators"]
        else:
            raise KeyError(f"existing experiment was selected as true, but we have no experiment in database matching id number: {self.id_number}")
        print(f"Successfully loaded existing experiment. ID number: {self.id_number}")
        
    def save_to_database(self):
        """Save database to Databases folder"""
        print(f"THis is what we are saying")
        print(json.dumps(self.database, indent=4))
        with open(self.DATABASE_PATH, "w") as file:
            json.dump(self.database, file, indent=4)
        self._reload_database()
        print("Saved to the experiments database successfully.")

    def plot_growth_curve_from_existing_results(self):
        """Plot a simple growth curve using matplotlib from existing results"""
        # Check if results exist and are not empty
        if not self.database[self.id_number]["results"]:
            print("No data available to plot. Please add some readings first.")
            raise ValueError("Cannot plot growth curve with no data")
        
        results = self.database[self.id_number]["results"]
        y_values = [result[0] for result in results] # Cell density values
        time_strings = [result[1] for result in results]  
        
        x_values = [datetime.strptime(time_str, "%Y%m%d%H%M%S") for time_str in time_strings]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker='o', linestyle='-', linewidth=2, markersize=6)
        
        plt.xlabel("Time")
        plt.ylabel("Cell Density")
        plt.title(f"Growth Curve for Experiment {self.id_number}")
        
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.show()
    
    
    
    