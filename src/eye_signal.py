import numpy as np
from scipy.signal import butter, filtfilt
from utils import eye_sectioning

class EyeSignal:
    """
    Class to generate a noiseless Signal with different modulation formats.
    This class handles the sampling rate and the bandwidth filtering of the data.

    Attributes
    ----------
    baud_rate : float
        The baud rate of the signal.
    samples : int
        The number of samples in the signal.
    bandwidth : float
        The bandwidth of the signal.
    sampling_rate : float
        The sampling rate of the signal.
    sampled_signal : np.ndarray
        The sampled version of the signal.
    signal : np.ndarray
        The original signal.
    time_samples : np.ndarray
        The time samples of the signal.
    filtered_signal : np.ndarray
        The filtered version of the signal.

    Methods
    -------
    update_processed_signals()
        Updates both the sampled and filtered versions of the signal.
    update_sampled_signal()
        Updates the sampled version of the signal.
    _calculate_time_samples(signal_length)
        Calculates the time samples of the signal.
    update_filtered_signal(filter_order=4)
        Updates the filtered version of the signal.
    """
    def __init__(self, config=None):
        """
        Initializes the Signal class with the provided configuration.

        Parameters
        ----------
        config : dict, optional
            Configuration dictionary with keys 'signal', 'baud_rate', 'bandwidth', and 'sampling_rate'.
        """
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
    def baud_rate(self, value:float):
        self._baud_rate = value
        self.update_processed_signals()


    @property
    def samples(self):
        return len(self._signal)
    
    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value:float):
        self._bandwidth = value
        self.update_filtered_signal()

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, value:float):

        self._sampling_rate = value
        self.update_processed_signals()
        
    @property
    def sampled_signal(self):
        return self._sampled_signal
    
    @sampled_signal.setter
    def sampled_signal(self, value:np.ndarray):
        self._sampled_signal = value

    @property
    def signal(self):
        return self._signal
        # repeat signal with given number of samples
        # filter the signal
    
    @signal.setter
    def signal(self, value: np.ndarray):
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
        """
        Updates both the sampled and filtered versions of the signal.
        """
        self.update_sampled_signal()
        self.update_filtered_signal()

    def update_sampled_signal(self):
        """
        Updates the sampled version of the signal.
        """
        if self._baud_rate and (self._signal is not None) and self._samples:
            # note that we round the number of samples per bit to an integer
            # I should create a check and assign this before this point
            samples_per_bit = int(self._sampling_rate/self._baud_rate)
            self.sampled_signal = np.repeat(self._signal, samples_per_bit)

            total_samples = self._samples * samples_per_bit
            self._calculate_time_samples(total_samples)

    def _calculate_time_samples(self, signal_length):

        """
        Calculates the time samples of the signal.

        Parameters
        ----------
        signal_length : int
            The length of the signal for which to calculate time samples.
        """

        sample_arr = np.linspace(0, signal_length, signal_length)
        self._time_samples = sample_arr/self._sampling_rate
        
    def update_filtered_signal(self, filter_order = 4):
        """
        Updates the filtered version of the signal.

        Parameters
        ----------
        filter_order : int, optional
            The order of the Butterworth filter to apply (default is 4).
        """

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

    def update_jittered_signal(self, eye_length = 5, bit_samples = -1):

        
        eye_samples = eye_length * self.sampling_rate//self.baud_rate
        eye_realisations = bit_samples // eye_length

        eye_time_samples = eye_sectioning.gen_eye_time_samples(
                                eye_samples, 
                                self.sampling_rate, 
                                eye_realisations)
        
        eye_volts = eye_sectioning.used_eye_points(self._filtered_signal, eye_realisations, eye_samples)
        
        return eye_time_samples, eye_volts
