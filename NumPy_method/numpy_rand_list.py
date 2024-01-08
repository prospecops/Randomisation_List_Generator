import csv
import numpy as np
import os
import datetime
import glob

def randomize_cohort(start_id, drug, dosage, cohort, rng):
    patients = []

    # Randomize sentinel dosing
    sentinel = ['Placebo', drug] if rng.choice([0, 1]) else [drug, 'Placebo']
    patients.extend([(start_id + i, dosage, sentinel[i], "Sentinel", cohort) for i in range(2)])

    # Randomize the rest of the cohort
    rest = ['Placebo'] + [drug]*3
    rng.shuffle(rest)
    patients.extend([(start_id + 2 + i, dosage, rest[i], "Not Sentinel", cohort) for i in range(4)])

    return patients

def generate_randomization_list(seed=None):
    # Initialize starting ID and drug
    start_id = 81001
    drug = 'PT00114'

    # Set dosages for each cohort
    dosages = [125, 250, 500, 750, 1000]

    # Use provided seed or generate a new one based on current time
    if seed is None:
        seed = int(datetime.datetime.now().timestamp())

    # Create a random number generator with the seed
    rng = np.random.default_rng(seed)

    # Generate randomization list
    randomization_list = []
    for cohort, dosage in enumerate(dosages, 1):
        randomization_list.extend(randomize_cohort(start_id, drug, dosage, cohort, rng))
        start_id += 6  # Increment starting ID for the next cohort

    # Get the latest index for randomization list and seed
    latest_index = len(glob.glob("NumPy_method/rand_list*")) + 1

    # Create directory for new randomization list and seed
    os.makedirs(f'NumPy_method/rand_list{latest_index}', exist_ok=True)

    # Write randomization list to CSV
    with open(f'NumPy_method/rand_list{latest_index}/randomization_list{latest_index}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject ID", "Dosage (μg)", "Treatment", "Type", "Cohort"])  # Write headers
        for row in randomization_list:
            writer.writerow(row)

    # Write seed to a new file
    with open(f'NumPy_method/rand_list{latest_index}/Seed{latest_index}.txt', 'w') as file:
        file.write(str(seed))

def recreate_randomization_list():
    # Ask for the seed file
    seed_file = input("Please enter the name of the seed file (e.g., Seed1): ")

    # Extract the number from the seed file name
    index = ''.join(filter(str.isdigit, seed_file))

    # Open the seed file and read the seed
    with open(f'NumPy_method/rand_list{index}/{seed_file}.txt', 'r') as file:
        seed = int(file.read())

    # Generate a randomization list using the read seed
    generate_randomization_list(seed)

if __name__ == "__main__":
    action = input("Do you want to create a new list or recreate a list from an existing seed? (new/recreate): ")

    if action.lower() == 'new':
        generate_randomization_list()
    elif action.lower() == 'recreate':
        recreate_randomization_list()
    else:
        print("Invalid input. Please type 'new' or 'recreate'.")
