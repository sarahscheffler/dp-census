import csv
import numpy as np
from states import STATE_ORDER, ABBR_TO_NAME, NAME_TO_ABBR
from apportionment import huntington_hill

EPSILONS = [10**x for x in range(-1, -6, -1)]
REPS = 10

POPULATIONS_FILE = "census_data/historical_populations.csv"
APPORTIONMENT_FILE = "census_data/house_apportionments.csv"

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

# TEMPORARY NOISE FUNCTION
def laplace_noise(dims, epsilon):
    # 1/epsilon because GS of count is 1
    return np.random.laplace(scale= 1/epsilon, size = dims)

def run_experiment():
    census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
    census_years, total_seats_apportioned, state_seats_apportioned = parse_historical_seats_apportioned(APPORTIONMENT_FILE)
    for year in census_years:
        print("=================================")
        for epsilon in EPSILONS:
            print("---------------------------------")
            true_population = total_us_pop[year]
            true_state_pop = state_pops[year]
            true_seats = total_seats_apportioned[year]
            true_answer = huntington_hill(true_population, true_state_pop, true_seats)

            if any(count is None for count in true_state_pop.values()):
                print("Not doing year %d because there is a None count" % year)
                continue

            for rep in range(REPS):
                noises = laplace_noise(len(true_state_pop), epsilon)
                population = true_population + sum(noises)
                state_pop = dict()
                counter = 0 # todo gross
                for state in true_state_pop.keys():
                    state_pop[state] = true_state_pop[state] + noises[counter]
                    counter += 1
                answer = huntington_hill(population, state_pop, true_seats)
                if true_answer != answer:
                    print("epsilon: %f, year: %d, rep: %d, Different" % (epsilon, year, rep))
                    for state in true_answer:
                        if true_answer[state] != answer[state]:
                            print("Expected answer: ", state, true_answer[state])
                            print("Actual answer: ", state, answer[state])
                else:
                    print("epsilon: %f, year: %d, rep: %d, Same" % (epsilon, year, rep))

run_experiment()


                




if __name__ == '__main__':
    census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
    census_years, total_seats_apportioned, state_seats_apportioned = parse_historical_seats_apportioned(APPORTIONMENT_FILE)

    #print(census_years)
    #print(total_seats_apportioned)
    #print(state_seats_apportioned)

