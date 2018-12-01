'''
Functions that implement interesting apportionment functions
'''
import math


# Hutington Hill https://www.maa.org/press/periodicals/convergence/apportioning-representatives-in-the-united-states-congress-hills-method-of-apportionment
def hutington_hill(populations, number_of_seats):
  '''
  populations:      array containing objects on the form { name: <state_name>, population: <population_count> }
                    first tuple is for the entire US population.
  number_of_seats:  number.
  '''
  total_population = populations[0]['population']
  D = total_population / float(number_of_seats)
  populations = populations[1:]
  
  # A single iteration of hutington_hill, computes for a given ratio D
  # and returns resulting quotas and total number of apportioned seats
  def iter(D):
    quotas = []
    total = 0
    for state in populations:
      if state['name'] == 'District of Columbia':
        continue
    
      quota = state['population'] / D
      flr = math.floor(quota)
      cel = math.ceil(quota)

      # round according to geometric mean
      geomean = math.sqrt(flr) * math.sqrt(cel)
      apportionment = cel if quota > geomean else flr

      total += apportionment
      quotas.append({'name': state['name'], 'apportionment': apportionment})

    return (total, quotas)

  while True:
    total, quotas = iter(D)
    if total == number_of_seats:
      print D
      return quotas
    elif total < number_of_seats:
      D = D - 1
    else:
      D = D + 1

if __name__ == '__main__':
  import csv

  with open('census_data/historical_populations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first = True
    populations = []
    for row in csv_reader:
      if first:
        first = False
        continue

      name = row[0]
      population = int(row[2])
      populations.append( { 'name': name, 'population': population })

  result = hutington_hill(populations, 435)
  for r in result:
    print(r['name'], r['apportionment'])
    
