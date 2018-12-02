'''
Functions that implement interesting apportionment functions
'''
import math


# Hutington Hill https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-hills-method-of-apportionment
def huntington_hill(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    D = total_population / float(number_of_seats)

    # A single iteration of huntington_hill, computes for a given ratio D
    # and returns resulting quotas and total number of apportioned seats
    def iter(D):
        quotas = dict()
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            quota = population / D
            flr = math.floor(quota)
            cel = math.ceil(quota) # should be different from flr if they're integers

            # round according to geometric mean
            geomean = math.sqrt(flr * cel)
            apportionment = cel if quota > geomean else flr

            total += apportionment
            quotas[state] = int(apportionment)

        return (total, quotas)

    while True:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        elif total < number_of_seats:
            D = D - 1
        else:
            D = D + 1

if __name__ == '__main__':
    from experiments import *
    import sys

    years, total_population, state_population = parse_historical_populations()
    _, total_seats, state_seats = parse_historical_seats_apportioned()

    domain = years
    if len(sys.argv) > 1:
        domain = map(int, sys.argv[1:])

    for year in sorted(domain):
        if year in [1920, 2017]: continue;

        actual_output = huntington_hill(total_population[year], state_population[year], total_seats[year], ignore=state_seats[year])
        if len(sys.argv) > 1:
            for key in sorted(actual_output.keys()):
                print(key, actual_output[key], state_seats[year][key], '' if actual_output[key] == state_seats[year][key] else '----------------')
        else:
            print(year, actual_output == state_seats[year])
