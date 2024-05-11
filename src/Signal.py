import numpy as np
from scipy.signal import butter, filtfilt

class Signal:
    """
    Class to generate a noiseless Signal with different modulation formats.
    """
    def __init__(self, modulation_format: str, baud_rate: float):

        self.modulation_format = modulation_format
        self.baud_rate = baud_rate

    def generate_signal(self, patterns: int, samples: int, eye_length: int):

        self.samples = samples

        symbols = patterns * eye_length
        org_signal = self._generate_nrz(symbols, samples)
        eye_samples = samples * eye_length

        time_samples = self._get_time_samples(eye_length, eye_samples, patterns)

        self.signal = org_signal
        self.time_samples = time_samples

        return (self.time_samples, self.signal)

    def _get_time_samples(self, eye_length, eye_samples, patterns):
        time_samples = np.linspace(0, eye_length, eye_samples) / self.baud_rate
        full_time_samples = np.tile(time_samples, patterns)

        return full_time_samples

    def _generate_nrz(self, symbols: int, samples: int) -> np.ndarray:

        opts = np.random.choice([0, 1], symbols)
        signal = np.repeat(opts, samples)
        return signal
    
    def filter_signal(self, bandwidth, filter_order = 4):

        
        sampling_frequency = self.baud_rate * self.samples

        if bandwidth < sampling_frequency * 2: 
            b,a  = butter(filter_order, bandwidth, fs = sampling_frequency)
            filtered_signal = filtfilt(b, a, self.signal)
            self.signal = filtered_signal
        else:
            print("Error: Bandwidth is larger than sampling frequency. Signal unchanged...")

        return self.signal


        
