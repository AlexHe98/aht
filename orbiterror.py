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


class PairingNotDisjoint(PairingError):
    """
    Raised when attempting to perform an operation on an interval that is
    supposed to be (but isn't) disjoint from a pairing (or collection of
    pairings).
    """
    def __init__( self, pairing, start, width ):
        msg = "{} is not disjoint from [{},{}].".format(
                pairing, start, start+width-1 )
        super().__init__(msg)


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
