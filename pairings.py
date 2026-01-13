"""
Implementation of pseudogroups of interval pairings.
"""
from aht.orbiterror import *
from aht.pairing import Pairing


class Pairings:
    """
    A pseudogroup of pairings between subintervals of { 1, ..., N }, for some
    positive integer N.
    """
    def __init__( self, pairings=None ):
        """
        Initialises a pseudogroup of interval pairings consisting of the
        given collection of pairings.

        If no pairings are given, then the initialised pseudogroup will be
        empty.
        """
        #TODO We need to be able to perform insertions and deletions, and do
        #   not need random access, so it would make more sense for this to
        #   be a linked list than a Python list.
        self._pairings = list(pairings)

    def __str__(self):
        return "An order-{} pseudogroup of interval pairings".format(
                self.order() )

    def __repr__(self):
        if self.isEmpty():
            return "Pairings()"
        else:
            return "Pairings( {} )".format( repr(self._pairings) )

    def detail(self):
        """
        Returns a detailed text representation of this pseudogroup of
        interval pairings.

        This text may span many lines, and provides a human-readable
        description that completely specifies this pseudogroup. This text
        always ends with a final newline.
        """
        msg = str(self)
        msg += "\n{}\n".format( "-" * len(msg) )
        for p in self._pairings:
            msg += "{}\n".format(p)
        return msg

    def isEmpty(self):
        """
        Is this the empty pseudogroup of interval pairings?
        """
        return (not self._pairings)

    def order(self):
        """
        Returns the number of interval pairings in this pseudogroup.
        """
        return len(self._pairings)

    def deleteIdentityPairings(self):
        """
        Deletes all pairings in this pseudogroup that are restrictions of the
        identity.

        Let k = self.order(), and let N denote the largest integer in the
        range of any of the pairings in this pseudogroup. This routine runs
        in O(k*log(N))-time.

        Returns:
            None
        """
        #TODO This implementation is O(k*log(N))-time for self._pairings
        #   represented as a Python list; it does not preserve the ordering
        #   of the pairings that are not deleted. We could get the same
        #   running time for a linked list with a simpler algorithm that also
        #   preserves the ordering.
        for i in range( self.order() - 1, -1, -1 ):
            if self._pairings[i].isIdentity():
                self._pairings[i] = self._pairings[-1]
                self._pairings.pop()

    def findStaticIntervals(self):
        """
        Returns a list containing details of all static intervals defined by
        this pseudogroup of pairings.

        An interval [r,s] is static if it is disjoint from the domain and
        range of every pairing in this pseudogroup.

        Each element of the returned list will be a list of the form
        [ start, end, width ], where:
        --> I = [start,end] is a static interval that is not contained inside
            a larger static interval; and
        --> width = end - start + 1 (i.e., it is the width of I).
        These elements will be arranged in ascending order in the returned
        list.

        Let k = self.order(), and let N denote the largest integer in the
        range of any of the pairings in this pseudogroup. This routine runs
        in O(k^2*log(N))-time.

        Returns:
            A list containing data as detailed above.
        """
        largest = 0
        static = []
        for pairing in self._pairings:
            d = pairing.rangeEnd()
            if d > largest:
                # Could find new static intervals as subintervals of
                # [largest+1,d].
                static.append( [ largest + 1, d, d - largest ] )
                largest = d

            # For each point currently described by the static list, this
            # point remains static if and only if it is fixed by the current
            # pairing.
            #NOTE At worst, each pairing only increases len(static) by adding
            #   a constant, so in total len(static) is always O(k).
            temp = []
            for start, end, width in static:
                temp.extend( pairing.fixedPoints( start, width ) )
            static = temp
        return static
