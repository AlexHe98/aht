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
    #NOTE Let m = len(L). A feature of the chosen data structure is that many
    #   operations on L correspond to useful modifications of the weight
    #   mapping:
    #   --> Append:
    #       Let [p,q] denote the last subinterval, and let w denote the
    #       weight assigned to [p,q]. For x > 0 and ww != w, appending the
    #       list [ x, ww ] corresponds to adding a new subinterval [q+1,q+x]
    #       to the end of this weight mapping, and assigning weight ww to
    #       this new subinterval.
    #   --> Insert:
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
    def __init__( self, data=None ):
        """
        Uses the given data to initialise a map from { 1, ..., N } to weight
        vectors of dimension d, for some positive integers N and d.

        If no data is supplied, then the weight mapping is taken to have
        empty domain.

        Otherwise, the given data should be a list of length L, where L>0,
        such that for each i in { 0, ..., L-1 }, the ith entry of this data
        is a pair ( width<i>, weight<i> ), where:
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
        if data is None:
            self._dim = None
            return
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
        if self.isEmpty():
            return "An empty weight mapping"
        else:
            return ( "A map from {{ 1, ..., {} }} ".format(
                self.intervalLength() ) +
                "to weight vectors of dimension {}".format( self._dim ) )

    def __repr__(self):
        if self.isEmpty():
            return "Weights()"

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
        msg = str(self)
        msg += "\n{}\n".format( "-" * len(msg) )
        start = 1
        for i in range( len( self._weights ) ):
            end, weight = self._weights[i]
            msg += "Interval [{}, {}] --> Vector {}\n".format(
                    start, end, weight )
            start = end + 1
        return msg

    def isEmpty(self):
        """
        Is this weight mapping empty?

        Returns:
            True if and only if the domain of this weight mapping is empty.
        """
        return (not self._weights)

    def dimension(self):
        """
        Returns the dimension of the vectors in the image of this weight
        mapping.

        If this weight mapping is empty, then the dimension might not have
        been defined yet, which means that this routine might return None.

        Returns:
            The dimension of the weight vectors, or None if this dimension
            has not been defined yet.
        """
        return self._dim

    def intervalLength(self):
        """
        Returns the interval length N of this weight mapping.
        """
        if self.isEmpty():
            return 0
        else:
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
        if self.isEmpty():
            return None
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
        #       [start,end] ends just before the ith subinterval S, or it
        #       ends somewhere inside S (except at the very end of S, since
        #       we would otherwise have incremented i in the previous step).
        #       In this case, one of the following tasks remains:
        #       --- If [start,end] ends inside S, then we can finish the
        #           adding weight procedure by simply inserting a new
        #           subinterval.
        #       --- If [start,end] ends just before S, then there is nothing
        #           left to do unless the weight assigned to end is now equal
        #           to the weight assigned to S, in which case we need to
        #           merge S with the (i-1)st subinterval.
        #NOTE In the worst case, this last step requires O(C+m)-time, since
        #   it might involve either a pop or an insertion operation.
        if i == self.countSubintervals():
            return foundIndex
        currentWeight = self._weights[i][1]
        if i == 0:
            previousEnd = 0
        else:
            previousEnd, previousWeight = self._weights[i-1]
        if end > previousEnd:
            # The case where [start,end] ends inside S.
            self._weights.insert(
                    i, [ end, _vectorSum( currentWeight, weight ) ] )
        elif previousWeight == currentWeight:
            # The case where [start,end] ends just before S.
            self._weights.pop(i-1)
        return foundIndex

    def transferBy( self, pairing ):
        """
        Transfers the weights in the range of the given pairing to smaller
        orbit representatives.

        The transfer operation has no effect if the given pairing is a
        restriction of the identity map. Otherwise, this operation proceeds
        in one of three ways:
        --> If the given pairing is orientation-reversing, then the very
            first step is to ensure, by trimming if necessary, that its
            domain and range are disjoint. We then use the inverse of this
            pairing to transfer the weights from the range to the domain.
        --> If the given pairing is orientation-preserving but is not
            periodic (which means that there is a gap between the domain and
            range), then we again use the inverse of this pairing to transfer
            the weights from the range to the domain.
        --> If the given pairing is periodic with period p, then we use
            periodicity to transfer all the weights in the periodic interval
            I to the first p points in I.

        Let m = self.countSubintervals(), and let C denote the worst-case
        complexity of adding two arbitrary weights in the image of this
        weight mapping (roughly, C scales logarithmically with the size of
        the integers in the weight vectors). This routine runs in
        O(C*m^2)-time.

        Pre-condition:
        --> The pairing parameter is an instance of Pairing.

        Warning:
        --> As explained above, the requested transfer might involve trimming
            (and hence modifying) the given pairing.

        TODO:
        --> Optimise: improve running time from O(C*m^2) to O(C*m).

        Parameters:
        --> pairing     The pairing by which to transfer weights.

        Returns:
            None
        """
        if self.isEmpty() or pairing.isIdentity():
            return
        pairing.trim()

        # Handle the non-periodic case first, since this case is relatively
        # straightforward.
        #TODO This case currently requires O(C*m^2)-time, but it should be
        #   possible to improve it to O(C*m)-time.
        if not pairing.periodicInterval():
            # Find all the destinations for the weights that will be
            # transferred out of the range of the given pairing.
            #NOTE We require O(m)-time to find the subinterval containing the
            #   start of the range of pairing, and then O(m)-time to visit
            #   each subinterval that meets the range of pairing.
            transferInstructions = []
            start = pairing.rangeStart()
            i, _, end, weight = self._findSubinterval(start)
            while start <= pairing.rangeEnd():
                # To where should we transfer the weights on the current
                # constant-weight subinterval?
                width = end - start + 1
                inverseStart = pairing.inverseImageStart( start, width )
                transferInstructions.append(
                        ( weight, inverseStart, width ) )

                # Find the next constant-weight subinterval.
                i += 1
                start = end + 1
                try:
                    end, weight = self._weights[i]
                except IndexError:
                    break
                if end > pairing.rangeEnd():
                    end = pairing.rangeEnd()

            # Set all the weights in the range of the given pairing to zero,
            # and then use the transferInstructions to ensure that orbit
            # weights are preserved.
            #TODO We require O(m^2)-time to run self.setZero(), but this can
            #   be optimised to O(m)-time.
            self.setZero( pairing.rangeStart(), pairing.width() )
            #TODO We need to make O(m) calls to self.addWeight(), requiring
            #   O(C*m^2)-time in total.
            #       Can possibly improve to O(C*m)-time by dividing into
            #   cases depending on whether the given pairing is
            #   orientation-preserving, and then exploiting what we know
            #   about the order of the subintervals to which we are adding
            #   weight.
            for weight, start, width in transferInstructions:
                self.addWeight( weight, start, width )
            return

        # Now handle the periodic case.
        #NOTE This case also currently requires O(C*m^2)-time, but again it
        #   should be possible to improve it to O(C*m)-time.
        period = pairing.periodicInterval()[2]
        transferInstructions = []
        a = pairing.domainStart()
        aMod = a % period
        start = pairing.rangeStart()
        #NOTE Similar to above, we require O(m)-time to find the subinterval
        #   containing start. We then need to visit O(m) subintervals that
        #   meet the range of pairing.
        i, _, end, weight = self._findSubinterval(start)
        while start <= pairing.rangeEnd():
            width = end - start + 1

            # Due to periodicity, the weights on the current constant-weight
            # subinterval get transferred at least (width // period) times to
            # the interval [a,a+period-1].
            transferInstructions.append( (
                [ (width // period) * w for w in weight ], a, period ) )

            # We get some extra weight transferred if the width of the
            # current constant-weight subinterval is not exactly divisible
            # by the period.
            remainder = width % period
            if remainder > 0:
                extraStart = (start - aMod) % period
                extraEnd = (extraStart + remainder - 1) % period
                if extraStart <= extraEnd:
                    transferInstructions.append(
                            ( weight, a + extraStart, remainder ) )
                else:
                    transferInstructions.append(
                            ( weight, a, extraEnd + 1 ) )
                    transferInstructions.append(
                            ( weight, a + extraStart, period - extraStart ) )

            # Find the next constant-weight subinterval.
            i += 1
            start = end + 1
            try:
                end, weight = self._weights[i]
            except IndexError:
                break
            if end > pairing.rangeEnd():
                end = pairing.rangeEnd()
        #TODO As above, we require O(m^2)-time to run self.setZero(), but
        #   this can be optimised to O(m)-time.
        self.setZero( pairing.rangeStart(), pairing.width() )
        #TODO We need to make O(m) calls to self.addWeight(), requiring
        #   O(C*m^2)-time in total. Similar to above, this can possibly be
        #   improved to O(C*m)-time.
        for weight, start, width in transferInstructions:
            self.addWeight( weight, start, width )
        return

    def extend( self, width, weight ):
        """
        Extends the domain of this weight mapping by the given width, and
        assigns the given weight to the new elements of the domain.

        This routine raises WeightDimensionError if:
        --> self.dimension() is not None; and
        --> len(weight) != self.dimension().

        Pre-condition:
        --> The given width is a positive integer.
        --> The given weight is a list of non-negative integers.

        Parameters:
        --> width   The width by which to extend the domain of this weight
                    mapping.
        --> weight  The weight to be assigned to the newly-added elements of
                    the domain.

        Returns:
            None
        """
        if self._weights and self._weights[-1][1] == weight:
            # Merge new subinterval with the last subinterval.
            self._weights[-1][0] += width
        else:
            self._weights.append( [ width, weight ] )

    def contract(self):
        """
        """
        #TODO
        pass
