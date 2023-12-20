"""The value used in disc selection. The radius of the area where there should not be any
other disc center"""
R_M = 0.95

"""Coefficient used in the calculation of connection quality. A large coefficient means that
the impact of the distance between discs is lower"""
RHO = 8.75

"""Minimal connection quality"""
Q_MIN = 0.07

"""Maximal difference between the quality of basic and alternative connection"""
QR_MAX = 0.24

"""Maximal angle between the two following vectors in a stroke (in degrees)"""
MAX_ANGLE = 67.5  # Halfway between 45 and 90 deg

"""Maximal approximation error"""
EPSILON = 0.039

"""Minimal stroke independence"""
D_MIN = 0.2
