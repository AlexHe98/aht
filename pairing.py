"""
Implementation of pairings between subintervals of { 1, ..., N }, for some
positive integer N.
"""
from orbiterror import *


class Pairing:
    """
    A pairing between two subintervals of { 1, ..., N }, for some positive
    integer N.
    """
    def __init__( self, a, c, width, preserving ):
        """
        Initialises a pairing between [a,b] and [c,d], where b = a+width-1
        and d = c+width-1.

        The pairing is taken to be orientation-preserving if preserving is
        set to True, and orientation-reversing if preserving is set to False.

        Pre-condition:
        --> The parameters a, c and width are all positive integers.
        """
        # If necessary, swap a and c to ensure that a <= c.
        self._a = min(a,c)
        self._b = self._a + width - 1
        self._c = max(a,c)
        self._d = self._c + width - 1
        self._width = width
        self._preserving = preserving

    def __str__(self):
        if self._preserving:
            orient = "preserving"
        else:
            orient = "reversing"
        return "Orientation-{} pairing [{},{}] <-> [{},{}]".format(
                orient, self._a, self._b, self._c, self._d )

    def __repr__(self):
        return "Pairing({},{},{},{})".format(
                self._a, self._c, self._width, self._preserving )

    def width(self):
        """
        Returns the width of this pairing.
        """
        return self._width

    def isOrientationPreserving(self):
        """
        Is this pairing orientation-preserving?
        """
        return self._preserving

    def isOrientationReversing(self):
        """
        Is this pairing orientation-reversing?
        """
        return ( not self._preserving )

    def isIdentity(self):
        """
        Is this pairing a restriction of the identity map?
        """
        return ( self._preserving and self._a == self._c )

    def period(self):
        """
        Returns the period of this pairing, or 0 if this pairing is not
        periodic.
        """
        if ( not self._preserving ) or ( self._c > self._b + 1 ):
            return 0

        # When there is no gap between the domain and range, the period is
        # given precisely by the translation distance.
        # (But when the translation distance is 0, the pairing is *not*
        # considered to be periodic.)
        return self._c - self._a

    #TODO Separate checking and performing?
    def contract( self, start, width ):
        """
        Attempts to contract the interval [start,end], where
        end = start+width-1.

        Raises PairingNotDisjoint if the interval [start,end] is not disjoint
        from the domain and range of this pairing.

        Pre-condition:
        --> The parameters start and width are both positive integers.
        """
        end = start + width - 1

        # For domain: test disjointness, and shift if necessary.
        shiftDom = False
        if end < self._a:
            # Need to shift domain.
            shiftDom = True
        elif start <= self._b:
            # Not disjoint from domain!
            raise PairingNotDisjoint( self, start, width )

        # For range: test disjointness, and shift if necessary.
        shiftRan = False
        if end < self._c:
            # Need to shift range.
            shiftRan = True
        elif start <= self._d:
            # Not disjoint from range!
            raise PairingNotDisjoint( self, start, width )

        # Perform shifts.
        if shiftDom:
            self._a -= width
            self._b -= width
        if shiftRan:
            self._c -= width
            self._d -= width

    def trim(self):
        """
        If this is an orientation-reversing pairing, then trims this pairing
        to ensure that the domain and range are disjoint.

        This routine does nothing if this pairing is orientation-preserving.
        """
        if self._preserving or self._b < self._c:
            return
        # This ensures that b is strictly less than the average of a and d,
        # and c is strictly greater than the average.
        self._b = ( self._a + self._d - 1 ) // 2
        self._c = ( self._a + self._d + 2 ) // 2

    def mergeWith( self, other ):
        """
        Attempts to perform a periodic merger or this pairing with the other
        pairing.

        In detail, if this pairing and the other pairing are both periodic,
        then this routins merges these two pairings, and returns the new
        periodic pairing that results from this merger; otherwise, this
        routine does nothing, and returns None.
        """
        #TODO
        pass


if __name__ == "__main__":
    #TODO Test code.
    Pairing(1,2,3,True).contract(2,2)
