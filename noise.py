import scipy.stats
import math
import numpy as np
from scipy.optimize import fsolve

def poisson_noise(lambda_, c, n):

    val = float(lambda_ + c*math.sqrt(lambda_))
    epsilon =  math.log(val/lambda_)
    delta = math.exp(-lambda_)*math.exp(val)*(lambda_**val)/(val**val)

    print("epsilon:", epsilon," delta:",delta)

    return np.random.poisson(lambda_, n)
