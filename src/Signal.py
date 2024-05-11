import numpy as np
from scipy.signal import butter, filtfilt

class Signal:
    """
    Class to generate a noiseless Signal with different modulation formats.
    """
    def __init__(self, modulation_format: str, baud_rate: float):

        self.modulation_format = modulation_format
        self.baud_rate = baud_rate

    def set_parameters(self, 
                       bandwidth:float, 
                       sample_rate: float, 
                       sampling_time: float):
        
        self.bandwidth = bandwidth
        self.sampling_rate = sample_rate
        self.sampling_time = sampling_time
        self.samples = int(sampling_time * sample_rate)

    def get_signal(self):
        return (self.time_samples, self.signal)
    
    def generate_signal(self):

        symbols = int(self.sampling_time * self.baud_rate)

        self._generate_nrz(symbols, self.samples)
        self._get_time_samples()

    def _get_time_samples(self):

        self.time_samples = np.linspace(0, self.sampling_time, self.samples)

    def _generate_nrz(self, symbols: int, samples: int) -> np.ndarray:

        opts = np.random.choice([0, 1], symbols)
        self.signal = np.repeat(opts, samples//symbols)
    
    def filter_signal(self, bandwidth, filter_order = 4):
        self.bandwidth = bandwidth
        if bandwidth < self.sampling_rate * 2: 
            b,a  = butter(filter_order, bandwidth, fs = self.sampling_rate)
            filtered_signal = filtfilt(b, a, self.signal)
            self.signal = filtered_signal
        else:
            print("Error: Bandwidth is larger than sampling frequency. Signal unchanged...")
    
    def enforce_jitter(self, jitter_time):
        """THIS MAY NOT WORK IN NEWEST ITERATION FIX"""
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


        
