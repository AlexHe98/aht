"""
Implementation of pseudogroups of interval pairings.
"""
from orbiterror import *
from pairing import Pairing


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
        self._pairings = set(pairings)

    def __str__(self):
        return "Order-{} pseudogroup of interval pairings".format(
                self.order() )

    def __repr__(self):
        return "Pairings( {} )".format( repr(self._pairings) )

    def detail(self):
        """
        Returns a detailed text representation of this pseudogroup of
        interval pairings.

        This text may span many lines, and provides a human-readable
        description that completely specifies this pseudogroup. This text
        always ends with a final newline.
        """
        msg = ""
        for p in self._pairings:
            msg += "{}\n".format(p)
        return msg

    def order(self):
        """
        Returns the number of interval pairings in this pseudogroup.
        """
        return len(self._pairings)
