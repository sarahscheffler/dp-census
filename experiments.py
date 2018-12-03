import csv
import numpy as np
from states import STATE_ORDER, ABBR_TO_NAME, NAME_TO_ABBR
from apportionment import huntington_hill, webster, dean, hamilton, lowndes, jefferson, adam
from noise import poisson_noise, laplace_noise, geometric_noise, gaussian_noise

EPSILONS = [10**x for x in range(-1, -6, -1)]
DELTAS = [10**x for x in range(-4, -20, -4)]
CS = range(1, 11, 2)
REPS = 100

POPULATIONS_FILE = "census_data/historical_populations.csv"
APPORTIONMENT_FILE = "census_data/house_apportionments.csv"
OUTPUT_FOLDER = "results"
VERBOSE = False

apportionments = {"hh": huntington_hill, "webster": webster, "dean": dean, "hamilton": hamilton, "lowndes": lowndes,
        "jefferson": jefferson, "adam": adam}
mechanisms = { "poisson": poisson_noise, "laplace": laplace_noise, "geometric": geometric_noise, "gaussian": gaussian_noise}

#########################################################
# Parsing functions
#########################################################

def parse_historical_populations(filename=POPULATIONS_FILE):
    census_years = []
    total_us_pop = []
    state_pops = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        # parse first row separately
        census_years = list(map(int, next(reader)[1:-3]))
        total_us_pop = dict(zip(census_years, list(map(int, next(reader)[1:-3]))))
        state_pops = dict()

        for row in reader:
            name = row[0]
            abbr = NAME_TO_ABBR[name]

            # Manually skip District of Columbia becasue they don't have seats in the house
            if abbr == 'DC':
                continue

            for i in range(len(row[1:-3])):
                year = census_years[i]
                popstr = row[1:-3][i]
                if year not in state_pops.keys():
                    state_pops[year] = dict()
                state_pops[year][abbr] = None if len(popstr)==0 else int(popstr)

    return set(census_years), total_us_pop, state_pops

def parse_historical_seats_apportioned(filename=APPORTIONMENT_FILE):
    census_years = []
    total_seats_apportioned = []
    state_seats_apportioned = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        census_years = list(map(int, next(reader)[1:]))
        total_seats_apportioned = { year: 0 for year in census_years }
        state_seats_apportioned = { year: dict() for year in census_years }
        for row in reader:
            name = row[0]
            for i in range(len(row[1:])):
                year = census_years[i]
                seats = row[1:][i]
                state_seats_apportioned[year][name] = None if seats=='-' else int(seats)
                total_seats_apportioned[year] += 0 if seats=='-' else int(seats)

    # Manually add 1920 (equal to 1910 reult) and 2017 (equal to 2010 result)
    census_years.append(1920)
    census_years.append(2017)
    census_years.sort()

    total_seats_apportioned[1920] = total_seats_apportioned[1910]
    total_seats_apportioned[2017] = total_seats_apportioned[2010]

    state_seats_apportioned[1920] = dict(state_seats_apportioned[1910])
    state_seats_apportioned[2017] = dict(state_seats_apportioned[2010])

    return set(census_years), total_seats_apportioned, state_seats_apportioned

#########################################################
# Experiments
#########################################################

def run_experiment(apportion_alg_name, count_mech_name):
    # Writes a function that returns the changes that must be made TO THE TRUE APPORTIONMENT in order to equal the
    # NOISY RESULT

    # TODO temporary - we already have results for hh, just move on
    if apportion_alg_name == "hh":
        return

    print("++++++++++++++++++++++++++++++++++++")
    print("apportionment algorithm: ", apportion_alg_name)
    print("count DP mechanism: ", count_mech_name)
    print("++++++++++++++++++++++++++++++++++++")

    apportionment_alg = apportionments[apportion_alg_name]
    count_mechanism = mechanisms[count_mech_name]

    census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
    census_years, total_seats_apportioned, state_seats_apportioned = parse_historical_seats_apportioned(APPORTIONMENT_FILE)

    for year in census_years:
        print("year: ", str(year))
        if VERBOSE: print("=================================")

        true_population = total_us_pop[year]
        true_state_pop = state_pops[year]
        true_seats = total_seats_apportioned[year]
        true_answer = apportionment_alg(true_population, true_state_pop, true_seats)

        output_file = OUTPUT_FOLDER + "/" + apportion_alg_name + "/" + count_mech_name + "/" + str(year) + ".csv"
        with open(output_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["apportionment","mechanism", "epsilon", "rep"] + STATE_ORDER)

            for epsilon in EPSILONS:
                print("  epsilon: ", str(epsilon))
                if VERBOSE: print("---------------------------------")

                deltas = DELTAS if count_mech_name == "gaussian" else [None]
                for delta in deltas:
                    print("    delta: ", str(delta))
                    if VERBOSE: print("  ---------------------------------")

                    for rep in range(REPS):
                        noises = count_mechanism(epsilon, delta, len(true_state_pop)) if count_mech_name == "gaussian" else count_mechanism(epsilon, len(true_state_pop))
                        population = true_population + sum(noises)
                        state_pop = dict()
                        for (state, i) in zip(true_state_pop.keys(), range(len(true_state_pop))):
                            state_pop[state] = true_state_pop[state] + noises[i] if true_state_pop[state] is not None else None
                        answer = apportionment_alg(population, state_pop, true_seats)

                        if true_answer != answer:
                            if VERBOSE: print("alg: %s, mech: %s, epsilon: %f, year: %d, rep: %d, Different" %
                                    (apportion_alg_name, count_mech_name, epsilon, year, rep))
                            for state in true_answer:
                                if true_answer[state] != answer[state]:
                                    diff = answer[state] - true_answer[state]
                                    if VERBOSE: print("    ", state, "+" if diff > 0 else " " if diff == 0 else "", diff)
                        else:
                            if VERBOSE: print("alg: %s, mech: %s, epsilon: %f, year: %d, rep: %d, Same" %
                                    (apportion_alg_name, count_mech_name, epsilon, year, rep))

                        writer.writerow([apportion_alg_name, count_mech_name, epsilon, rep] + [answer[st] - true_answer[st] for st in filter(lambda st: true_answer[st] is
                            not None, STATE_ORDER)])
    print("Done!  Results are in ", OUTPUT_FOLDER)


if __name__ == '__main__':
    census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
    census_years, total_seats_apportioned, state_seats_apportioned = parse_historical_seats_apportioned(APPORTIONMENT_FILE)

    for aa in apportionments.keys():
        for cm in mechanisms.keys():
            if cm == "poisson":
                continue # skip for now
            run_experiment(aa, cm)

    #print(census_years)
    #print(total_seats_apportioned)
    #print(state_seats_apportioned)

