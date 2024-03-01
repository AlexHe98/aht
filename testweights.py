"""
Test suite for the Weights class.
"""
from sys import argv
from weights import Weights


def _testSetZero():
    #######################################################################
    print( "============================================================" )
    print( " Weights.setZero( start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    woutZeros = [
            ( 2, [1,2,3] ),
            ( 3, [4,5,6] ),
            ( 2, [3,4,5] ),
            ( 3, [2,3,4] ),
            ( 3, [1,2,3] ) ]
    withZeros = [
            ( 3, [2,3,4,5] ),
            ( 4, [0,0,0,0] ),
            ( 4, [1,2,3,4] ) ]
    setZeroTestCases = [
            [ woutZeros, 4, 1, 1, ( 1, 7, False ) ],
            [ woutZeros, 4, 3, 0, ( 1, 6, False ) ],
            [ woutZeros, 3, 4, 1, ( 1, 5, False ) ],
            [ woutZeros, 3, 4, 2, None ],
            [ woutZeros, 2, 10, 0, ( 0, 3, False ) ],
            [ woutZeros, 2, 10, 1, None ],
            [ withZeros, 5, 2, 1, ( 1, 3, True ) ],
            [ withZeros, 5, 3, 0, ( 1, 3, True ) ],
            [ withZeros, 6, 3, 1, ( 1, 3, False ) ],
            [ withZeros, 6, 3, 2, None ],
            [ withZeros, 4, 3, 0, ( 1, 3, True ) ],
            [ withZeros, 3, 3, 0, ( 0, 3, False ) ],
            [ withZeros, 3, 3, 1, None ],
            [ withZeros, 4, 4, 0, ( 1, 3, True ) ],
            [ withZeros, 3, 5, 0, ( 0, 3, False ) ],
            [ withZeros, 4, 8, 1, ( 1, 2, False ) ],
            [ withZeros, 1, 9, 0, ( 0, 2, False ) ] ]
    for data, start, width, index, expected in setZeroTestCases:
        weights = Weights(data)
        end = start + width - 1
        print( weights.detail() )
        print( "    Set [{}, {}] to zero.".format( start, end ) )
        msg = "    Searching from index {} should ".format(index)
        foundIndex = weights.setZero( start, width, index )
        if expected is None:
            msg += "fail."
            print(msg)
            print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
            print()
            if foundIndex is not None:
                print( weights.detail() )
                raise RuntimeError( "FAILED." )
        else:
            expectedIndex, subintervals, isUnchanged = expected
            msg += "find index {}.".format(expectedIndex)
            print(msg)
            print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
            print()
            print( weights.detail() )
            if ( foundIndex != expectedIndex or
                    weights.countSubintervals() != subintervals or
                    ( weights == Weights(data) ) != isUnchanged ):
                raise RuntimeError( "FAILED." )
        print( "    ----------------------------------------------------" )
        print()
    return


def _testAddWeight():
    #######################################################################
    print( "============================================================" )
    print( " Weights.addWeight( weight, start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    addWeightTestData = [
            ( 3, [1,2,3] ),
            ( 4, [3,3,3] ),
            ( 5, [1,1,1] ),
            ( 4, [3,3,3] ) ]
    addWeightTestCases = [
            [ addWeightTestData, [1,2,3], 5, 5, 1, ( 1, 6 ) ],
            [ addWeightTestData, [1,2,3], 2, 8, 0, ( 0, 6 ) ],
            [ addWeightTestData, [1,2,3], 9, 3, 2, ( 2, 6 ) ],
            [ addWeightTestData, [1,2,3], 9, 3, 3, None ],
            [ addWeightTestData, [1,2,3], 1, 14, 0, ( 0, 5 ) ],
            [ addWeightTestData, [1,2,3], 3, 10, 0, ( 0, 5 ) ],
            [ addWeightTestData, [1,2,3], 3, 10, 1, None ],
            [ addWeightTestData, [2,2,2], 9, 4, 0, ( 2, 4 ) ],
            [ addWeightTestData, [2,2,2], 8, 9, 2, ( 2, 3 ) ],
            [ addWeightTestData, [2,2,2], 8, 5, 0, ( 2, 2 ) ] ]
    for data, summand, start, width, index, expected in addWeightTestCases:
        weights = Weights(data)
        end = start + width - 1
        print( weights.detail() )
        print( "    Add {} to [{}, {}].".format( summand, start, end ) )
        msg = "    Searching from index {} should ".format(index)
        foundIndex = weights.addWeight( summand, start, width, index )
        if expected is None:
            msg += "fail."
            print(msg)
            print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
            print()
            if foundIndex is not None:
                print( weights.detail() )
                raise RuntimeError( "FAILED." )
        else:
            expectedIndex, subints = expected
            msg += "find index {}.".format(expectedIndex)
            print(msg)
            print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
            print()
            print( weights.detail() )
            if ( foundIndex != expectedIndex or
                    weights.countSubintervals() != subints ):
                print(foundIndex)
                raise RuntimeError( "FAILED." )
        print( "    ----------------------------------------------------" )
        print()
    return


def _testTransferBy():
    #######################################################################
    print( "============================================================" )
    print( " Weights.transferBy(pairing) " )
    print( "------------------------------------------------------------" )
    print()
    #TODO
    return


def _testWeights(testName):
    print()

    # Which set of tests are we running?
    knownTestNames = [
            "all",
            "setZero",
            "addWeight",
            "transferBy" ]
    if testName not in knownTestNames:
        if testName == "":
            print( "Need to supply a test name." )
        else:
            print( "Unknown test name." )
        print()
        print( "The following tests are available:" )
        for name in knownTestNames:
            print( "    {}".format(name) )
        print()
        return

    # Run the requested set of tests.
    if testName in { "all", "setZero" }:
        _testSetZero()
    if testName in { "all", "addWeight" }:
        _testAddWeight()
    if testName in { "all", "transferBy" }:
        _testTransferBy()

    # End of test suite.
    print( "============================================================" )
    print()
    print( "+---------+" )
    print( "| PASSED! |" )
    print( "+---------+" )
    return


if __name__ == "__main__":
    try:
        testName = argv[1]
    except IndexError:
        testName = ""
    _testWeights(testName)
