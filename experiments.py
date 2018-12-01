import csv
from states import STATE_ORDER, ABBR_TO_NAME, NAME_TO_ABBR

POPULATIONS_FILE = "census_data/historical_populations.csv"

def parse_historical_populations(filename):
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
            for i in range(len(row[1:-3])):
                year = census_years[i]
                popstr = row[1:-3][i]
                if year not in state_pops.keys():
                    state_pops[year] = dict()
                state_pops[year][abbr] = None if len(popstr)==0 else int(popstr)

    return census_years, total_us_pop, state_pops

census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
print(census_years)
print(total_us_pop)
print(state_pops)

