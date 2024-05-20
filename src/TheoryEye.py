import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import erfc

class TheoryEye:
    def __init__(self, config):
        config = config or {}

        self._snr = config.get("snr", None)
        self._plots_x_std = config.get("plots_x_std", 3)
        self._plot_points = config.get("x_axis_samples", 1000)
        self._data_levels = config.get("data_levels", 2)

        self._plots_data = None
        self._linear_snr = None
        self._noise_std = None
        self._x_axis = None
        self._ber = None

        self._calculate_linear_snr()
        self._update_noise_std()
        self._get_x_axis()
        self._generate_plot_data()

    @property
    def data_levels(self):
        return self._data_levels
    
    @data_levels.setter
    def data_levels(self, value):
        self._data_levels = value

    def _calculate_linear_snr(self):
        if self._data_levels == 2:
            self._linear_snr = 10**(self._snr/10)

    def _update_noise_std(self):
        self._noise_std = np.sqrt(0.5/self._linear_snr)
        self.calculate_ber()

    def _get_x_axis(self):
        min_x = 0 - self._plots_x_std * self._noise_std
        max_x = self._data_levels - 1 + self._plots_x_std * self._noise_std
        self._x_axis = np.linspace(min_x, max_x, self._plot_points)

    def _generate_plot_data(self):

        self._plots_data = []
        for i in range(self._data_levels):
            self._plots_data.append(norm.pdf(self._x_axis, i, self._noise_std))

    def calculate_ber(self):
        if self._data_levels == 2:
            self._ber = 0.5 * erfc(np.sqrt(self._linear_snr/2))

    def plotter(self, ax):
        for plot_data in self._plots_data:
            plt.fill_between(self._x_axis, plot_data, alpha = 0.3)
        ax.set_title(f'{self._data_levels}-Level Signal - SNR: {self._snr}dB - BER: {self._ber:.2e}')
        return ax