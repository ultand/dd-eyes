import numpy as np
from scipy.signal import butter, filtfilt

class Signal:
    """
    Class to generate a noiseless Signal with different modulation formats.
    """
    def __init__(self, config=None):

        config = config or {}

        #required properties
        self._signal = config.get("signal", None)
        self._baud_rate = config.get("baud_rate", None)
        self._bandwidth = config.get("bandwidth", None)
        self._sampling_rate = config.get("sampling_rate", None)

        # processed variables
        self._time_samples = None
        self._sampled_signal = None
        self._filtered_signal = None
        self._samples = len(self._signal) if self._signal is not None else 0

        self.update_processed_signals()

    @property
    def baud_rate(self):
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, value):
        self._baud_rate = value
        self.update_processed_signals()


    @property
    def samples(self):
        return len(self._signal) if self._signal else 0
    
    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        self._bandwidth = value
        self.update_filtered_signal()

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, value):

        self._sampling_rate = value
        self.update_processed_signals()
        
    @property
    def sampled_signal(self):
        return self._sampled_signal
    
    @sampled_signal.setter
    def sampled_signal(self, value):
        self._sampled_signal = value

    @property
    def signal(self):
        return self._signal
        # repeat signal with given number of samples
        # filter the signal
    
    @signal.setter
    def signal(self, value):
        # assign time samples based on the baud rate
        self._signal = value
        self._samples = len(value) if value is not None else 0
        self.update_processed_signals()
        #repeat the signal with sampling repeat number of samples
        # if there is a bandwidth already then filter the signal

    @property
    def time_samples(self):
        return self._time_samples
    
    @property
    def filtered_signal(self):
        return self._filtered_signal
    
    def update_processed_signals(self):
        self.update_sampled_signal()
        self.update_filtered_signal()

    def update_sampled_signal(self):
        if self._baud_rate and (self._signal is not None) and self._samples:
            # note that we round the number of samples per bit to an integer
            # I should create a check and assign this before this point
            samples_per_bit = int(self._sampling_rate/self._baud_rate)
            self.sampled_signal = np.repeat(self._signal, samples_per_bit)

            total_samples = self._samples * samples_per_bit
            self._calculate_time_samples(total_samples)

    def _calculate_time_samples(self, signal_length):
        sample_arr = np.linspace(0, signal_length, signal_length)
        self._time_samples = sample_arr/self._sampling_rate
        
    def update_filtered_signal(self, filter_order = 4):
        # needs to be neatened

        if self._bandwidth is None:
            print("No Bandwidhth provided...")

        elif self._bandwidth <= 0:
            print(f"Error, Bandwidth of {self._bandwidth} is not valid. Set bandwidth before filtering the signal...")

        elif self._bandwidth >= self._sampling_rate * 2:
            print("Error: Bandwidth is larger than sampling frequency. Signal unchanged...")

        else: 
            nyquist = self._sampling_rate/2

            b,a  = butter(filter_order, self._bandwidth/nyquist)
            self._filtered_signal = filtfilt(b, a, self._sampled_signal)
