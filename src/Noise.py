import numpy as np
class Noise:
    def __init__(self, snr, signal):
        self.signal = signal
        self.snr = snr

        self.signal_power = 0
        self._calc_signal_power()

        self.noise = np.zeros_like(signal)

    def generate_noise(self):
        snr_linear = 10**(self.snr/10)
        
        noise_power = self.signal_power/snr_linear
        self.noise = np.random.normal(0, np.sqrt(noise_power), self.signal.size)
    
    
    def _calc_signal_power(self):
        
        mean_power = np.mean(self.signal)
        self.signal_power = np.mean((self.signal-mean_power) ** 2)
