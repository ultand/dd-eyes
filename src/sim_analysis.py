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

    def _remove_transition_times(self, jittered_signal, sampling_time, baud_rate, samples):
        """
        based on the signal bandwidth, this remove the transition regions from the signal such that only the signal levels are analysed
        """

        # TO BE CLEAR I AM CURRENTLY REMOVING THE TRANSITION TIMES, NOT THE JITTER TIMES. JITTER TIMES REQUIRES ADDITIONAL CODE

        #I pass the jittered signal
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
        plt.plot(jittered_signal)
        #determine the ranges that we want to filter out
        ranges = [[transition_point - transition_range/2, transition_point + transition_range/2] for transition_point in transition_points]

        #temporary checks
        for transition_point in transition_points:
            plt.vlines(transition_point-transition_range/2, 0, 1, color = 'red')
            plt.vlines(transition_point+transition_range/2, 0, 1, color = 'green', ls = '--')


        mask = self.check_values_in_ranges(ranges, range(len(jittered_signal)))
        #confirm that this is filtering out the points appropriately
        return [jittered_signal[i] for i in range(len(jittered_signal)) if mask[i]]

    def check_values_in_ranges(self, ranges, values):
        #two pointer method to check if values are within some range

        result = [True] * len(values)
        i, j = 0, 0
    
        while i < len(values) and j < len(ranges):
            print(ranges[j][0], ranges[j][1])
            if values[i] < ranges[j][0]:
                # value is less than the start of the range, move to next value
                i += 1
            elif values[i] > ranges[j][1]:
                # value is greater than the end of the range, move to next range
                j += 1
            else:
                # value is within the current range
                print(i)
                result[i] = False
                i += 1
    
        return result
    
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
