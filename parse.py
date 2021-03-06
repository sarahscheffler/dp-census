import csv
from states import STATE_ORDER, ABBR_TO_NAME, NAME_TO_ABBR

POPULATIONS_FILE = "census_data/historical_populations.csv"
APPORTIONMENT_FILE = "census_data/house_apportionments.csv"

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
