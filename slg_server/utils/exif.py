
import numpy as np


type point_value = int
type point_multiplier = int
type point_sub = tuple[point_value, point_multiplier]

type point = tuple[point_sub, point_sub, point_sub]
type altitude_point = point_sub

def dec_to_dms(dec: float,
               seconds_multiplier: point_multiplier = 10000,
               ) -> point:
    '''
    Convert decimal degrees to degrees-minutes-seconds

    Parameters
    ----------
    dec : float
        Input coordinate in decimal degrees.

    Returns
    -------
    list
        Coordinate in degrees-minutes-seconds.
        :param dec:
        :param minutes_multiplier:
        :param degrees_multiplier:
        :param seconds_multiplier:
    '''
    degree = int(np.floor(dec))
    minutes = dec % 1.0 * 60
    seconds = int(np.floor(minutes % 1.0 * 60 * seconds_multiplier))
    minutes = int(np.floor(minutes))

    return (degree, 1), (minutes, 1), (seconds, seconds_multiplier)

def normalize_alt(dec: float|int, altitude_multiplier = 1000) -> altitude_point:
    if dec is int:
        return dec, 1
    value = np.floor(dec * altitude_multiplier)
    return int(value), altitude_multiplier