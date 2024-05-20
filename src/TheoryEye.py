import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import erfc

class TheoryEye:
    """
    A class to calculate and plot histograms representing eye diagram levels for a given signal-to-noise ratio (SNR).

    Attributes
    ----------
    data_levels : int
        The number of data levels in the modulation format.
    
    Methods
    -------
    calculate_ber():
        Calculates the Bit Error Rate (BER) for a binary modulation format.
    plotter(ax):
        Plots the theoretical eye diagram on the provided axes.
    """
    def __init__(self, config):
        """
        Initializes the TheoryEye class with the provided configuration.

        :param config: Dictionary containing configuration values.
        :type config: dict, optional
        """
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
        """
        Calculates the linear SNR value from the provided SNR in dB.
        """
        if self._data_levels == 2:
            self._linear_snr = 10**(self._snr/10)
        else:
            raise ValueError

    def _update_noise_std(self):
        """
        Updates the noise standard deviation based on the linear SNR value and calculates the BER.
        """
        self._noise_std = np.sqrt(0.5/self._linear_snr)
        self.calculate_ber()

    def _get_x_axis(self):
        """
        Generates the x-axis values for the plot based on the noise standard deviation and data levels. 
        
        The plot range is designed so that it strethes between the maximum data level + plots_x_std standard deviations to the minimum data level - plots_x_std standard deviations.
        """
        min_x = 0 - self._plots_x_std * self._noise_std
        max_x = self._data_levels - 1 + self._plots_x_std * self._noise_std
        self._x_axis = np.linspace(min_x, max_x, self._plot_points)

    def _generate_plot_data(self):
        """
        Generates the data for plotting the probability density functions for each data level.
        """

        self._plots_data = []
        for i in range(self._data_levels):
            self._plots_data.append(norm.pdf(self._x_axis, i, self._noise_std))

    def calculate_ber(self):
        """
        Calculates the Bit Error Rate (BER) for a binary modulation format.
        """
        if self._data_levels == 2:
            self._ber = 0.5 * erfc(np.sqrt(self._linear_snr/2))

    def plotter(self, ax):
        """
        Plots the theoretical eye diagram on the provided axes.

        :param ax: The axes on which to plot the eye diagram.
        :type ax: matplotlib.axes.Axes
        :return: The axes with the plotted eye diagram.
        :rtype: matplotlib.axes.Axes
        """
        for plot_data in self._plots_data:
            plt.fill_between(self._x_axis, plot_data, alpha = 0.3)
        ax.set_title(f'{self._data_levels}-Level Signal - SNR: {self._snr}dB - BER: {self._ber:.2e}')
        return ax