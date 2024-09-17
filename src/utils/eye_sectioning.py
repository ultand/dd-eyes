import numpy as np


def gen_eye_time_samples(eye_realisation_samps, sample_rate, eye_realisations):
        """
        Generates the time samples for the eye diagram.
        This allows the signal to be partioned to produce the eye diagram 
        """
        true_time_stamps = np.linspace(0, 
                                       eye_realisation_samps, eye_realisation_samps)
        true_time_stamps /= sample_rate

        eye_time_samples = np.tile(true_time_stamps, eye_realisations)
        return eye_time_samples

def used_eye_points(signal, eye_length, eye_realisation_samps):
    
    total_samples = eye_length * eye_realisation_samps
    eye_data = signal[:total_samples] 

    return eye_data

def get_eye_subsection(used_eye_data, eye_time_samples, start, end):
    
    mask = ((eye_time_samples >= start) & (eye_time_samples <= end))
    return (eye_time_samples[mask], used_eye_data[mask])