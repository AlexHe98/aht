"""
Implementation of pairings between subintervals of { 1, ..., N }, for some
positive integer N.
"""
from math import gcd
from orbiterror import *


def periodicPairing( start, end, period ):
    """
    Attempts to construct a periodic pairing of the given period such that
    the periodic interval is given by [start,end].

    Such a periodic pairing exists if and only if the given parameters
    satisfy the following inequality:
        period <= (end - start + 1) // 2.
    When such a periodic pairing exists, it is unique, and this routine
    returns this uniquely determined pairing; otherwise, this routine returns
    None.

    Pre-condition:
    --> The parameters start and end are positive integers such that
        start < end.
    --> The period parameter is a positive integer.

    Parameters:
    --> start   The start point of the periodic interval of the constructed
                periodic pairing.
    --> end     The end point of the periodic interval of the constructed
                periodic pairing.
    --> period  The period of the constructed periodic pairing.

    Returns
        The requested periodic pairing, or None if no such pairing exists.
    """
    if period > (end - start + 1) // 2:
        return None
    pairing = Pairing()
    pairing._setPeriodic( start, end, period )
    return pairing


class Pairing:
    """
    A pairing between two subintervals of { 1, ..., N }, for some positive
    integer N.
    """
    def __init__( self, a=1, c=1, width=1, preserving=True ):
        """
        Initialises a pairing between [a,b] and [c,d], where
        b = a + width - 1 and d = c + width - 1.

        The pairing is taken to be orientation-preserving if preserving is
        set to True, and orientation-reversing if preserving is set to False.

        Pre-condition:
        --> The parameters a, c and width are all positive integers.

        Parameters:
        --> a           The start point of the domain (if a <= c) or range
                        (if a > c) of the constructed pairing.
        --> c           The start point of the range (if a <= c) or domain
                        (if a > c) of the constructed pairing.
        --> width       The width of the constructed pairing.
        --> preserving  Is the constructed pairing orientation-preserving?
        """
        # If necessary, swap a and c to ensure that a <= c.
        if a > c:
            a, c = c, a
        self._setPairing( a, c, width, preserving )

    def _setPairing( self, a, c, width, preserving ):
        """
        Sets this pairing to map between [a,b] and [c,d], where a <= c,
        b = a + width - 1 and d = c + width - 1.

        The pairing is taken to be orientation-preserving if preserving is
        set to True, and orientation-reversing if preserving is set to False.

        Pre-condition:
        --> The parameters a, c and width are all positive integers.

        Parameters:
        --> a           The start point of the domain of the constructed
                        pairing.
        --> c           The start point of the range of the constructed
                        pairing.
        --> width       The width of the constructed pairing.
        --> preserving  Is the constructed pairing orientation-preserving?

        Returns:
            None
        """
        self._a = a
        self._b = a + width - 1
        self._c = c
        self._d = c + width - 1
        self._preserving = preserving

        # We already know the width, so we can at least fill in this value.
        self._resetCache()
        self._width = width

    def _resetCache(self):
        """
        Resets cached properties to None.
        """
        self._width = None
        self._translationDistance = None
        self._isIdentity = None
        self._periodicInterval = None

    def __str__(self):
        if self._preserving:
            orient = "preserving"
        else:
            orient = "reversing"
        return "Orientation-{} pairing [{},{}] <-> [{},{}]".format(
                orient, self._a, self._b, self._c, self._d )

    def __repr__(self):
        return "Pairing({},{},{},{})".format(
                self._a, self._c, self.width(), self._preserving )

    def __eq__( self, other ):
        return ( ( self._a == other._a ) and
                ( self._c == other._c ) and
                ( self.width() == other.width() ) and
                ( self._preserving == other._preserving ) )

    def clone(self):
        """
        Returns a clone of this pairing.

        The clone does not inherit cached properties of this pairing.

        Returns:
            A new pairing that is equal to this one.
        """
        return Pairing( self._a, self._c, self.width(), self._preserving )

    def width(self):
        """
        Returns the width of this pairing.

        If the width is not already known, then this routine will calculate
        it and cache the result.
        """
        if self._width is None:
            self._width = self._b - self._a + 1
        return self._width

    def translationDistance(self):
        """
        Returns the translation distance if this pairing is
        orientation-preserving, or -1 if this pairing is
        orientation-reversing.

        If the translation distance is not already known, then this routine
        will calculate it and cache the result.
        """
        if self._translationDistance is None:
            if self._preserving:
                self._translationDistance = self._c - self._a
            else:
                self._translationDistance = -1
        return self._translationDistance

    def domainStart(self):
        """
        Returns the start point of the domain of this pairing.
        """
        return self._a

    def rangeStart(self):
        """
        Returns the start point of the range of this pairing.
        """
        return self._c

    def isOrientationPreserving(self):
        """
        Is this pairing orientation-preserving?

        Returns:
            True if and only if this Pairing is orientation-preserving.
        """
        return self._preserving

    def isOrientationReversing(self):
        """
        Is this pairing orientation-reversing?

        Returns:
            True if and only if this Pairing is orientation-reversing.
        """
        return ( not self._preserving )

    def isIdentity(self):
        """
        Is this pairing a restriction of the identity map?

        If the answer is not already known, then this routine will calculate
        it and cache the result.

        Returns:
            True if and only if this Pairing is an identity map.
        """
        if self._isIdentity is None:
            self._isIdentity = ( self._preserving and self._a == self._c )
        return self._isIdentity

    def domainContains( self, start, width=1 ):
        """
        Does the domain of this pairing contain the interval [start,end],
        where end = start + width - 1?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the domain contains the point start.

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval to test for containment
                    in the domain of this pairing.
        --> width   The width of the interval to test for containment in the
                    domain of this pairing.

        Returns:
            True if and only if the interval [start,end] is a subset of the
            domain of this pairing.
        """
        end = start + width - 1
        return ( start >= self._a and end <= self._b )

    def rangeContains( self, start, width=1 ):
        """
        Does the range of this pairing contain the interval [start,end],
        where, end = start + width - 1?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the range contains the point start.

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval to test for containment
                    in the range of this pairing.
        --> width   The width of the interval to test for containment in the
                    range of this pairing.

        Returns:
            True if and only if the interval [start,end] is a subset of the
            range of this pairing.
        """
        end = start + width - 1
        return ( start >= self._c and end <= self._d )

    def domainMeets( self, start, width=1 ):
        """
        Does the domain of this pairing have non-empty intersection with the
        interval [start,end], where end = start + width - 1?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the domain contains the point start.

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval to test for non-empty
                    intersection with the domain of this pairing.
        --> width   The width of the interval to test for non-empty
                    intersection with the domain of this pairing.

        Returns:
            True if and only if the interval [start,end] intersects the
            domain of this pairing.
        """
        end = start + width - 1
        return ( start <= self._b and end >= self._a )

    def rangeMeets( self, start, width=1 ):
        """
        Does the range of this pairing have non-empty intersection with the
        interval [start,end], where end = start + width - 1?

        If no width is supplied, then the default behaviour of this routine
        is to simply check whether the range contains the point start.

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval to test for non-empty
                    intersection with the range of this pairing.
        --> width   The width of the interval to test for non-empty
                    intersection with the range of this pairing.

        Returns:
            True if and only if the interval [start,end] intersects the range
            of this pairing.
        """
        end = start + width - 1
        return ( start <= self._d and end >= self._c )

    def periodicInterval(self):
        """
        If this pairing is periodic, then returns details of the
        corresponding periodic interval; otherwise, returns the empty tuple.

        Specifically, if this pairing is periodic, then this routine returns
        a triple ( s, e, p ), where:
        --> s is the start point;
        --> e is the end point; and
        --> p is the period.

        If the answer is not already known, then this routine will calculate
        it and cache the result.

        Returns:
            Data as detailed above.
        """
        if self._periodicInterval is None:
            if ( not self._preserving ) or ( self._c > self._b + 1 ):
                self._periodicInterval = ()
            else:
                period = self.translationDistance()
                if period == 0:
                    self._periodicInterval = ()
                else:
                    self._periodicInterval = ( self._a, self._d, period )
        return self._periodicInterval

    def _contractImpl( self, start, width ):
        """
        Provides instructions on how to contract the interval [start,end],
        where end = start + width - 1.

        This is a helper routine for Pairing.contract( start, width ). See
        the documentation of the main routine for a description of the
        contraction operation.

        If the requested contraction is legal, then this routine returns a
        pair (d,r), where:
        --> d is True if and only if the domain of this pairing needs to be
            shifted as part of the contraction; and
        --> r is True if and only if the range of this pairing needs to be
            shifted as part of the contraction.
        Otherwise, this routine returns None.

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval to contract.
        --> width   The width of the interval to contract.

        Returns:
            Data as detailed above.
        """
        end = start + width - 1
        if end < self._a:
            return ( True, True )
        elif start > self._b and end < self._c :
            return ( False, True )
        elif start > self._d:
            return ( False, False )
        else:
            return None

    def isDisjointFrom( self, start, width ):
        """
        Are the domain and range of this pairing both disjoint from the
        interval [start,end], where end = start + width - 1?

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval on which to test
                    disjointness.
        --> width   The width of the interval on which to test disjointness.

        Returns:
            True if and only if [start,end] is disjoint from both the domain
            and range of this pairing.
        """
        return ( self._contractImpl( start, width ) is not None )

    def contract( self, start, width ):
        """
        Attempts to contract the interval [start,end], where
        end = start + width - 1.

        Such a contraction is legal if and only if [start,end] is disjoint
        from both the domain and the range of this pairing. Performing the
        contraction leaves points to the left of [start,end] untouched, and
        modifies this pairing by subtracting width from points to the right of
        [start,end].

        Pre-condition:
        --> The parameters start and width are both positive integers.

        Parameters:
        --> start   The start point of the interval to contract.
        --> width   The width of the interval to contract.

        Returns:
            True if and only if the contraction is legal.
        """
        instructions = self._contractImpl( start, width )
        if instructions is None:
            return False

        # The contraction is legal, so perform it.
        shiftDom, shiftRan = instructions
        if shiftDom:
            self._a -= width
            self._b -= width
        if shiftRan:
            self._c -= width
            self._d -= width
        return True

    def truncate( self, newBound ):
        """
        Attempts to truncate the range of this pairing.

        The specific effect of truncation depends on whether this pairing is
        orientation-preserving or orientation-reversing:
        --> Orientation-preserving:
            In this case, truncation is possible if and only if the given
            newBound satisfies c <= newBound < d, where [c,d] is the range of
            this pairing. When truncation is possible, this routine performs
            the truncation by:
            --- shortening the domain of this pairing from [a,b] to [a,b'],
                where b' = b - (d - newBound); and
            --- shortening the range of this pairing from [c,d] to
                [c,newBound].
        --> Orientation-reversing:
            In this case, truncation is possible if and only if:
            --- the domain and range of this pairing are disjoint; and
            --- the given newBound satisfies c <= newBound < d, where [c,d]
                is the range of this pairing.
            When truncation is possible, this routine performs the truncation
            by:
            --- shortening the domain of this pairing from [a,b] to [a',b],
                where a' = a + d - newBound; and
            --- shortening the range of this pairing from [c,d] to
                [c,newBound].

        Pre-condition:
        --> The parameter newBound is a positive integer.

        Parameters:
        --> newBound    The new upper bound for the range of this pairing
                        after performing the truncation.

        Returns:
            True if and only if the truncation is legal.
        """
        if newBound < self._c or newBound >= self._d:
            return False
        if self.isOrientationPreserving():
            self._b = self._b - ( self._d - newBound )
            self._d = newBound
            self._resetCache()
            return True
        else:
            if self._c <= self._b:
                return False
            self._a = self._a + self._d - newBound
            self._d = newBound
            self._resetCache()
            return True

    def trim(self):
        """
        If this pairing is orientation-reversing, then trims this pairing to
        ensure that the domain and range are disjoint.

        This routine returns True if and only if it modifies this pairing.
        Thus, if this pairing is orientation-preserving, or if its domain and
        range are already disjoint, then this routine does nothing other than
        return False.

        Returns
            True if and only if this pairing was modified by the requested
            trimming operation.
        """
        if self._preserving or self._b < self._c:
            return False
        # Ensure that b is strictly less than the average of a and d, and
        # that c is strictly greater than the average.
        self._b = ( self._a + self._d - 1 ) // 2
        self._c = ( self._a + self._d + 2 ) // 2
        self._resetCache()
        return True

    def _setPeriodic( self, start, end, period ):
        """
        Sets this pairing to a periodic pairing of the given period such that
        the periodic interval is given by [start,end].

        This routine does not check that the requested periodic pairing
        exists. Use the periodicPairing() function to construct the requested
        periodic pairing if it is not known in advance that this is possible.

        Pre-condition:
        --> The parameters start and end are positive integers such that
            start < end.
        --> The period parameter is a positive integer such that
            period <= (end - start + 1) // 2.

        Parameters:
        --> start   The start point of the periodic interval of the
                    constructed periodic pairing.
        --> end     The end point of the periodic interval of the constructed
                    periodic pairing.
        --> period  The period of the constructed periodic pairing.

        Returns:
            None
        """
        c = start + period
        self._setPairing( start, c, end - c + 1, True )

    def mergeWith( self, other ):
        """
        Attempts to modify this pairing by performing a periodic merger with
        the other pairing.

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
        RR. This routine returns True if and only if it was able to perform
        this periodic merger.

        Parameters:
        --> other   The other pairing to be merged with this one.

        Returns:
            True if and only if the requested periodic merger is legal.
        """
        myInterval = self.periodicInterval()
        if myInterval == ():
            return False
        yourInterval = other.periodicInterval()
        if yourInterval == ():
            return False

        # Do the two periodic intervals have sufficient overlap?
        overlapWidth = ( min( myInterval[1], yourInterval[1] )
                - max( myInterval[0], yourInterval[0] )
                + 1 )
        if overlapWidth < myInterval[2] + yourInterval[2]:
            return False

        # Construct the pairing that results from the periodic merger.
        start = min( myInterval[0], yourInterval[0] )
        end = max( myInterval[1], yourInterval[1] )
        period = gcd( myInterval[2], yourInterval[2] )
        self._setPeriodic( start, end, period )
        return True

    #TODO Finish documenting this routine.
    #TODO Test this routine.
    def transmitBy( self, other ):
        """
        Transmits this pairing by the other pairing.

        If the other pairing is orientation-reversing and has overlapping
        domain and range, then the very first step of transmission is to trim
        the other pairing.

        For a transmission to be possible, the range of this pairing must be
        contained in the range of the other pairing (after possibly trimming
        the other pairing, as explained above). Assuming this requirement is
        satisfied, transmission proceeds in one of the following ways:
        -->

        Warning:
        --> As explained above, the requested transmission might involve
            trimming (and hence modifying) the given other pairing.

        Parameters:
        --> other   The other pairing by which to transmit this one.

        Returns:
            True if and only if the requested transmission is possible.
        """
        # After trimming other if necessary, is the range of this contained
        # in the range of other?
        other.trim()
        if not other.rangeContains( self.rangeStart(), self.width() ):
            return False

        # The effect of transmission depends on whether the *domain* of this
        # is contained in the range of other.
        if other.rangeContains( self.domainStart(), self.width() ):
            #TODO
            pass
        else:
            #TODO
            pass
        #TODO
        pass
