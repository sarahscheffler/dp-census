'''
Functions that implement interesting apportionment functions
'''
import math


# Hutington Hill's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-hills-method-of-apportionment
def oneshot_huntington_hill(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state. (oneshot method, modifies divisor D until it works)
    '''

    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = float(total_population) / float(number_of_seats)

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
            cel = math.ceil(quota)

            # round according to geometric mean
            geomean = math.sqrt(flr * cel)
            apportionment = cel if quota > geomean else flr

            total += apportionment
            quotas[state] = int(apportionment)

        return (total, quotas)

    gone_up = False
    gone_down = False
    while not gone_up or not gone_down:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        # else: go up/down until we find new D
        elif total < number_of_seats:
            gone_down = True
            D = D - 1
        else:
            gone_up = True
            D = D + 1

    # if we were "bouncing" then binary search to find new D
    lower_D = D - 1
    higher_D = D + 1
    while True:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        elif total < number_of_seats:
            higher_D = D
            D = (D + lower_D) / 2
        else:
            lower_D = D
            D = (D + higher_D) / 2

def iter_huntington_hill(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state (iterating over seats method)
    '''

    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    apportionments = {}
    for state,population in populations.items():
        if population is not None and (state not in ignore or ignore[state] is not None):
            apportionments[state] = 1 #everyone gets at least one seat, avoids div by 0

    priorities = {}
    for seat in range(number_of_seats - sum(apportionments.values())):
        for state in apportionments.keys():
            if populations[state] is None or (state in ignore and ignore[state] is not None):
                continue
            priorities[state] = populations[state] / math.sqrt(apportionments[state] * (apportionments[state]+1))
        apportionments[ max(priorities.keys(), key=(lambda state: priorities[state])) ] += 1

    total = sum(apportionments.values())
    if total == number_of_seats:
        for state in populations.keys():
            if state not in apportionments.keys():
                apportionments[state] = None
        return apportionments

def huntington_hill(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    # iter is faster than oneshot
    return iter_huntington_hill(total_population, populations, number_of_seats, ignore)


# Webster's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-websters-method-of-apportionment
def webster(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = total_population / float(number_of_seats)

    def iter(D):
        quotas = dict()
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            quota = population / D
            apportionment = round(quota)

            total += apportionment
            quotas[state] = int(apportionment)

        return (total, quotas)

    gone_up = False
    gone_down = False
    while not gone_up or not gone_down:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        # else: go up/down until we find new D
        elif total < number_of_seats:
            gone_down = True
            D = D - 1
        else:
            gone_up = True
            D = D + 1

    # if we were "bouncing" then binary search to find new D
    lower_D = D - 1
    higher_D = D + 1
    while True:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        elif total < number_of_seats:
            higher_D = D
            D = (D + lower_D) / 2
        else:
            lower_D = D
            D = (D + higher_D) / 2



# Dean's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-deans-method-of-apportionment
def dean(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = total_population / float(number_of_seats)

    def iter(D):
        quotas = dict()
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            quota = population / D
            flr = math.floor(quota)
            cel = math.ceil(quota)

            # round according to harmonic mean
            harmonicmean = (flr*(cel))/(flr+0.5)
            apportionment = cel if quota > harmonicmean else flr

            total += apportionment
            quotas[state] = int(apportionment)

        return (total, quotas)

    gone_up = False
    gone_down = False
    while not gone_up or not gone_down:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        # else: go up/down until we find new D
        elif total < number_of_seats:
            gone_down = True
            D = D - 1
        else:
            gone_up = True
            D = D + 1

    # if we were "bouncing" then binary search to find new D
    lower_D = D - 1
    higher_D = D + 1
    while True:
        total, quotas = iter(D)
        if total == number_of_seats:
            return quotas
        elif total < number_of_seats:
            higher_D = D
            D = (D + lower_D) / 2
        else:
            lower_D = D
            D = (D + higher_D) / 2




# Hamilton's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-hamiltons-method-of-apportionment
def hamilton(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''

    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = total_population / float(number_of_seats)

    def iter(D):
        quotas = dict()
        remainders = []
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            # first assign seats based on a rounded down state quota
            # and keep the remainder
            quota = population / D
            apportionment = math.floor(quota)
            remainder = quota - apportionment

            total += apportionment
            quotas[state] = int(apportionment)
            remainders.append((remainder,state))

        return (total, quotas, remainders)

    total, quotas, remainders = iter(D)

    print(total)
    print("ns: ", number_of_seats)

    #if there are no surplus of seats
    #then we are done
    if total == number_of_seats:
        return quotas

    #assign the surplus of seats to the states
    #with the largest remainders
    elif total < number_of_seats:
        surplus = number_of_seats - total
        remainders.sort(reverse=True)

        for r,s in remainders:
            if(surplus > 0 and r > 0):
                if(r > 0):
                    quotas[s] += 1
                    surplus -=1
            else:
                return  quotas

# Lowndes's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-lowndes-method-of-apportionment
def lowndes(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = total_population / float(number_of_seats)

    def iter(D):
        quotas = dict()
        remainders = []
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            # first assign seats based on a rounded down state quota
            # and keep the relative fraction part:
            #  fractional of quota divided by floor(quota)
            quota = population / D
            
            apportionment = math.floor(quota)
            apportionment = apportionment if apportionment>0 else 1

            remainder = (quota - apportionment) / apportionment

            total += apportionment
            quotas[state] = int(apportionment)
            remainders.append((remainder,state))

        return (total, quotas, remainders)

    total, quotas, remainders = iter(D)

    #if there are no surplus of seats
    #then we are done
    if total == number_of_seats:
        return quotas

    #assign the surplus of seats to the states
    #with the largest remainders
    elif total < number_of_seats:
        surplus = number_of_seats - total
        remainders.sort(reverse=True)

        for r,s in remainders:
            if(surplus > 0 and r > 0):
                if(r > 0):
                    quotas[s] += 1
                    surplus -=1
            else:
                return  quotas



# Jefferson's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-jeffersons-method-of-apportionment
def jefferson(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = total_population / float(number_of_seats)
    d = 0
    # A single iteration of jefferson, computes for a given ratio D and a given divisor adjustment d
    # and returns resulting quotas and total number of apportioned seats
    def iter(D, d):
        quotas = dict()
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            quota = population / (D - d)
            apportionment = math.floor(quota)

            total += apportionment
            quotas[state] = int(apportionment)

        return (total, quotas)

    while True:
        total, quotas = iter(D, d)
        if total == number_of_seats:
            return quotas
        elif total < number_of_seats:
            d = d - 1
        else:
            d = d + 1

# Adam's method https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-adams-method-of-apportionment
# "Inverted Jefferson"
def adam(total_population, populations, number_of_seats, ignore=dict()):
    '''
    total_population: number: total population of the United States.
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    Returns: a map from state codes to seats allocated to that state.
    '''
    total_population = sum([0 if (population is None or (state in ignore and ignore[state] is None)) else population for state,population in populations.items()])
    D = total_population / float(number_of_seats)
    d = 0
    # A single iteration of jefferson, computes for a given ratio D and a given divisor adjustment d
    # and returns resulting quotas and total number of apportioned seats
    def iter(D, d):
        quotas = dict()
        total = 0
        for state, population in populations.items():
            if population is None or (state in ignore and ignore[state] is None):
                quotas[state] = None
                continue;

            quota = population / (D + d)
            apportionment = math.floor(quota)

            total += apportionment
            quotas[state] = int(apportionment)

        return (total, quotas)

    while True:
        total, quotas = iter(D, d)
        if total == number_of_seats:
            return quotas
        elif total < number_of_seats:
            d = d - 1
        else:
            d = d + 1


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

        actual_output = lowndes(total_population[year], state_population[year], total_seats[year], ignore=state_seats[year])
        if len(sys.argv) > 1:
            for key in sorted(actual_output.keys()):
                print(key, actual_output[key], state_seats[year][key], '' if actual_output[key] == state_seats[year][key] else '----------------')
        else:
            print(year, actual_output == state_seats[year])
