import numpy as np

def gauss(x, mu, sigma, A):
    return A * np.exp(-((x-mu)**2)/(2 *sigma**2))
   
def bimodal(x, *params_vals):
    y = np.zeros_like(x)
    num_gaussians = len(params_vals)//3
    for i in range(num_gaussians):
        mu = params_vals[3 * i]
        sigma = params_vals[3 * i + 1]
        A = params_vals[3 * i + 2]
        y += gauss(x, mu, sigma, A)
    return y