import scipy.stats
import math
import numpy as np
from scipy.optimize import fsolve

delta = 0
epsilon = 0

def poisson_equations(p):
    lambda_, c = p
    print("-----------------")
    print(math.ceil(lambda_),c)
    print("-----------------")
    lambda_ = math.ceil(lambda_)
    val = lambda_ + c*math.sqrt(lambda_)

    f1 =  math.log(val/lambda_) - epsilon

    # keeping operands small enough so as not to get a 
    # a math overflow or a math domain error
    op1 = -lambda_
    op2 = 1+math.log(lambda_)
    op2 = op2*val
    op3 = math.log(val)*val

    f2 = op1 + op2 - op3

    f2 = math.exp(f2) - delta


 F = @(x)[ log(1 + x(2)*sqrt(x(1))/x(1))-epsilon;
    exp(-x(1))*(exp(1)*x(1))^(x(1)+x(2)*sqrt(x(1)))/((x(1)+x(2)*sqrt(x(1)))^((x(1)+x(2)*sqrt(x(1)))))
  ]
    return (f1,f2)

def poisson_noise(eps, dlt):
    global delta
    global epsilon

    epsilon = eps
    delta = dlt
    (lambda_,c) = scipy.optimize.excitingmixing(poisson_equations, (16400,10))

    print(lambda_,c)
    print(epsilon)

    val = float(lambda_ + c*math.sqrt(lambda_))
    epsilon =  math.log(val/lambda_)

    print(epsilon)
    epsilon = 0
    delta = 0
    return np.random.poisson(math.ceil(lambda_))

poisson_noise(0.5,0.5)



#
# def poisson_noise(lambda_, c, n):
#
#     val = float(lambda_ + c*math.sqrt(lambda_))
#     epsilon =  math.log(val/lambda_)
#     delta = math.exp(-lambda_)*math.exp(val)*(lambda_**val)/(val**val)
#
#     print("epsilon:", epsilon," delta:",delta)
#
#     return np.random.poisson(lambda_, n)
