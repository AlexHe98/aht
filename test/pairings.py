"""
Test suite for the Pairings class.
"""
from sys import argv
from aht.pairing import Pairing
from aht.pairings import Pairings


def _testStatic():
    #######################################################################
    print( "============================================================" )
    print( " Pairings.findStaticIntervals() " )
    print( "------------------------------------------------------------" )
    print()
    pairings0 = Pairings( [
        Pairing( 3, 10, 3, False ),     # [3,5] <-> [10,12]
        Pairing( 2, 14, 5, True ) ] )   # [2,6] <-> [14,18]
    static0 = [
            [ 1, 1, 1 ],
            [ 7, 9, 3 ],
            [ 13, 13, 1 ] ]
    pairings1 = Pairings( [
        Pairing( 1, 7, 3, True ),       # [1,3] <-> [7,9]
        Pairing( 2, 5, 4, False ) ] )   # [2,5] <-> [5,8]
    static1 = [
            [ 5, 5, 1 ] ]
    pairings2 = Pairings( [
        Pairing( 1, 6, 1, False ),      # [1,1] <-> [6,6]
        Pairing( 5, 12, 1, True ),      # [5,5] <-> [12,12]
        Pairing( 4, 8, 5, False ) ] )   # [4,8] <-> [8,12]
    static2 = [
        [ 2, 3, 2 ],
        [ 8, 8, 1 ] ] 
    staticCases = [
            [ pairings0, static0 ],
            [ pairings1, static1 ],
            [ pairings2, static2 ] ]
    for pairings, static in staticCases:
        print( pairings.detail() )
        print( "Should have the following static intervals:" )
        for s in static:
            print( "    [{}, {}]".format( s[0], s[1] ) )
        print()
        if pairings.findStaticIntervals() != static:
            raise RuntimeError( "FAILED." )
        print( "--------------------------------------------------------" )
        print()
    return


def _testPairings(testName):
    print()

    # Which set of tests are we running?
    knownTestNames = [
            "all",
            "static" ]
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
    if testName in { "all", "static" }:
        _testStatic()

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
    _testPairings(testName)
