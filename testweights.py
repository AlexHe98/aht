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
            [ woutZeros, 4, 1, 7, False ],
            [ woutZeros, 4, 3, 6, False ],
            [ woutZeros, 3, 4, 5, False ],
            [ woutZeros, 2, 10, 3, False ],
            [ withZeros, 5, 2, 3, True ],
            [ withZeros, 5, 3, 3, True ],
            [ withZeros, 6, 3, 3, False ],
            [ withZeros, 4, 3, 3, True ],
            [ withZeros, 3, 3, 3, False ],
            [ withZeros, 4, 4, 3, True ],
            [ withZeros, 3, 5, 3, False ],
            [ withZeros, 4, 8, 2, False ],
            [ withZeros, 1, 9, 2, False ] ]
    for data, start, width, subintervals, isUnchanged in setZeroTestCases:
        weights = Weights(data)
        end = start + width - 1
        print( weights.detail() )
        msg = "    Set [{}, {}] to zero.".format( start, end )
        print(msg)
        print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
        print()
        weights.setZero( start, width )
        print( weights.detail() )
        if weights.countSubintervals() != subintervals:
            raise RuntimeError( "FAILED." )
        if ( weights == Weights(data) ) != isUnchanged:
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
            [ addWeightTestData, [1,2,3], 5, 5, 6 ],
            [ addWeightTestData, [1,2,3], 2, 8, 6 ],
            [ addWeightTestData, [1,2,3], 9, 3, 6 ],
            [ addWeightTestData, [1,2,3], 1, 14, 5 ],
            [ addWeightTestData, [1,2,3], 3, 10, 5 ],
            [ addWeightTestData, [2,2,2], 9, 4, 4 ],
            [ addWeightTestData, [2,2,2], 8, 9, 3 ],
            [ addWeightTestData, [2,2,2], 8, 5, 2 ] ]
    for data, summand, start, width, subintervals in addWeightTestCases:
        weights = Weights(data)
        end = start + width - 1
        print( weights.detail() )
        msg = "    Add {} to [{}, {}].".format( summand, start, end )
        print(msg)
        print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
        print()
        weights.addWeight( summand, start, width )
        print( weights.detail() )
        if weights.countSubintervals() != subintervals:
            raise RuntimeError( "FAILED." )
        print( "    ----------------------------------------------------" )
        print()
    return


def _testWeights(testName):
    print()

    # Which set of tests are we running?
    knownTestNames = [
            "all",
            "setZero",
            "addWeight" ]
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
