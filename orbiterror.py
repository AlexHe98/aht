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
