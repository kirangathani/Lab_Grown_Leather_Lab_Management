"""This is where the client will run the software from"""
from datetime import datetime
import json

from Core import Experiment
from Core import Person

if __name__ == "__main__":
    
    # Able to add a supervisor and reciprate the supervision link between employees
    supervisee = Person(
        id_number="2332",
        first_name="Jake",
        last_name="Bison"
    )
    
    supervisor = Person(
        id_number="4526",
        first_name="Mark",
        last_name="Ranch"
    )
    
    supervisee.register_person_in_database()
    supervisor.register_person_in_database()
    
    supervisor.add_supervisee(supervisee.id_number)
    
    # Add experiments
    
    experiment = Experiment(
        id_number = "5372",
        existing_experiment=True,
    )
    
    experiment.add_reading(2.44)
    experiment.add_reading(2.65)
    
    print(json.dumps(experiment.database, indent=4))

    experiment.plot_growth_curve_from_existing_results()
    
    
    
    
    