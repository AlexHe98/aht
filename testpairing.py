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
    contractTestCases = [
            [ 3, 7, 2, True, 1, 2, True ],
            [ 3, 7, 2, False, 5, 2, True ],
            [ 3, 7, 2, True, 9, 2, True ],
            [ 3, 7, 2, False, 2, 2, False ],
            [ 3, 7, 2, True, 4, 2, False ],
            [ 3, 7, 2, False, 2, 4, False ],
            [ 3, 7, 2, True, 6, 3, False ],
            [ 3, 7, 2, False, 7, 3, False ],
            [ 3, 7, 2, True, 7, 2, False ],
            [ 3, 7, 2, False, 3, 7, False ],
            [ 1, 2, 3, True, 2, 2, False ] ]
    for a, c, pWidth, preserving, cStart, cWidth, legal in contractTestCases:
        pairing = Pairing( a, c, pWidth, preserving )
        msg = "{}. Contracting [{},{}] is ".format(
                pairing, cStart, cStart + cWidth - 1 )
        if legal:
            msg += "legal."
        else:
            msg += "illegal."
        print(msg)
        if pairing.contract( cStart, cWidth ) != legal:
            raise RuntimeError( "FAILED." )
        print()
    # End of test suite.
    print( "PASSED!" )
    return


if __name__ == "__main__":
    testPairing()
