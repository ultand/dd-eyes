import numpy as np
from scipy.signal import butter, filtfilt

class Signal:
    """
    Class to generate a noiseless Signal with different modulation formats.
    """
    def __init__(self, modulation_format: str, baud_rate: float, jitter: float = 0):

        self.modulation_format = modulation_format
        self.baud_rate = baud_rate
        self.jitter = jitter

        self.bandwidth = 0
        self.sampling_rate = 0
        self.sampling_time = 0
        self.samples = 0

        self.symbols = 0

        self.time_samples = np.zeros(0)
        self.signal = np.zeros(0)

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
    
    def get_eye_diagram(self, eye_length, jitter_bool = True):
        eye_time_samples = self.eye_time_samples(eye_length)
        if jitter_bool:
            jitter_signal = self.enforce_jitter(self.jitter)
            return (eye_time_samples, jitter_signal[:len(eye_time_samples)])
        return (eye_time_samples, self.signal[:len(eye_time_samples)])

    def generate_signal(self):

        self.symbols = int(self.sampling_time * self.baud_rate)
        self._generate_nrz()
        self._get_time_samples()
        if self.bandwidth > 0:
            self.filter_signal()

    def _get_time_samples(self):
    
        self.time_samples = np.linspace(0, self.sampling_time, self.samples)

    def _generate_nrz(self) -> np.ndarray:

        opts = np.random.choice([0, 1], self.symbols)
        self.signal = np.repeat(opts, self.samples//self.symbols)

    def eye_time_samples(self, eye_length):
        
        eye_samples = int(eye_length*(self.sampling_rate/self.baud_rate))
        time_samples = np.linspace(0, eye_samples, eye_samples)
        time_samples/=self.sampling_rate
        full_time_samples = np.tile(time_samples, int(self.samples/eye_samples))
        return full_time_samples
        

    def filter_signal(self, filter_order = 4):

        if self.bandwidth < 0:
            print(f"Error, Bandwidth of {self.bandwidth} is not valid. Set bandwidth before filtering the signal...")
        if self.bandwidth < self.sampling_rate * 2: 
            b,a  = butter(filter_order, self.bandwidth, fs = self.sampling_rate)
            filtered_signal = filtfilt(b, a, self.signal)
            self.signal = filtered_signal
        else:
            print("Error: Bandwidth is larger than sampling frequency. Signal unchanged...")
    
    def enforce_jitter(self, jitter_time):
        # currently this function assumes that the provided jitter describes the STD of the jitter time. This may be updated to agree with definitions
        self.jitter_time = jitter_time * self.sampling_rate

        # partition the signal realisations
        partitioned_signal = np.split(self.signal, self.symbols)
        # need to divide it into patterns number of realisations
        # this particular thing probably needs a test
        for i, signal_partition in enumerate(partitioned_signal):
            jitter = np.random.normal(0, self.jitter_time)
            partitioned_signal[i] = np.roll(signal_partition, int(np.round(jitter)))

        return np.ravel(partitioned_signal)


        
