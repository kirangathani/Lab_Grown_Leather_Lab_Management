# This is a lab grown leather lab management tool

# Instructions:

## General
 - Make sure you install `requirements.txt`! (`pip install requirements.txt`)
 - Make sure you only run code in `client_window.py`

## Person Registration
To register a new person, just initialise an instance of the person class with a chosen ID. Call the `register_person_in_database()` method
To connect this person to a particular supervisor or supervisee, use the `.add_supervisor()` or the `.add_supervisee()` method, respectively. The programme will reciprocally add this person as a supervisee/supervisor to the entry for the other person in the database.

```python
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
```

## Experiment Creation
To create an experiment, initialise an instance of the experiment class. Initialise it with the variables you like:

```python
experiment = Experiment(
    id_number = "5372",
    existing_experiment=False,
    operators = ["2332", "4526"]
)

experiment.add_reading(2.44)
experiment.add_reading(2.65)

# Print the database entry:
print(json.dumps(experiment.database[experiment.id_number], indent=4))

# Show a growth cuvre for the experiment
experiment.plot_growth_curve_from_existing_results()
```
