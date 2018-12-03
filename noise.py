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
    return np.random.laplace(scale = 1/epsilon, size = n)

def geometric_noise(epsilon, n):
    return scipy.stats.dlaplace.rvs(epsilon, size = n)

def gaussian_noise(epsilon, delta, n):
    #not sure about GS_2(f)
    global_sensitivity_2 = 1
    sigma = math.sqrt(2*math.log(1/delta))/epsilon*global_sensitivity_2
    return np.random.normal(0, sigma, n)
