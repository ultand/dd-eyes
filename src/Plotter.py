import matplotlib.pyplot as plt
import numpy as np
import Signal
from matplotlib.colors import LogNorm

class Plotter:
    def __init__(self, axs, signal: Signal.Signal, config=None):

        config = config  or {}
        self._axs = axs
        self._signal_class = signal
        self._jitter_time = config.get("jitter_time", None)
        self._eye_length = config.get("eye_length", None)
        self._eye_cmap = config.get("color_map", plt.cm.hot)
        self._noise = config.get("noise", None)
        self._bins = config.get("eye_diagram_bins", None)

        self._eye_samples = int(self._signal_class.sampling_rate/self._signal_class.baud_rate * self._eye_length)

        self._eye_realisations = self._signal_class.samples//self._eye_length

        self._eye_data = None
        self._eye_time_samples = None   
        self._jittered_signal = None

        self._generate_eye_time_samples()
        self._generate_noisy_signal()
        self._generate_jittered_signal()

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, value):
        self._noise = value
        self._generate_noisy_signal()
        self._generate_jittered_signal()

    @property
    def signal_class(self):
        return self._signal_class
    
    @signal_class.setter
    def signal_class(self, value):
        self._signal_class = value

        self._eye_samples = int(self._signal_class.sampling_rate/self._signal_class.baud_rate * self._eye_length)
        self._eye_realisations = self._signal_class.samples//self._eye_length

        self._generate_eye_time_samples()
        self._generate_noisy_signal()
        self._generate_jittered_signal()

    # specify which type of eye diagram
    def get_eye_diagram_plot(self, axs_pos):

        #make this vmax_value options
        total_eye_samples = len(self._eye_time_samples)
        expected_samples = total_eye_samples/self._bins**2
    
        hist = self._axs[axs_pos].hist2d(self._eye_time_samples,
                        self._jittered_signal + 1,
                        bins = self._bins,
                        cmap = self._eye_cmap,
                        norm = LogNorm())
        return hist

    def _generate_jittered_signal(self):

        eye_total_samples = self._eye_samples * self._eye_realisations
        eye_data = self._noisy_signal[:eye_total_samples]

        partitioned_signal = np.array_split(eye_data, self._eye_realisations)

        for i, signal_partition in enumerate(partitioned_signal):
            jitter = np.random.normal(0, self._jitter_time*self._signal_class.sampling_rate)
            partitioned_signal[i] = np.roll(signal_partition, int(np.round(jitter)))

        self._jittered_signal = np.concatenate(partitioned_signal)

    def _generate_eye_time_samples(self):
        true_time_stamps = np.linspace(0, self._eye_samples, self._eye_samples)
        true_time_stamps /= self._signal_class.sampling_rate

        self._eye_time_samples = np.tile(true_time_stamps, self._eye_realisations)
    
    def _generate_noisy_signal(self):
        self._noisy_signal = self._signal_class.filtered_signal + self._noise
