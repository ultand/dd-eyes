import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import erfc

class TheoryEye:
    def __init__(self, config):
        config = config or {}

        self._modulation_format = config.get("modulation_format", None)
        self._snr = config.get("snr", None)
        self._plots_x_std = config.get("plots_x_std", 3)
        self._plot_points = config.get("x_axis_samples", 1000)

        self._data = None
        self._plot_data = None
        self._linear_snr = None
        self._noise_std = None
        self._x_axis = None
        self._ber = None

        self._get_x_axis()
        self._calculate_linear_snr()
        self._update_noise_variance()
        self._calculate_ber()


    def _calculate_linear_snr(self):
        if self._modulation_format.lower() == 'ook':
            self._linear_snr = 10*np.log10(self._snr/10)

    def _update_noise_variance(self):
        self._noise_variance = np.sqrt(0.5/self._linear_snr)

    def _get_x_axis(self):
        min_x = np.min(self._data) - self._plots_x_std * self._noise_std
        max_x = np.max(self._data) + self._plots_x_std * self._noise_std
        self._x_axis = np.linspace(min_x, max_x, self._plot_points)

    def _calculate_ber(self):
        if self._modulation_format.lower() == 'ook':
            self._ber = 0.5 * erfc(np.sqrt(self._linear_snr/2))
            
    def modulated_data(self):
        if self._modulation_format.lower() == 'ook':
            self._data = [0, 1]

    def noisy_data(self):

        self._plots_data = []
        for i, pt in enumerate(self._data):
            self._plots_data[i] = norm.pdf(self._x_axis, pt, self._noise_std)

    def plotter(self):
        plt.fill_between(self._x_axis, self._plot_data_1, alpha = 0.3)
        plt.fill_between(self._x_axis, self._plot_data_2, alpha = 0.3, color = 'orange')