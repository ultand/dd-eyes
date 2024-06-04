from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

class SimAnalysis:
    def __init__(self, config = None):
        self.params = []
        self._bandwidth = None


    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        self._bandwidth = value

    def _remove_transition_times(self, signal, sampling_time, baud_rate, samples):
        """
        based on the signal bandwidth, this remove the transition regions from the signal such that only the signal levels are analysed
        """
        # this will require the signal
        # the bandwidth
        # the 90% - 10% rise time is assumed to be 0.35/3dB bandwidth
        # https://www.thorlabs.com/images/TabImages/Rise_Time_3dB_Bandwidth_Relationship_Lab_Fact.pdf

        transition_time = 0.35/self.bandwidth

        #determine the points at which the transition happens
        # currently this is in sample units, not real space
        bit_samples = int(1/(baud_rate * sampling_time))
        transition_points = [ x*bit_samples for x in range(samples)]

        #determine the number of points that will need to be removed from each transition point. Note that this should be centered on each point
        transition_range = transition_time/sampling_time



    def add_to_params(self, mu, sigma, A):
        self.params.extend([mu, sigma, A])
        
    def _jittered_hist(self, x, y, ax):
        """
        Generate a histogram from the jittered noisy data
        """
        initial_params = np.array(self.params)
        new_params, cov = curve_fit(self.bimodal, x, y, p0=initial_params)
        new_plot = ax.plot(x, self.bimodal(x, *new_params))
        return new_plot
        
    def gauss(self, x, mu, sigma, A):
        return A * np.exp(-((x-mu)**2)/(2 *sigma**2))
        

    def bimodal(self, x, *params_vals):
        y = np.zeros_like(x)
        num_gaussians = len(params_vals)//3
        for i in range(num_gaussians):
            mu = params_vals[3 * i]
            sigma = params_vals[3 * i + 1]
            A = params_vals[3 * i + 2]
            y += self.gauss(x, mu, sigma, A)
        return y

    def ber_analysis(self):
        pass
