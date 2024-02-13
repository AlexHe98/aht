"""
Test suite for the Pairing class.
"""
from pairing import Pairing


def testPairing():
    print()

    # Test Pairing.contract().
    print( "============================================================" )
    print( " Pairing.contract() " )
    print( "------------------------------------------------------------" )
    print()
    preserve = Pairing( 7, 3, 2, True )
    reverse = Pairing( 7, 3, 2, False )
    contractTestCases = [
            [ preserve.clone(), 1, 2, Pairing( 1, 5, 2, True ) ],
            [ reverse.clone(), 5, 2, Pairing( 3, 5, 2, False ) ],
            [ preserve.clone(), 9, 2, preserve ],
            [ reverse.clone(), 2, 2, None ],
            [ preserve.clone(), 4, 2, None ],
            [ reverse.clone(), 2, 4, None ],
            [ preserve.clone(), 6, 3, None ],
            [ reverse.clone(), 7, 3, None ],
            [ preserve.clone(), 7, 2, None ],
            [ reverse.clone(), 3, 7, None ],
            [ Pairing( 1, 2, 3, True ), 2, 2, None ] ]
    for oldPairing, start, width, newPairing in contractTestCases:
        msg = "{}\n    Contracting [{},{}] should ".format(
                oldPairing, start, start + width - 1 )
        if newPairing is None:
            print( msg + "be illegal." )
            if oldPairing.contract( start, width ):
                raise RuntimeError( "FAILED." )
        else:
            print( msg + "should yield:\n        {}.".format(newPairing) )
            if ( not oldPairing.contract( start, width ) or
                    oldPairing != newPairing ):
                raise RuntimeError( "FAILED." )
        print()
    # End of test suite.
    print( "PASSED!" )
    return


if __name__ == "__main__":
    testPairing()
