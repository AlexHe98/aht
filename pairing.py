"""
Implementation of pairings between subintervals of { 1, ..., N }, for some
positive integer N.
"""
from math import gcd
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
        if a > c:
            a, c = c, a
        self._a = a
        self._b = a + width - 1
        self._c = c
        self._d = c + width - 1
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

    def inDomain( self, start, width=1 ):
        """
        Does the interval [start,end], where end = start + width - 1, lie
        entirely inside the domain of this pairing?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the point start lies inside the domain of
        this pairing.

        Pre-condition:
        --> The parameters start and width are both positive integers.
        """
        end = start + width - 1
        return ( start >= self._a and end <= self._b )

    def inRange( self, start, width=1 ):
        """
        Does the interval [start,end], where end = start + width - 1, lie
        entirely inside the range of this pairing?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the point start lies inside the range of
        this pairing.

        Pre-condition:
        --> The parameters start and width are both positive integers.
        """
        end = start + width - 1
        return ( start >= self._c and end <= self._d )

    def meetsDomain( self, start, width=1 ):
        """
        Does the interval [start,end], where end = start + width - 1, have
        non-empty intersection with the domain of this pairing?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the point start lies inside the domain of
        this pairing.

        Pre-condition:
        --> The parameters start and width are both positive integers.
        """
        end = start + width - 1
        return ( start <= self._b and end >= self._a )

    def meetsRange( self, start, width=1 ):
        """
        Does the interval [start,end], where end = start + width - 1, have
        non-empty intersection with the range of this pairing?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the point start lies inside the range of
        this pairing.

        Pre-condition:
        --> The parameters start and width are both positive integers.
        """
        end = start + width - 1
        return ( start <= self._d and end >= self._c )

    def periodicInterval(self):
        """
        If this pairing is periodic, then returns details of the
        corresponding periodic interval; otherwise, returns None.

        Specifically, if this pairing is periodic, then this routine returns
        a triple ( s, e, p ), where:
        --> s is the start point;
        --> e is the end point; and
        --> p is the period.
        """
        if ( not self._preserving ) or ( self._c > self._b + 1 ):
            return None
        period = self._c - self._a
        if period == 0:
            return None
        else:
            return ( self._a, self._d, period )

    #TODO Test this routine.
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

    def truncate( self, newBound ):
        """
        """
        #TODO
        pass

    #TODO Test this routine.
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

    #TODO Test this routine.
    #TODO Separate checking and performing?
    def mergeWith( self, other ):
        """
        Attempts to perform a periodic merger of this pairing with the other
        pairing.
        
        In detail, a periodic merger is possible if and only if:
        --> this pairing and the other pairing are both periodic; and
        --> the respective periodic intervals R and RR have "sufficient"
            overlap.
        More precisely, letting t and tt denote the periods of R and RR,
        respectively, the overlap is "sufficient" if its width is at least
        (t + tt).

        When the above conditions are satisfied, the requested periodic
        merger produces a new periodic pairing P whose period is given by
        gcd(t,tt) and whose periodic interval is given by the union of R and
        RR. If a periodic merger is possible, then this routine returns the
        new pairing P; otherwise, this routine returns None.
        """
        myInterval = self.periodicInterval()
        if myInterval is None:
            return None
        yourInterval = other.periodicInterval()
        if yourInterval is None:
            return None

        # Do the two periodic intervals have sufficient overlap?
        overlapWidth = ( min( myInterval[1], yourinterval[1] ) -
                max( myInterval[0], yourInterval[0] ) )
        if overlapWidth < myInterval[2] + yourInterval[2]:
            return None

        # Construct the pairing that results from the periodic merger.
        a = min( myInterval[0], yourInterval[0] )
        c = a + gcd( myInterval[2], yourInterval[2] )
        width = max( myInterval[1], yourInterval[1] ) - c + 1
        return Pairing( a, c, width )

    def transmitBy( self, other ):
        """
        Transmits this pairing by the other pairing.
        """
        #TODO
        pass
