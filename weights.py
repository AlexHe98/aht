"""
Implementation of weights on subintervals of { 1, ..., N }, for some positive
integer N.
"""
from orbiterror import *


def _vectorSum( v, w ):
    """
    Pre-condition:
    --> len(v) == len(w).
    """
    return [ v[i] + w[i] for i in range( len(v) ) ]


class Weights:
    """
    A map assigning weight vectors to each element of { 1, ..., N }, for some
    positive integer N.

    Such a weight mapping is specified by partitioning { 1, ..., N } into
    subintervals of constant weight. More precisely, we specify the map using
    a sequence whose elements are of the form:
        ( [p<i>, p<i+1>-1], w<i> ),
    where:  --> i runs from 0 to (m - 1);
            --> p<0> == 1;
            --> p<m> == N + 1;
            --> each w<i> is a non-negative integer vector of dimension d,
                for some constant d, which represents the weight assigned to
                each element of the subinterval [p<i>, p<i+1>-1].
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
        previousWeight = []
        for i in range( len(data) ):
            width, weight = data[i]
            if i == 0:
                self._dim = len(weight)
            else:
                if self._dim != len(weight):
                    raise WeightDimensionError( self._dim, len(weight) )

            # Append a new subinterval. If this new subinterval is assigned
            # the same weight as the previous subinterval, then merge these
            # two subintervals.
            total += width
            if weight == previousWeight:
                self._weights[-1] = [ total, weight ]
            else:
                self._weights.append( [ total, weight ] )
            previousWeight = weight
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

    def __eq__( self, other ):
        return self._weights == other._weights

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

    def _findSubinterval( self, x, start=0 ):
        """
        Finds i >= start such that the ith subinterval [p,q] contains x, and
        returns the tuple (i, p, q, w), where w is the weight assigned to
        each integer in [p,q].

        This routine returns None if it cannot find the required subinterval.

        Let m = self.countSubintervals(). This routine runs in O(m)-time.

        Pre-condition:
        --> The parameter x is a positive integer such that
            x <= self.intervalLength().
        --> The parameter start is a non-negative integer such that
            start < self.countSubintervals().
        """
        previousEnd = 0
        for i in range( start, self.countSubintervals() ):
            currentEnd, currentWeight = self._weights[i]
            if x <= currentEnd:
                return ( i, previousEnd + 1, currentEnd, currentWeight )
            else:
                previousEnd = currentEnd

        # If we reach this point, then we failed.
        return None

    def setZero( self, start, width ):
        """
        Sets the weights on the interval [start,end] to zero, where
        end = start + width - 1.

        Let m = self.countSubintervals(). This routine runs in O(m^2)-time.

        Pre-condition:
        --> The parameters start and width are positive integers such that
            start + width - 1 <= self.intervalLength().

        TODO:
        --> Optimise: improve running time from O(m^2) to O(m).
        """
        #TODO This routine could be improved to O(m)-time by encoding
        #   self._weights as a linked list.
        end = start + width - 1
        zero = [0] * self.dimension()

        # In O(m)-time, find the subinterval [p,q] that contains start.
        i, p, q, assignedWeight = self._findSubinterval(start)

        # If start > p, then the weight on the subinterval [p,start-1] should
        # remain as the original assignedWeight (i.e., it does not need to be
        # set to zero). We keep track of this by inserting a new subinterval.
        #TODO This insertion requires O(m)-time. With a linked list, this
        #   could be improved to O(1)-time.
        zeroBefore = False
        if start == p:
            if i > 0 and self._weights[i-1][1] == zero:
                zeroBefore = True
        else:
            if assignedWeight == zero:
                zeroBefore  = True
            self._weights.insert( i, [ start - 1, assignedWeight ] )
            i += 1

        # Delete all subintervals consisting entirely of entries that should
        # now be assigned zero weight.
        # This loop is O(m^2)-time because each pop requires O(m)-time. With
        # a linked list, this loop could be improved to O(m)-time.
        while i < self.countSubintervals() and end >= self._weights[i][0]:
            self._weights.pop(i)

        # Finish by setting the weight on [start,end] to zero. How this is
        # achieved depends on whether (start-1) and/or (end+1) are already
        # assigned zero weight.
        #TODO In the worst case, this last step requires O(m)-time, since it
        #   might involve either a pop or an insertion operation. With a
        #   linked list, this could be improved to O(1)-time.
        if i < self.countSubintervals() and self._weights[i][1] == zero:
            # In this case, we already have a subinterval S with zero weight,
            # so there is no need to create a new such subinterval. If S is
            # already preceded by a subinterval R with zero weight, then we
            # need to merge R and S.
            if zeroBefore:
                self._weights.pop(i-1)
        else:
            # In this case, we need to create a new subinterval S with zero
            # weight. If S is already preceded by a subinterval R with zero
            # weight, then we need to merge R and S.
            if zeroBefore:
                self._weights[i-1] = [ end, zero ]
            else:
                self._weights.insert( i, [ end, zero ] )

    def addWeight( self, weight, start, width ):
        """
        Adds the given weight to the image of each element of the interval
        [start,end], where end = start + width - 1.

        Let m = self.countSubintervals(), and let C denote the worst-case
        complexity of adding the given weight to any particular vector in the
        image of this weight mapping (roughly, C scales logarithmically with
        the size of the integers in the weight vectors). ...

        Pre-condition:
        --> The parameters start and width are positive integers such that
            start + width - 1 <= self.intervalLength().

        TODO:
        """
        #TODO
        end = start + width - 1

        # In O(m)-time, find the subintervals [p,q] and [pp,qq] that contain
        # start and end, respectively.
        i, p, q, w = self._findSubinterval(start)
        ii, pp, qq, ww = self._findSubinterval( end, i )

        #TODO
        # ...
        if start > p:
            self._weights.insert( i, [ start - 1, w ] )
            i += 1

        # ...
        while i < self.countSubintervals() and end >= self._weights[i][0]:
            currentEnd, assignedWeight = self._weights[i]
            self._weights[i] = [ currentEnd,
                    _vectorSum( assignedWeight, weight ) ]
            i += 1
        #TODO Huh?
        if i < self.countSubintervals():
            assignedWeight = self._weights[i][1]
            self._weights.insert(
                    i, [ end, _vectorSum( assignedWeight, weight ) ] )
        #TODO
        pass

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
