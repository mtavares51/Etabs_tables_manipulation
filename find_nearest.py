
import numpy as np

def find_nearest(array, value):
    """Function to get nearest value from an array"""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
