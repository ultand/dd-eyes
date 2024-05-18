import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import Signal

class Plotter:
    def __init__(self, signal:Signal.Signal, jitter_bool = True):
        self.eye_cmap = plt.cm.jet
        self.signal = signal
        self.jitter_bool = jitter_bool

        self.eye_time_samples = None
        self.eye_signal = None

        self.time_samples = None
        self.signal_values = None



    def get_eye_diagram_plot(self, eye_length, ax, bins = 500):

        self._get_eye_diagram_data(eye_length)
        ax.hist2d(self.eye_time_samples, self.eye_signal, bins)
        return ax


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
    

