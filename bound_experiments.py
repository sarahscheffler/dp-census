import apportionment as algs
import noise
import math

'''
Bounding the probability of the noise altering the apportionment using the method detailed in our report
'''

def bound_huntington_hill_laplace(epsilon, populations, number_of_seats, ignore=dict()):
    '''
    populations:      maps state code (two letters) to population of that state (number).
    number_of_seats:  number.
    ignore:           dict, if a state is in the dict, and is mapped to None, then it is ignored.
    Returns: (min_probability_of_staying_the_same), (max_probability_of_staying_the_same)
    '''
    A = algs.huntington_hill(populations, number_of_seats, ignore=ignore) # apportionment
    
    # list only states we should not ignore
    states = sorted([ s for s in populations.keys() if not (s in ignore and ignore[s] is None) ])

    probs = []
    pairs = [ (si, sj) for si in states for sj in states if A[si] > 1 and si != sj ] # cannot loose a seat if I only have 1 seat
    for i, j in pairs:
      pi = populations[i]
      pj = populations[j]

      si = float(A[i]) # last seat allocated to i
      sj = float(A[j] + 1) # first seat not allocated to j

      r = math.sqrt(si * (si-1)) / math.sqrt(sj * (sj-1))
      k = pj * r - pi
      
      prob = noise.laplace_difference_greater_than_k(epsilon, r, k)

      # probability that ci - r * cj < k
      probs.append(prob)

    return (min(probs), max(probs))


if __name__ == '__main__':
  from parse import *
  import sys

  years, total_population, state_population = parse_historical_populations()
  _, total_seats, state_seats = parse_historical_seats_apportioned()

  years = list(years)
  if len(sys.argv) > 2:
    years = map(int, sys.argv[2:])

  for year in sorted(years):
    print(year, bound_huntington_hill_laplace(epsilon, state_population[year], total_seats[year], ignore=state_seats[year]))

