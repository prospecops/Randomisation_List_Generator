import csv
import numpy as np
from scipy.stats import chisquare, binom_test, binomtest, pearsonr
import collections

def check_randomness(filename):
    # Initialize the data lists
    treatments = []
    types = []
    cohorts = []

    # Load the randomization list
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            treatments.append(row[2])  # Treatment column
            cohorts.append(int(row[4]))  # Cohort column
            types.append(row[3])  # Type column

    treatments = np.array(treatments)
    cohorts = np.array(cohorts)
    types = np.array(types)

    # Frequency test per cohort
    for cohort in np.unique(cohorts):
        for t in np.unique(types):
            cohort_treatment_type = treatments[(cohorts == cohort) & (types == t)]
            unique, counts = np.unique(cohort_treatment_type, return_counts=True)
            treatment_counts = dict(zip(unique, counts))
            print(f"Frequency Test for Cohort {cohort}, Type {t}: {treatment_counts}")
            # Binomial test for each cohort
            p_binom = binomtest(treatment_counts['PT00114'], sum(treatment_counts.values()), 0.5 if t == 'Sentinel' else 0.75)
            print(f"Binomial Test for Cohort {cohort} ({t}): p = {p_binom.pvalue}")

            # Chi-square test for sentinel and non-sentinel blocks
            observed_frequencies = collections.Counter(cohort_treatment_type)
            if t == 'Sentinel':
                expected_frequencies = [1, 1]
            else:
                expected_frequencies = [1, 3]
            chi2, p_chi2 = chisquare(list(observed_frequencies.values()), expected_frequencies)
            print(f"Chi-square Test for Cohort {cohort}, Type {t}: chi2 = {chi2}, p = {p_chi2}")

    # Autocorrelation test for the whole experiment
    binary_treatments = (treatments == 'PT00114').astype(int)  # Convert treatments to binary values
    treatment_lags = np.roll(binary_treatments, 1)
    treatment_lags[0] = binary_treatments[-1]  # Handle the lagged value for the first treatment
    r, p_corr = pearsonr(binary_treatments, treatment_lags)
    print(f"Autocorrelation Test: r = {r}, p = {p_corr}")

if __name__ == "__main__":
    filename = input("Please enter the filename of your randomization list: ")
    check_randomness(filename)

