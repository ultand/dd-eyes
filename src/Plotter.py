import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import Signal

class Plotter:
    def __init__(self, axs, signal: Signal.Signal, config=None):

        config = config  or {}
        self._axs = axs
        self._signal_class = signal
        self._jitter_time = config.get("jitter_time", None)
        self._eye_length = config.get("eye_length", None)
        self._eye_cmap = config.get("color_map", plt.cm.jet)
        self._noise = config.get("noise", None)
        self._bins = config.get("eye_diagram_bins", None)

        self.eye_cmap = plt.cm.jet

        self._eye_samples = int(self._signal_class.sampling_rate/self._signal_class.baud_rate * self._eye_length)

        self._eye_realisations = self._signal_class.samples//self._eye_length

        self._eye_data = None
        self._eye_time_samples = None   

    # specify which type of eye diagram
    def get_eye_diagram_plot(self, axs_pos):

        self._generate_eye_diagram()
        self._generate_eye_time_samples()

        print(self._eye_time_samples)
        print(self._eye_data)
        return self._axs[axs_pos].hist2d(self._eye_time_samples,
                        self._eye_data,
                        bins = self._bins)
    
    def _generate_eye_diagram(self):
        #reformat plot
        #add jitter
        #assume just signal for now
        eye_total_samples = self._eye_samples * self._eye_realisations
        self._eye_data = (self._signal_class.filtered_signal+ self._noise)[:eye_total_samples] 


    def _generate_eye_time_samples(self):
        true_time_stamps = np.linspace(0, self._eye_samples, self._eye_samples)
        true_time_stamps /= self._signal_class.sampling_rate

        self._eye_time_samples = np.tile(true_time_stamps, self._eye_realisations)

    def get_signal_plot(self, ax, start = 0, end = -1):

        self._get_signal_data()
        partition = np.where(start, )
        partition = np.where((start <= self.time_samples) & (self.time_samples <= end), True, False)
        print(partition)
        ax.plot(self.time_samples[partition], self.signal_values[partition])
        return ax
    

    def _get_eye_diagram_data(self, eye_length):

        eye_params= self.signal.get_eye_diagram(eye_length, self.jitter_bool)
        self.eye_time_samples, self.eye_signal = eye_params


    def _get_signal_data(self):
        self.time_samples, self.signal_values = self.signal.get_signal()
    

