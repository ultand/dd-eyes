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

        self.patterns = patterns
        self.samples = samples

        symbols = patterns * eye_length
        org_signal = self._generate_nrz(symbols, samples)
        self.eye_samples = samples * eye_length

        time_samples = self._get_time_samples(eye_length, self.eye_samples, patterns)

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


        self.sampling_frequency = self.baud_rate * self.samples

        if bandwidth < self.sampling_frequency * 2: 
            b,a  = butter(filter_order, bandwidth, fs = self.sampling_frequency)
            filtered_signal = filtfilt(b, a, self.signal)
            self.signal = filtered_signal
        else:
            print("Error: Bandwidth is larger than sampling frequency. Signal unchanged...")

        return self.signal
    
    def enforce_jitter(self, jitter_time):
        # currently this function assumes that the provided jitter describes the STD of the jitter time. This may be updated to agree with definitions
        self.jitter_time = jitter_time * self.sampling_frequency

        # partition the signal realisations
        partitioned_signal = np.split(self.signal, self.patterns)
        # need to divide it into patterns number of realisations
        # this particular thing probably needs a test
        for i, signal_partition in enumerate(partitioned_signal):
            jitter = np.random.normal(0, self.jitter_time)
            partitioned_signal[i] = np.roll(signal_partition, int(np.round(jitter)))

        return np.ravel(partitioned_signal)


        
