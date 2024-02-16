"""
Test suite for the Pairing class.
"""
from pairing import Pairing


def testPairing():
    print()

    #######################################################################
    print( "============================================================" )
    print( " Pairing.__eq__(other) " )
    print( "------------------------------------------------------------" )
    print()
    preserve0 = Pairing( 1, 2, 3, True )
    reverse0 = Pairing( 1, 2, 3, False )
    preserve1 = Pairing( 4, 3, 2, True )
    reverse1 = Pairing( 4, 3, 2, False )
    eqTestCases = [
            [ preserve0, preserve0.clone(), True ],
            [ preserve0, reverse0, False ],
            [ preserve0, preserve1, False ],
            [ reverse0, reverse0.clone(), True ],
            [ reverse0, reverse1, False ],
            [ preserve1, preserve1.clone(), True ],
            [ preserve1, reverse1, False ],
            [ reverse1, reverse1.clone(), True ] ]
    for me, you, eq in eqTestCases:
        msg = "{}\n    Should ".format(me)
        if eq:
            msg += "be equal to:\n"
        else:
            msg += "not be equal to:\n"
        print( msg + "        {}".format(you) )
        if ( me == you ) != eq:
            raise RuntimeError( "FAILED." )
        print()

    #######################################################################
    print( "============================================================" )
    print( " Pairing.contract( start, width ) " )
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

    #######################################################################
    print( "============================================================" )
    print( " Pairing.trim() " )
    print( "------------------------------------------------------------" )
    print()
    preserve = Pairing( 2, 4, 5, True )
    touching = Pairing( 2, 5, 3, False )
    apart = Pairing( 2, 6, 3, False )
    odd = Pairing( 2, 4, 5, False )
    even = Pairing( 2, 4, 6, False )
    trimTestCases = [
            [ preserve.clone(), False, preserve ],
            [ touching.clone(), False, touching ],
            [ apart.clone(), False, apart ],
            [ odd.clone(), True, Pairing( 2, 6, 3, False ) ],
            [ even.clone(), True, Pairing( 2, 6, 4, False ) ] ]
    for me, change, you in trimTestCases:
        msg = "{}\n    Trimming should ".format(me)
        if change:
            print( msg + "yield:\n        {}.".format(you) )
        else:
            print( msg + "do nothing." )
        if ( me.trim() != change ) or ( me != you ):
            print(me)
            print( "    {}".format( me._a ) )
            print( "    {}".format( me._c ) )
            print( "    {}".format( me.width() ) )
            print( "    {}".format( me._preserving ) )
            print(you)
            print( "    {}".format( you._a ) )
            print( "    {}".format( you._c ) )
            print( "    {}".format( you.width() ) )
            print( "    {}".format( you._preserving ) )
            raise RuntimeError( "FAILED." )
        print()
    # End of test suite.
    print( "PASSED!" )
    return


if __name__ == "__main__":
    testPairing()
