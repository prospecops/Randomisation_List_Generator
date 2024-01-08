import datetime
import os
import csv
import numpy as np
import glob

dosages = [125, 250, 500, 750, 1000]
drug = 'PT00114'
dir_path = os.getcwd()

def randomize_cohort(drug, dosage, cohort, rng, start_seq, is_replacement):
    patients = []
    treatments = ['Placebo'] * 2 + [drug] * 4
    rng.shuffle(treatments)
    for i in range(6):
        treatment = treatments[i]
        treatment_id = dosages.index(dosage) + 1 if treatment != 'Placebo' else 6
        randomization_sequence = start_seq + i
        patients.append([1, treatment, 1, is_replacement, randomization_sequence,
                         '', '', '',
                         treatment_id, cohort])
    return patients

def generate_randomization_list(seed=None):
    if seed is None:
        seed = int(datetime.datetime.now().timestamp())

    rng = np.random.default_rng(seed)
    randomization_list = []
    start_seq = 6001
    is_replacement = 0

    # Loop twice for the two sets of randomizations
    for round in range(2):
        if round == 1:
            is_replacement = 1
            start_seq = 7001

        for i in range(60):  # Generate 60 rows
            cohort = (i // 12) + 1
            randomization_list.extend(randomize_cohort(drug, dosages[cohort - 1], cohort, rng, start_seq, is_replacement))
            start_seq += 6

    # Create a directory for the new randomization list and seed
    latest_index = len(glob.glob(os.path.join(dir_path, "rand_list*")))
    new_dir = os.path.join(dir_path, f"rand_list{latest_index}")
    os.makedirs(new_dir, exist_ok=True)

    # Write the randomization list to CSV
    with open(os.path.join(new_dir, f"randomization_list{latest_index}.csv"), 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ListID", "Treatment", "IsTestData", "IsReplacement", "RandomizationSequence",
                         "PatientID", "ReplacementPatientID", "CenterID", "TreatmentID", "Block", "Cohort"])
        for row in randomization_list[:120]:  # Limit to 120 rows
            writer.writerow(row)

    # Write the seed to a new file
    with open(os.path.join(new_dir, f"Seed{latest_index}.txt"), 'w') as file:
        file.write(str(seed))


def recreate_randomization_list():
    # Ask for the seed file
    seed_file = input("Please enter the name of the seed file (e.g., Seed1): ")

    # Extract the number from the seed file name
    index = ''.join(filter(str.isdigit, seed_file))

    # Open the seed file and read the seed
    with open(glob.glob(f"rand_list*/{seed_file}.txt")[0], 'r') as file:
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

