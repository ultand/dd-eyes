import numpy as np
class Noise:
    """
    A class to handle simulated noise. All noise is assumed to be Gaussian, and the provided SNR refers to the ratio between the mean signal power, and the standard deviation of the noise power.

    This class will generate noise when called. The noise will be updated if the signal is updated, the snr is updated, or if :meth:`Noise.generate_noise` is called.

    Attributes
    ----------
    signal : np.ndarray
        The noiseless signal generated by :class:`Signal.Signal`
    snr : float
        Signal-to-Noise ratio in dB
    noise : np.ndarray
        The simulated noise associated with the provided signal (read-only)
    signal_power : float
        The power of the signal (read-only)

    Methods
    -------
    generate_noise()
        Generate noise based on the current signal and SNR.
    _calc_signal_power()
        Calculate the rms signal power for use in determining the snr.
    """
    def __init__(self, config:dict = None):
        """
        Based on parameters passed in config, sets the signal and snr, and calculates an accompanying noise array for the signal.

        The signal should be an array generated by :class:`Signal.Signal`.

        SNR should be a float describing the Signal-to-Noise ratio in dB.

        :param config: dictionary containing the 'signal' and 'snr' initial value. Both values default to None. If no values are provided, setting the snr and signal separately will generate the noise., defaults to None
        :type config: dict, optional
        """

        config = config or {}

        self._signal = config.get("signal", None)
        self._snr = config.get("snr", None)

        self._signal_power = 0
        self._noise = np.zeros_like(self._signal)

        self.generate_noise()

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, value:np.ndarray):
        self._signal = value
        self.generate_noise()
    
    @property
    def snr(self):
        return self._snr
    
    @snr.setter
    def snr(self, value:float):
        self._snr = value
        self.generate_noise()

    @property
    def noise(self):
        return self._noise
    
    @property
    def signal_power(self):
        return self._signal_power
    
    def generate_noise(self):
        """
        Generate noise based on the current signal and SNR. Access the noise array by calling self.noise.
        """
        # efficiency could be improved if I rescaled the noise when updating parmeters instead of recalculating noise every time
        self._calc_signal_power()
        snr_linear = 10**(self.snr/10)
        noise_power = self._signal_power/snr_linear
        self._noise = np.random.normal(0, np.sqrt(noise_power), self._signal.size)
    
    def _calc_signal_power(self):
        """
        Calculate the rms signal power for use in determining the SNR.
        """
        mean_power = np.mean(self.signal)
        self._signal_power = np.mean((self.signal-mean_power) ** 2)