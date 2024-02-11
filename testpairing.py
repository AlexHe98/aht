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
    #TODO
    if Pairing(1,2,3,True).contract(2,2):
        # This contraction should be illegal.
        raise RuntimeError( "FAILED." )
    print()
    # End of test suite.
    print( "PASSED!" )
    return


if __name__ == "__main__":
    testPairing()
