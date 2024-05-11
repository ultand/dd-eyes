import numpy as np
class Noise:
    def __init__(self, snr, signal):
        self.signal = signal
        self.snr = snr

    def generate_noise(self):
        signal_power = self._calc_signal_power()
        snr_linear = 10**(self.snr/10)
        noise_power = signal_power/snr_linear
        noise = np.random.normal(0, np.sqrt(noise_power), self.signal.size)
    
        return noise
    
    def _calc_signal_power(self):
        
        mean_power = np.mean(self.signal)
        signal_power = np.mean((self.signal-mean_power) ** 2)

        return signal_power
