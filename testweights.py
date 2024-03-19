"""
Test suite for the Weights class.
"""
from sys import argv
from weights import Weights
from pairing import Pairing


def _testSetZero():
    #######################################################################
    print( "============================================================" )
    print( " Weights.setZero( start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    woutZeros = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 3, [4,5,6] ),     # [3,5]
            ( 2, [3,4,5] ),     # [6,7]
            ( 3, [2,3,4] ),     # [8,10]
            ( 3, [1,2,3] ) ]    # [11,13]
    expWout4_1 = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 1, [4,5,6] ),     # [3,3]
            ( 1, [0,0,0] ),     # [4,4]
            ( 1, [4,5,6] ),     # [5,5]
            ( 2, [3,4,5] ),     # [6,7]
            ( 3, [2,3,4] ),     # [8,10]
            ( 3, [1,2,3] ) ]    # [11,13]
    expWout4_3 = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 1, [4,5,6] ),     # [3,3]
            ( 3, [0,0,0] ),     # [4,6]
            ( 1, [3,4,5] ),     # [7,7]
            ( 3, [2,3,4] ),     # [8,10]
            ( 3, [1,2,3] ) ]    # [11,13]
    expWout3_4 = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 4, [0,0,0] ),     # [3,6]
            ( 1, [3,4,5] ),     # [7,7]
            ( 3, [2,3,4] ),     # [8,10]
            ( 3, [1,2,3] ) ]    # [11,13]
    expWout2_10 = [
            ( 1, [1,2,3] ),     # [1,1]
            ( 10, [0,0,0] ),     # [2,11]
            ( 2, [1,2,3] ) ]    # [12,13]
    withZeros = [
            ( 3, [2,3,4,5] ),   # [1,3]
            ( 4, [0,0,0,0] ),   # [4,7]
            ( 4, [1,2,3,4] ) ]  # [8,11]
    expWith6_3 = [
            ( 3, [2,3,4,5] ),   # [1,3]
            ( 5, [0,0,0,0] ),   # [4,8]
            ( 3, [1,2,3,4] ) ]  # [9,11]
    expWith3_3 = [
            ( 2, [2,3,4,5] ),   # [1,2]
            ( 5, [0,0,0,0] ),   # [3,7]
            ( 4, [1,2,3,4] ) ]  # [8,11]
    expWith3_5 = [
            ( 2, [2,3,4,5] ),   # [1,2]
            ( 5, [0,0,0,0] ),   # [3,7]
            ( 4, [1,2,3,4] ) ]  # [8,11]
    expWith4_8 = [
            ( 3, [2,3,4,5] ),   # [1,3]
            ( 8, [0,0,0,0] ) ]  # [4,11]
    expWith1_9 = [
            ( 9, [0,0,0,0] ),   # [1,9]
            ( 2, [1,2,3,4] ) ]  # [10,11]
    setZeroTestCases = [
            [ woutZeros, 4, 1, 1, ( 1, expWout4_1 ) ],
            [ woutZeros, 4, 3, 0, ( 1, expWout4_3 ) ],
            [ woutZeros, 3, 4, 1, ( 1, expWout3_4 ) ],
            [ woutZeros, 3, 4, 2, None ],
            [ woutZeros, 2, 10, 0, ( 0, expWout2_10 ) ],
            [ woutZeros, 2, 10, 1, None ],
            [ withZeros, 5, 2, 1, ( 1, withZeros ) ],
            [ withZeros, 5, 3, 0, ( 1, withZeros ) ],
            [ withZeros, 6, 3, 1, ( 1, expWith6_3 ) ],
            [ withZeros, 6, 3, 2, None ],
            [ withZeros, 4, 3, 0, ( 1, withZeros ) ],
            [ withZeros, 3, 3, 0, ( 0, expWith3_3 ) ],
            [ withZeros, 3, 3, 1, None ],
            [ withZeros, 4, 4, 0, ( 1, withZeros ) ],
            [ withZeros, 3, 5, 0, ( 0, expWith3_5 ) ],
            [ withZeros, 4, 8, 1, ( 1, expWith4_8 ) ],
            [ withZeros, 1, 9, 0, ( 0, expWith1_9 ) ] ]
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
            expectedIndex, expectedData = expected
            expectedWeights = Weights(expectedData)
            msg += "find index {}.".format(expectedIndex)
            print(msg)
            print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
            print()
            print( expectedWeights.detail() )
            if ( foundIndex != expectedIndex or
                    weights != expectedWeights ):
                print( weights.detail() )
                raise RuntimeError( "FAILED." )
        print( "--------------------------------------------------------" )
        print()
    return


def _testAddWeight():
    #######################################################################
    print( "============================================================" )
    print( " Weights.addWeight( weight, start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    addWeightTestData = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 4, [3,3,3] ),     # [4.7]
            ( 5, [1,1,1] ),     # [8,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp5_5 = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 1, [3,3,3] ),     # [4.4]
            ( 3, [4,5,6] ),     # [5.7]
            ( 2, [2,3,4] ),     # [8,9]
            ( 3, [1,1,1] ),     # [10,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp2_8 = [
            ( 1, [1,2,3] ),     # [1,1]
            ( 2, [2,4,6] ),     # [2,3]
            ( 4, [4,5,6] ),     # [4.7]
            ( 2, [2,3,4] ),     # [8,9]
            ( 3, [1,1,1] ),     # [10,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp9_3 = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 4, [3,3,3] ),     # [4.7]
            ( 1, [1,1,1] ),     # [8,8]
            ( 3, [2,3,4] ),     # [9,11]
            ( 1, [1,1,1] ),     # [12,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp1_14 = [
            ( 3, [2,4,6] ),     # [1,3]
            ( 4, [4,5,6] ),     # [4.7]
            ( 5, [2,3,4] ),     # [8,12]
            ( 2, [4,5,6] ),     # [13,14]
            ( 2, [3,3,3] ) ]    # [15,16]
    exp3_10 = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 1, [2,4,6] ),     # [3,3]
            ( 4, [4,5,6] ),     # [4.7]
            ( 5, [2,3,4] ),     # [8,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp9_4 = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 4, [3,3,3] ),     # [4.7]
            ( 1, [1,1,1] ),     # [8,8]
            ( 8, [3,3,3] ) ]    # [9,16]
    exp8_9 = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 9, [3,3,3] ),     # [4.12]
            ( 4, [5,5,5] ) ]    # [13,16]
    exp8_5 = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 13, [3,3,3] ) ]   # [4,16]
    exp2_3 = [
            ( 1, [1,2,3] ),     # [1,1]
            ( 2, [2,3,4] ),     # [2,3]
            ( 1, [4,4,4] ),     # [4.4]
            ( 3, [3,3,3] ),     # [5.7]
            ( 5, [1,1,1] ),     # [8,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp3_2 = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 1, [2,3,4] ),     # [3,3]
            ( 1, [4,4,4] ),     # [4.4]
            ( 3, [3,3,3] ),     # [5.7]
            ( 5, [1,1,1] ),     # [8,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp4_1 = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 1, [4,4,4] ),     # [4.4]
            ( 3, [3,3,3] ),     # [5.7]
            ( 5, [1,1,1] ),     # [8,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    exp3_6 = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 1, [2,3,4] ),     # [3,3]
            ( 4, [4,4,4] ),     # [4.7]
            ( 1, [2,2,2] ),     # [8,8]
            ( 4, [1,1,1] ),     # [9,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    addWeightTestCases = [
            [ addWeightTestData, [1,2,3], 5, 5, 1, ( 1, exp5_5 ) ],
            [ addWeightTestData, [1,2,3], 2, 8, 0, ( 0, exp2_8 ) ],
            [ addWeightTestData, [1,2,3], 9, 3, 2, ( 2, exp9_3 ) ],
            [ addWeightTestData, [1,2,3], 9, 3, 3, None ],
            [ addWeightTestData, [1,2,3], 1, 14, 0, ( 0, exp1_14 ) ],
            [ addWeightTestData, [1,2,3], 3, 10, 0, ( 0, exp3_10 ) ],
            [ addWeightTestData, [1,2,3], 3, 10, 1, None ],
            [ addWeightTestData, [2,2,2], 9, 4, 0, ( 2, exp9_4 ) ],
            [ addWeightTestData, [2,2,2], 8, 9, 2, ( 2, exp8_9 ) ],
            [ addWeightTestData, [2,2,2], 8, 5, 0, ( 2, exp8_5 ) ],
            [ addWeightTestData, [1,1,1], 2, 3, 0, ( 0, exp2_3 ) ],
            [ addWeightTestData, [1,1,1], 3, 2, 0, ( 0, exp3_2 ) ],
            [ addWeightTestData, [1,1,1], 4, 1, 0, ( 1, exp4_1 ) ],
            [ addWeightTestData, [1,1,1], 3, 6, 0, ( 0, exp3_6 ) ] ]
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
            expectedIndex, expectedData = expected
            expectedWeights = Weights(expectedData)
            msg += "find index {}.".format(expectedIndex)
            print(msg)
            print( "    {}".format( "-" * ( len(msg) - 4 ) ) )
            print()
            print( expectedWeights.detail() )
            if ( foundIndex != expectedIndex or
                    weights != expectedWeights ):
                print(foundIndex)
                print( weights.detail() )
                raise RuntimeError( "FAILED." )
        print( "--------------------------------------------------------" )
        print()
    return


def _testTransferBy():
    #######################################################################
    print( "============================================================" )
    print( " Weights.transferBy(pairing) " )
    print( "------------------------------------------------------------" )
    print()
    transferByTestData = [
            ( 3, [1,2,3] ),     # [1,3]
            ( 4, [3,3,3] ),     # [4,7]
            ( 5, [1,1,1] ),     # [8,12]
            ( 4, [3,3,3] ) ]    # [13,16]
    iden = Pairing( 6, 6, 11, True )            # [6,16] <-> [6,16]
    reversing = Pairing( 3, 6, 11, False )      # [3,13] <-> [6,16]
    trimmed = reversing.clone()
    trimmed.trim()                              # [3,9] <-> [10,16]
    nonPeriodic = Pairing( 2, 10, 7, True )     # [2,8] <-> [10,16]
    periodic = Pairing( 2, 6, 11, True )        # [2,12] <-> [6,16]
    reversingExp = [
            ( 2, [1,2,3] ),     # [1,2]
            ( 1, [4,5,6] ),     # [3,3]
            ( 3, [6,6,6] ),     # [4,6]
            ( 1, [4,4,4] ),     # [7,7]
            ( 2, [2,2,2] ),     # [8,9]
            ( 7, [0,0,0] ) ]    # [10,16]
    nonPeriodicExp = [
            ( 1, [1,2,3] ),     # [1,1]
            ( 2, [2,3,4] ),     # [2,3]
            ( 1, [4,4,4] ),     # [4,4]
            ( 3, [6,6,6] ),     # [5,7]
            ( 1, [4,4,4] ),     # [8,8]
            ( 1, [1,1,1] ),     # [9,9]
            ( 7, [0,0,0] ) ]    # [10,16]
    periodicExp = [
            ( 1, [1,2,3] ),     # [1,1]
            ( 2, [8,9,10] ),    # [2,3]
            ( 1, [8,8,8] ),     # [4,4]
            ( 1, [7,7,7] ),     # [5,5]
            ( 11, [0,0,0] ) ]   # [6,16]
    transferByTestCases = [
            [ transferByTestData, iden.clone(), iden,
                transferByTestData ],
            [ transferByTestData, reversing.clone(), trimmed,
                reversingExp ],
            [ transferByTestData, trimmed.clone(), trimmed,
                reversingExp ],
            [ transferByTestData, nonPeriodic.clone(), nonPeriodic,
                nonPeriodicExp ],
            [ transferByTestData, periodic.clone(), periodic,
                periodicExp ] ]
    for data, pairing, pairAfter, expectedData in transferByTestCases:
        weights = Weights(data)
        expected = Weights(expectedData)
        print( weights.detail() )
        msg = str(pairing)
        print( "    Transfer by:\n        {}.".format(msg) )
        print( "    {}".format( "-" * (len(msg)+5) ) )
        print()
        weights.transferBy(pairing)
        print( expected.detail() )
        if pairing != pairAfter or weights != expected:
            print( weights.detail() )
            raise RuntimeError( "FAILED." )
        print( "--------------------------------------------------------" )
        print()
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
