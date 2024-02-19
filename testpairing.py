"""
Test suite for the Pairing class.
"""
from pairing import periodicPairing, Pairing


def testPairing():
    print()

    #######################################################################
    print( "============================================================" )
    print( " periodicPairing( start, end, period ) " )
    print( "------------------------------------------------------------" )
    print()
    periodicPairingTestCases = [
            [ 1, 6, 3, Pairing( 1, 4, 3, True ) ],
            [ 2, 8, 3, Pairing( 2, 5, 4, True ) ],
            [ 3, 10, 3, Pairing( 3, 6, 5, True ) ],
            [ 4, 12, 3, Pairing( 4, 7, 6, True ) ],
            [ 5, 14, 3, Pairing( 5, 8, 7, True ) ],
            [ 6, 12, 4, None ],
            [ 7, 14, 5, None ] ]
    for start, end, period, expected in periodicPairingTestCases:
        msg = "Period {} on [{}, {}] should be ".format(
                period, start, end )
        constructed = periodicPairing( start, end, period )
        if expected is None:
            msg += "impossible."
            print(msg)
            if constructed is not None:
                raise RuntimeError( "FAILED." )
        else:
            msg += "equivalent to:\n    {}.".format(expected)
            print(msg)
            perInt = ( start, end, period )
            if ( constructed != expected or
                    constructed.periodicInterval() != perInt ):
                print(constructed)
                raise RuntimeError( "FAILED." )
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
        print( msg + "        {}.".format(you) )
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
    print( " Pairing.truncate(newBound) " )
    print( "------------------------------------------------------------" )
    print()
    preserve = Pairing( 2, 5, 7, True )
    reverse = Pairing( 1, 7, 6, False )
    overlap = Pairing( 2, 5, 7, False )
    truncateTestCases = [
            [ preserve.clone(), 4, False, preserve ],
            [ reverse.clone(), 12, False, reverse ],
            [ preserve.clone(), 8, True, Pairing( 2, 5, 4, True ) ],
            [ overlap.clone(), 8, False, overlap ],
            [ reverse.clone(), 9, True, Pairing( 4, 7, 3, False ) ] ]
    for oldPairing, newBound, change, newPairing in truncateTestCases:
        msg = "{}\n    Truncating to {} should ".format(
                oldPairing, newBound )
        if change:
            print( msg + "yield:\n        {}.".format(newPairing) )
        else:
            print( msg + "do nothing." )
        if ( oldPairing.truncate(newBound) != change or
                oldPairing != newPairing ):
            print(oldPairing)
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

    #######################################################################
    print( "============================================================" )
    print( " Pairing.mergeWith(other) " )
    print( "------------------------------------------------------------" )
    print()
    nonPeriodic = Pairing( 2, 6, 3, True )
    periodic1 = periodicPairing( 1, 6, 3 )
    periodic2 = periodicPairing( 2, 10, 4 )
    periodic5 = periodicPairing( 5, 13, 2 )
    periodic6 = periodicPairing( 6, 19, 6 )
    periodic7 = periodicPairing( 7, 16, 3 )
    mergeWithTestCases = [
            [ nonPeriodic, periodic1, None ],
            [ periodic1, nonPeriodic, None ],
            [ periodic1, periodic2, None ],
            [ periodic2.clone(), periodic5, periodicPairing( 2, 13, 2 ) ],
            [ periodic6.clone(), periodic5, periodicPairing( 5, 19, 2 ) ],
            [ periodic6.clone(), periodic7, periodicPairing( 6, 19, 3 ) ] ]
    for me, you, expected in mergeWithTestCases:
        msg = "Merge:\n    {}\n    {}\nShould ".format( me, you )
        changed = me.mergeWith(you)
        if expected is None:
            msg += "be impossible."
            print(msg)
            if changed:
                raise RuntimeError( "FAILED." )
        else:
            msg += "yield:\n    {}.".format(expected)
            print(msg)
            if ( not changed ) or ( me != expected ):
                print(me)
                raise RuntimeError( "FAILED." )
        print()
    # End of test suite.
    print( "============================================================" )
    print()
    print( "+---------+" )
    print( "| PASSED! |" )
    print( "+---------+" )
    return


if __name__ == "__main__":
    testPairing()
