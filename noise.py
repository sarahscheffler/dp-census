import scipy.stats
import math

import numpy as np
from scipy.optimize import fsolve

# based on work in: https://eprint.iacr.org/2016/943.pdf
def poisson_noise(lambda_, c, n):
    val = float(lambda_ + c*math.sqrt(lambda_))
    epsilon =  math.log(val/lambda_)

    # keeping operands small enough so as not to get a 
    # a math overflow or a math domain error
    try:
        op1 = -lambda_
        op2 = 1+math.log(lambda_)
        op2 = op2*val
        op3 = math.log(val)*val

        f2 = op1 + op2 - op3
        delta = math.exp(f2)

    except:
        print("delta too small, setting it to 0")
        delta = 0

    print("epsilon:", epsilon," delta:",delta)

    return np.random.poisson(lambda_, n)


def laplace_noise(epsilon, n):
    return np.random.laplace(scale = 1.0/epsilon, size = n)

def geometric_noise(epsilon, n):
    return scipy.stats.dlaplace.rvs(epsilon, size = n)

def gaussian_noise(epsilon, delta, n):
    #not sure about GS_2(f)
    global_sensitivity_2 = 1.0
    sigma = math.sqrt( 2.0 * math.log(1.0/delta) ) / epsilon * global_sensitivity_2
    return np.random.normal(0, sigma, n)


'''
Probability of certain events
'''

def laplace_difference_greater_than_k(epsilon, r, k):
  if r != 1.0:
    d = (2 - 2 * r * r) * epsilon
    d = r / d
    integrals = 0
    if k <= 0:  
      integrals = epsilon*math.exp(k*r/epsilon)/r - r*epsilon*math.exp(k/epsilon)
    else:
      integrals = epsilon/r + (epsilon-epsilon*math.exp(-1*k*r/epsilon))/r - r*epsilon - r*(epsilon-epsilon*math.exp(-1*k/epsilon))
    return 1 - d * integrals
  else:
    d = 1.0 / (4 * epsilon)
    integrals = 0
    if k <= 0:
      integrals = epsilon * math.exp(k / epsilon) - (k - epsilon) * math.exp(k/epsilon)
    else:
      integrals = 4 * epsilon
      integrals -= epsilon * math.exp(-1*k / epsilon)
      integrals -= (k + epsilon) * math.exp(-1 * k / epsilon)
    return 1 - d * integrals

