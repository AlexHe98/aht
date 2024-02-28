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
    #NOTE This class encodes each subinterval S of constant weight using a
    #   two-element list [ x, w ], where:
    #   --> x is the last element of S; and
    #   --> w is the weight vector assigned to S.
    #   This data is all stored in order in a list L, so that we can (for
    #   instance) recover the first element of the ith subinterval by simply
    #   adding one to the last element of the (i-1)st subinterval.
    #NOTE Let m = len(L). A feature of the chosen data structure is that
    #   insertion and pop operations on L often correspond to useful
    #   modifications of the weight mapping:
    #   --> Insertion:
    #       Let i be in { 0, ..., m - 1 }; let [p,q] denote the ith
    #       subinterval; and let w denote the weight assigned to [p,q]. For x
    #       in [p,q-1], inserting the list [ x, ww ] before the ith entry of
    #       L corresponds to splitting [p,q] into the following subintervals:
    #       --- [p,x], which is now assigned weight ww; and
    #       --- [x+1,q], which is still assigned weight w.
    #   --> Pop:
    #       Let i be in { 0, ..., m - 2 }; let [p,q] and [pp,qq] denote the
    #       ith and (i+1)st subintervals, respectively; and let w and ww
    #       denote the weights assigned to [p,q] and [pp,qq], respectively.
    #       Popping the ith entry of L corresponds to merging [p,q] and
    #       [pp,qq] into a single subinterval [p,qq] with weight ww.
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

    def __str__(self):
        return ( "A map from {{ 1, ..., {} }} ".format(
            self.intervalLength() ) +
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
        return self._weights[-1][0]

    def countSubintervals(self):
        """
        Returns the number of subintervals of constant weight given by this
        weight mapping.
        """
        return len( self._weights )

    def _findSubinterval( self, x, index=0 ):
        """
        Finds i >= index such that the ith constant-weight subinterval [p,q]
        contains x, and returns the tuple (i, p, q, w), where w is the weight
        assigned to each integer in [p,q].

        This routine returns None if it cannot find the required subinterval.

        Let m = self.countSubintervals(). This routine runs in O(m)-time.

        Pre-condition:
        --> The parameter x is a positive integer such that
            x <= self.intervalLength().
        --> The parameter index is a non-negative integer such that
            index < self.countSubintervals().

        Parameters:
        --> x       A point inside the constant-weight subinterval that we
                    are required to find.
        --> index   The subinterval index at which to start searching for the
                    point x.

        Returns:
            Data as detailed above.
        """
        if index == 0:
            previousEnd = 0
        else:
            previousEnd = self._weights[ index - 1 ][0]
        if x <= previousEnd:
            return None

        # Since we now have x > previousEnd, we are guaranteed to succeed
        # (assuming that x <= self.intervalLength()).
        for i in range( index, self.countSubintervals() ):
            currentEnd, currentWeight = self._weights[i]
            if x <= currentEnd:
                return ( i, previousEnd + 1, currentEnd, currentWeight )
            else:
                previousEnd = currentEnd

    def setZero( self, start, width, index=0 ):
        """
        Sets the weights on the interval [start,end] to zero, where
        end = start + width - 1.

        This routine begins by searching for i >= index such that the ith
        constant-weight subinterval contains the given start point. This
        routine returns i if the search succeeds; otherwise, it returns None.
        If the given index is 0 (the default), then the search is guaranteed
        to succeed (assuming that start <= self.intervalLength()).

        Let m = self.countSubintervals(). This routine runs in O(m^2)-time.

        Pre-condition:
        --> The parameters start and width are positive integers such that
            start + width - 1 <= self.intervalLength().

        TODO:
        --> Optimise: improve running time from O(m^2) to O(m).

        Parameters:
        --> start   The start point of the interval whose weights should be
                    set to zero.
        --> width   The width of the interval whose weights should be set to
                    zero.
        --> index   The index at which to start searching for the constant-
                    weight subinterval containing the given start point.

        Returns:
            The index of the constant-weight subinterval containing the given
            start point, or None if this routine failed to find the required
            subinterval.
        """
        #TODO This routine could be improved to O(m)-time by encoding
        #   self._weights as a linked list.

        # In O(m)-time, find the subinterval [p,q] that contains start.
        data = self._findSubinterval( start, index )
        if data is None:
            return None
        i, p, q, assignedWeight = data
        foundIndex = i

        zero = [0] * self.dimension()
        end = start + width - 1

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
        return foundIndex

    def addWeight( self, weight, start, width, index=0 ):
        """
        Adds the given weight to the image of each element of the interval
        [start,end], where end = start + width - 1.

        This routine begins by searching for i >= index such that the ith
        constant-weight subinterval contains the given start point. This
        routine returns i if the search succeeds; otherwise, it returns None.
        If the given index is 0 (the default), then the search is guaranteed
        to succeed (assuming that start <= self.intervalLength()).

        Let m = self.countSubintervals(), and let C denote the worst-case
        complexity of adding the given weight to any particular vector in the
        image of this weight mapping (roughly, C scales logarithmically with
        the size of the integers in the weight vectors). This routine runs in
        O(C*m)-time.

        Pre-condition:
        --> The given weight is a length-d list of non-negative integers,
            where d = self.dimension().
        --> The parameters start and width are positive integers such that
            start + width - 1 <= self.intervalLength().

        Parameters:
        --> weight  The weight to be added to the specified interval.
        --> start   The start point of the interval to which we should add
                    the given weight.
        --> width   The width of the interval to which we should add the
                    given weight.
        --> index   The index at which to start searching for the constant-
                    weight subinterval containing the given start point.

        Returns:
            The index of the constant-weight subinterval containing the given
            start point, or None if this routine failed to find the required
            subinterval.
        """
        # In O(m)-time, find the subinterval [p,q] that contains start.
        data = self._findSubinterval( start, index )
        if data is None:
            return None
        i, p, q, assignedWeight = data
        foundIndex = i

        if weight == [0] * self.dimension():
            return foundIndex
        end = start + width - 1

        # Handle the weights immediately preceding the interval [start,end].
        #TODO In the worst case, this step requires O(m)-time, since it might
        #   involve either a pop or an insertion operation. With a linked
        #   list, this could be improved to O(1)-time.
        if start == p:
            # If assignedWeight + weight coincides with the weight of the
            # (i-1)st subinterval, then the (i-1)ist and ith subintervals
            # will get merged after we add weight. We handle this by merging
            # the subintervals now, and treating the elements that used to
            # form the (i-1)st subinterval as if they lie inside [start,end].
            if i > 0 and self._weights[i-1][1] == _vectorSum(
                    assignedWeight, weight ):
                self._weights.pop(i-1)
                i -= 1
        else:
            # If start > p, then the weight on the subinterval [p,start-1]
            # should remain as the original assignedWeight (i.e., we do not
            # need to add the given weight to it). We keep track of this by
            # inserting a new subinterval.
            self._weights.insert( i, [ start - 1, assignedWeight ] )
            i += 1

        # For each subinterval lying entirely inside [start,end], adding the
        # given weight is straightforward.
        #NOTE This step requires O(C*m)-time.
        while i < self.countSubintervals() and end >= self._weights[i][0]:
            currentEnd, assignedWeight = self._weights[i]
            self._weights[i] = [ currentEnd,
                    _vectorSum( assignedWeight, weight ) ]
            i += 1

        # At this point, we have one of the following possibilities:
        #   --> If i == self.countSubintervals(), then we have already added
        #       weight all the way to the end of the interval covered by this
        #       weight mapping (i.e., end == self.intervalWidth()), and hence
        #       there is nothing left to do.
        #   --> If i < self.countSubintervals(), then either the interval
        #       [start,end] ends at the beginning of the ith subinterval S,
        #       or it ends somewhere in the middle of S (it cannot end at the
        #       end of S, since we would have incremented i in the previous
        #       step). In this case, one of the following tasks remains:
        #       --- If [start,end] ends in the middle of S, then we can
        #           finish the adding weight procedure by simply inserting a
        #           new subinterval.
        #       --- If [start,end] ends at the beginning of S, then there is
        #           nothing left to do unless the weight assigned to end is
        #           now equal to the weight assigned to S, in which case we
        #           need to merge S with the (i-1)st subinterval.
        #NOTE In the worst case, this last step requires O(C+m)-time, since
        #   it might involve either a pop or an insertion operation.
        if i == self.countSubintervals():
            return foundIndex
        currentWeight = self._weights[i][1]
        if i == 0:
            previousEnd = 0
        else:
            previousEnd, previousWeight = self._weights[i-1]
        if end > previousEnd + 1:
            # The case where [start,end] ends in the middle of S.
            self._weights.insert(
                    i, [ end, _vectorSum( currentWeight, weight ) ] )
        elif previousWeight == currentWeight:
            # The case where [start,end] ends at the beginning of S.
            self._weights.pop(i-1)
        return foundIndex

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

    #TODO Finish documenting this routine.
    #TODO Test this routine.
    def transferBy( self, pairing ):
        """
        Transfers the weights in the range of the given pairing to smaller
        orbit representatives.

        If the given pairing is orientation-reversing and has overlapping
        domain and range, then the very first step of the transfer is to trim
        the given pairing.

        ...

        Pre-condition:
        --> The pairing parameter is an instance of Pairing.

        Warning:
        --> As explained above, the requested transfer might involve trimming
            (and hence modifying) the given pairing.

        Parameters:
        --> pairing     The pairing by which to transfer weights.

        Returns:
            None
        """
        # Handle the orientation-reversing case first.
        if pairing.isOrientationReversing():
            pairing.trim()

            # Iteratively transfer weights out of the constant-weight
            # subintervals of the range of the given pairing.
            start = pairing.rangeStart()
            i, _, end, weight = self._findSubinterval(start)
            #TODO
            pass

        # Now handle the orientation-preserving but non-periodic case.
        #NOTE This is very similar to the orientation-reversing case, but we
        #   handle it separately to optimise the algorithm slightly.
        if not pairing.periodicInterval():
            #TODO
            pass

        # Finally, handle the periodic case.
        #TODO Reimplement.
        pairing.trim()

        # Handle the non-periodic case first, since this case is relatively
        # straightforward.
        if not pairing.periodicInterval():
            # Iteratively transfer weights out of the constant-weight
            # subintervals of the range of the given pairing.
            start = pairing.rangeStart()
            i, _, end, weight = self._findSubinterval(start)
            #TODO Can possibly accelerate adding weights by exploiting the
            #   fact that we know where the previous subinterval was.
            while start <= pairing.rangeEnd():
                # Transfer weight out of the current constant-weight
                # subinterval.
                width = end - start + 1
                inverseStart = pairing.inverseImageStart( start, width )
                self.addWeight( weight, inverseStart, width )

                # Find the next constant-weight subinterval.
                i += 1
                start = end + 1
                end, weight = self._weights[i]
                if end > pairing.rangeEnd():
                    end = pairing.rangeEnd()

            # Now that the weights have been transferred out of the range of
            # the given pairing, we finish the transfer operation by setting
            # all the weights inside the range to zero.
            self.setZero( pairing.rangeStart(), pairing.width() )
            return

        # Now handle the periodic case.
        #TODO
        return
