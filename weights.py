"""
Implementation of weights on subintervals of { 1, ..., N }, for some positive
integer N.
"""
from orbiterror import *


class Weights:
    """
    A map assigning weight vectors to each element of { 1, ..., N }, for some
    positive integer N.
    """
    def __init__( self, data ):
        """
        Uses the given data to initialise a map from { 1, ..., N } to weight
        vectors of dimension d, for some positive integers N and d.

        The given data should be a list of length L, where L>0, such that for
        each i in { 0, ..., L-1 }, the ith entry of this data is a pair
        ( width<i>, weight<i> ), where:
        --> width<i> is a positive integer; and
        --> weight<i> is a list containing precisely d positive integers.
        Letting sum<i> = width<0> + ... + width<i>, this routine uses the
        given data to construct a map on { 1, ..., N }, where N = sum<L-1>,
        as follows:
            For each i in { 0, ..., L-1 }, the map sends each integer in
            [ sum<i-1> + 1, sum<i> ] to the vector given by weight<i>.

        Pre-condition:
        --> The given data conforms to the format described above.
        """
        total = 0
        self._weights = []
        for i in range( len(data) ):
            width, weight = data[i]
            if i == 0:
                self._dim = len(weight)
            else:
                if self._dim != len(weight):
                    raise WeightDimensionError( self._dim, len(weight) )
            total += width
            self._weights.append( [ total, weight ] )
        self._total = total

    def __str__(self):
        return ( "A map from {{ 1, ..., {} }} ".format( self._total ) +
                "to weight vectors of dimension {}".format( self._dim ) )

    def __repr__(self):
        # Reconstruct the data needed to build this map from scratch.
        data = []
        previous = 0
        for i in range( len( self._weights ) ):
            current, weight = self._weights[i]
            width = current - previous
            previous = current
            data.append( ( width, weight ) )
        return "Weights( {} )".format( repr(data) )

    def detail(self):
        """
        Returns a detailed text representation of this weight mapping.

        This text may span many lines, and provides a human-readable
        description that completely specifies this weight mapping. This text
        always ends with a final newline.
        """
        msg = ""
        start = 1
        for i in range( len( self._weights ) ):
            end, weight = self._weights[i]
            msg += "Interval [{}, {}] --> Vector {}\n".format(
                    start, end, weight )
            start = end + 1
        return msg

    def append(self):
        """
        """
        #TODO
        pass

    def contract(self):
        """
        """
        #TODO
        pass

    def transfer( self, start, width, pairing ):
        """
        Transfers the weights in [start,end], where end = start+width-1, by
        the given pairing.
        """
        #TODO
        pass


if __name__ == "__main__":
    #TODO Test code.
    w = Weights( [ ( 2, [1,2,3] ), ( 3, [4,5,6] ) ] )
    print(w)
    print( repr(w) )
    print( w.detail() )
    w = Weights( [ ( 2, [1,2,3] ), ( 3, [4,5] ) ] )
