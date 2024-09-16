from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from  eye_signal import EyeSignal
from signal_noise import Noise

class SimAnalysis:
    def __init__(self, 
                 eyeSignal: EyeSignal, 
                 noise: Noise,
                 config = None):
        self.params = []
        self.sampled_signal = eyeSignal.sampled_signal
        self.sampled_noise = noise.noise
        self._noisy_signal = self.sampled_noise + self.sampled_signal


    @property
    def sampled_signal(self):
        return self._sampled_signal
    
    @sampled_signal.setter
    def sampled_signal(self, value):
        self._sampled_signal = value

    @property
    def sampled_noise(self):
        return self._sampled_noise
    
    @sampled_noise.setter
    def sampled_noise(self, value):
        self._sampled_noise = value

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

        #determine the ranges that we want to filter out
        ranges = [[transition_point - transition_range/2, transition_point + transition_range/2] for transition_point in transition_points]

        mask = self._check_values_in_ranges(ranges, range(len(jittered_signal)))
        #confirm that this is filtering out the points appropriately
        self._no_transition_signal = [jittered_signal[i] for i in range(len(jittered_signal)) if mask[i]]

    def _check_values_in_ranges(self, ranges, values):
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
        
        
    def _ideal_hist(self):
        """
        Calculate the bimodal fit to the ideal sampled signal with noise. Ignores issues associated with jitter and finite-width transitions.
        To first approximation can be considered the SNR of an ideally timed sample
        """
        (counts, bins) = np.histogram(self._noisy_signal, bins = 100)
        
        bin_centers = (bins[:-1] + bins[1:]) / 2
        ini_params = np.array(self.params)
        params, _ = curve_fit(self.bimodal, bin_centers, counts, p0=ini_params)
        
        #should define parametesr with appropriate controls for these
        self.ideal_fit = self.bimodal(bin_centers, *params)
        self.bin_centers = bin_centers



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
        """
        This method should determine the bit-error rate of an ideal sampled signal, and a real sampled signal, both theory and measured
        """
        pass
