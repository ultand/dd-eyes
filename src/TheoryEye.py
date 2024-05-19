import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import erfc

class TheoryEye:
    def __init__(self, config):
        config = config or {}

        self._modulation_format = config.get("modulation_format", None)
        self._snr = config.get("snr", None)
        
        linear_snr = 10**(self._snr/10)
        self._noise_variance = np.sqrt(0.5/linear_snr)

        self._data = None
        self._plot_data = None

    def modulated_data(self):
        if self._modulation_format.lower() == 'ook':
            self._data = [0, 1]

    def noisy_data(self):
        min_x = np.min(self._data) - 3 * self._noise_variance
        max_x = np.max(self._data) + 3 * self._noise_variance

        self._x_axis = np.linspace(min_x, max_x, 1000)

        self._plot_data_1 = norm.pdf(self._x_axis, self._data[0], self._noise_variance)
        self._plot_data_2 = norm.pdf(self._x_axis, self._data[1], self._noise_variance)

    def calculated_ber(self):
        if self._modulation_format.lower() == 'ook':
            q = 0.5 * erfc(np.sqrt(10**(self._snr/10)/2))
            print(q)

    def plotter(self):
        plt.fill_between(self._x_axis, self._plot_data_1, alpha = 0.3)
        plt.fill_between(self._x_axis, self._plot_data_2, alpha = 0.3, color = 'orange')