"""
Custom exceptions for orbit-counting.
"""


class OrbitError(Exception):
    """
    Raised when an error is encountered while counting orbits.
    """
    pass


class PairingError(OrbitError):
    """
    Raised when there is an error with an interval pairing.
    """
    pass


class WeightError(OrbitError):
    """
    Raised when there is an error with a weight mapping.
    """
    pass


class WeightDimensionError(WeightError):
    """
    Raised when a weight vector of the wrong dimension is encountered.
    """
    def __init__( self, expectedDim, foundDim ):
        msg = ( "Expected vector of dimension {}, ".format(expectedDim) +
                "but found vector of dimension {}.".format(foundDim) )
        super().__init__(msg)
