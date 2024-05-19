import numpy as np
class Noise:
    def __init__(self, config=None):

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
    def signal(self, value):
        self._signal = value
        self.generate_noise()
    
    @property
    def snr(self):
        return self._snr
    
    @snr.setter
    def snr(self, value):
        self._snr = value
        self.generate_noise()

    @property
    def noise(self):
        return self._noise
    
    @property
    def signal_power(self):
        return self._signal_power
    
    def generate_noise(self):
        # efficiency could be improved if I rescaled the noise when updating parmeters instead of recalculating noise every time
        self._calc_signal_power()
        snr_linear = 10**(self.snr/10)
        noise_power = self._signal_power/snr_linear
        self._noise = np.random.normal(0, np.sqrt(noise_power), self._signal.size)
    
    def _calc_signal_power(self):
        
        mean_power = np.mean(self.signal)
        self._signal_power = np.mean((self.signal-mean_power) ** 2)
