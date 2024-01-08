import csv
import random


# Function to randomize treatment for each cohort
def randomize_cohort(start_id, drug, dosage, block):
    patients = []

    # Randomize sentinel dosing
    sentinel = ['Placebo', drug] if random.randint(0, 1) else [drug, 'Placebo']
    patients.extend([(start_id + i, dosage, sentinel[i], "Sentinel", block) for i in range(2)])

    # Randomize the rest of the cohort
    rest = ['Placebo'] + [drug] * 3
    random.shuffle(rest)
    patients.extend([(start_id + 2 + i, dosage, rest[i], "Not Sentinel", block) for i in range(4)])

    return patients


def generate_randomization_list():
    # Initialize starting ID and drug
    start_id = 81001
    drug = 'PT00114'

    # Set dosages for each cohort
    dosages = [125, 250, 500, 750, 1000]

    # Generate randomization list
    randomization_list = []
    for block, dosage in enumerate(dosages, 1):
        randomization_list.extend(randomize_cohort(start_id, drug, dosage, block))
        start_id += 6  # Increment starting ID for the next cohort

    # Write randomization list to CSV
    with open('randomization_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject ID", "Dosage (μg)", "Treatment", "Type", "Block"])  # Write headers
        for row in randomization_list:
            writer.writerow(row)


if __name__ == "__main__":
    generate_randomization_list()
