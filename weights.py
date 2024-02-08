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
        self._intervalLength = total

    def __str__(self):
        return ( "A map from {{ 1, ..., {} }} ".format(
            self._intervalLength ) +
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

    def dimension(self):
        """
        Returns the dimension of the vectors in the image of this weight
        mapping.
        """
        return self._dim

    def intervalLength(self):
        """
        Returns the interval length N of this weight mapping.
        """
        return self._intervalLength

    def countSubintervals(self):
        """
        Returns the number of subintervals of constant weight given by this
        weight mapping.
        """
        return len( self._weights )

    def setZero( self, start, width ):
        """
        Sets the weights on the interval [start,end] to zero, where
        end = start + width - 1.

        Let m = self.countSubintervals(). This routine runs in O(m^2)-time.

        Pre-condition:
        --> end <= self.intervalLength().

        TODO:
        --> Optimise: improve running time from O(m^2) to O(m).
        """
        #TODO This routine could be improved to O(m)-time by encoding
        # self._weights as a linked list.
        end = start + width - 1
        zero = [0] * self.dimension()
        previousEnd = 0

        # Loop is O(m)-time. With a linked list, this could be replaced with
        # a functionally-equivalent O(m)-time loop.
        for i in range( len( self._weights ) ):
            currentEnd, currentWeight = self._weights[i]
            if start <= currentEnd:
                break
            else:
                previousEnd = currentEnd

        # Insert new subinterval(s) to indicate the weight changing from
        # currentWeight to zero.
        # This is O(m)-time because each insertion requires O(m)-time. With a
        # linked list, this could be improved to O(1)-time.
        if start - 1 > previousEnd:
            self._weights.insert( i, [ start - 1, currentWeight ] )
            i += 1
        self._weights.insert( i, [ end, zero ] )
        i += 1

        # To finish, delete all subintervals consisting entirely of entries
        # that are now assigned zero weight.
        # This loop is O(m^2)-time because each pop requires O(m)-time. With
        # a linked list, this loop could be improved to O(m)-time.
        while end >= self._weights[i][0]:
            self._weights.pop(i)

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
    w = Weights( [
        ( 2, [1,2,3] ),
        ( 3, [4,5,6] ),
        ( 2, [4,5,6] ),
        ( 3, [2,3,4] ),
        ( 3, [1,2,3] ) ] )
    print( w.detail() )

    print( "Set [2,3] to zero." )
    w.setZero( 2, 2 )
    print( w.detail() )

    print( "Set [5,10] to zero." )
    w.setZero( 5, 6 )
    print( w.detail() )
