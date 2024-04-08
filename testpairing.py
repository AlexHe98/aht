"""
Test suite for the Pairing class.
"""
from sys import argv
from pairing import periodicPairing, Pairing


def _testPeriodicPairing():
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
    return


def _testEq():
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
    return


def _testWidth():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.width() " )
    print( "------------------------------------------------------------" )
    print()
    #TODO
    return


def _testTranslationDistance():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.translationDistance() " )
    print( "------------------------------------------------------------" )
    print()
    preserving3 = Pairing( 2, 5, 12, True )     # [2,13] <-> [5,16], period 3
    preserving8 = Pairing( 3, 11, 4, True )     # [3,6] <-> [11,14]
    reversing = Pairing( 1, 5, 5, False )       # [1,5] <-> [5,9]
    contract = preserving8.clone()
    contract.contract( 7, 4 )                   # [3,6] <-> [7,10]
    truncPres = preserving3.clone()
    truncPres.truncate(12)                      # [2,9] <-> [5,12]
    trim = reversing.clone()
    trim.trim()                                 # [1,4] <-> [6,9]
    truncRev = trim.clone()
    truncRev.truncate(7)                        # [3,4] <-> [6,7]
    merge = periodicPairing( 6, 21, 6 )
    merge.mergeWith(preserving3)                # [2,18] <-> [5,21], period 3
    transPP = Pairing( 5, 12, 4, True )
    transPP.transmitBy(preserving3)             # [2,5] <-> [3,6], period 1
    transRP = Pairing( 5, 12, 4, False )
    transRP.transmitBy(preserving3)             # [2,5] <-> [3,6]
    transPR = Pairing( 5, 6, 3, True )
    transPR.transmitBy(trim)                    # [2,4] <-> [5,7]
    transRR = Pairing( 5, 6, 3, False )
    transRR.transmitBy(trim)                    # [2,4] <-> [5,7]
    translationDistanceTestCases = [
            [ preserving3, 3 ],
            [ preserving8, 8 ],
            [ reversing, -1 ],
            [ contract, 4 ],
            [ truncPres, 3 ],
            [ trim, -1 ],
            [ truncRev, -1 ],
            [ merge, 3 ],
            [ transPP, 1 ],
            [ transRP, -1 ],
            [ transPR, -1 ],
            [ transRR, 3 ] ]
    for pairing, distance in translationDistanceTestCases:
        msg = "{}\n    Should have ".format(pairing)
        if distance < 0:
            print( msg + "undefined translation distance." )
        else:
            print( msg + "translation distance {}.".format(distance) )
        if pairing.translationDistance() != distance:
            raise RuntimeError( "FAILED." )
        print()
    return


def _testDomainRange():
    #######################################################################
    print( "============================================================" )
    print( " Pairing domain and range " )
    print( "------------------------------------------------------------" )
    print()
    preserving1436 = Pairing( 3, 1, 4, True )
    preserving2468 = Pairing( 2, 6, 3, True )
    reversing1436 = Pairing( 1, 3, 4, False )
    reversing2468 = Pairing( 6, 2, 3, False )
    domainRangeEndpointTestCases = [
            [ preserving1436, 1, 4, 3, 6 ],
            [ preserving2468, 2, 4, 6, 8 ],
            [ reversing1436, 1, 4, 3, 6 ],
            [ reversing2468, 2, 4, 6, 8 ] ]
    for pairing, a, b, c, d in domainRangeEndpointTestCases:
        print( "{}\n    Should map from [{}, {}] to [{}, {}].".format(
            pairing, a, b, c, d ) )
        if ( pairing.domainStart() != a or
                pairing.domainEnd() != b or
                pairing.rangeStart() != c or
                pairing.rangeEnd() != d ):
            raise RuntimeError( "FAILED." )
        print()
    print( "    ----------------------------------------------------" )
    print()
    domainRangeContainsTestCases = [
            [ preserving1436, 2, 3, True, False ],
            [ reversing1436, 3, 3, False, True ],
            [ preserving1436, 3, 2, True, True ],
            [ reversing1436, 2, 4, False, False ],
            [ preserving2468, 2, 3, True, False ],
            [ reversing2468, 6, 3, False, True ],
            [ preserving2468, 4, 3, False, False ] ]
    for pair, start, width, domCont, ranCont in domainRangeContainsTestCases:
        msg = "{}\n    Domain should ".format(pair)
        if not domCont:
            msg += "not "
        cont = "contain [{}, {}].".format( start, start + width - 1 )
        msg += "{}\n    Range should ".format(cont)
        if not ranCont:
            msg += "not "
        print( msg + cont )
        if ( pair.domainContains( start, width ) != domCont or
                pair.rangeContains( start, width ) != ranCont ):
            raise RuntimeError( "FAILED." )
        print()
    print( "    ----------------------------------------------------" )
    print()
    domainRangeMeetsTestCases = [
            [ reversing1436, 1, 2, True, False ],
            [ preserving1436, 5, 3, False, True ],
            [ reversing1436, 2, 5, True, True ],
            [ preserving1436, 7, 3, False, False ],
            [ preserving2468, 1, 2, True, False ],
            [ reversing2468, 5, 3, False, True ],
            [ preserving2468, 4, 3, True, True ],
            [ reversing2468, 5, 1, False, False ] ]
    for pair, start, width, domMeet, ranMeet in domainRangeMeetsTestCases:
        msg = "{}\n    Domain should ".format(pair)
        if not domMeet:
            msg += "not "
        meet = "meet [{}, {}].".format( start, start + width - 1 )
        msg += "{}\n    Range should ".format(meet)
        if not ranMeet:
            msg += "not "
        print( msg + meet )
        if ( pair.domainMeets( start, width ) != domMeet or
                pair.rangeMeets( start, width ) != ranMeet ):
            raise RuntimeError( "FAILED." )
        print()
    return


def _testPreserving():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.isOrientationPreserving()" )
    print( "------------------------------------------------------------" )
    print()
    preserving = Pairing( 1, 2, 3, True )
    reversing = Pairing( 1, 2, 3, False )
    preservingTestCases = [
            [ preserving, True ],
            [ reversing, False ] ]
    for pairing, isPres in preservingTestCases:
        msg = "{}\n    Should be orientation-".format(pairing)
        if isPres:
            print( msg + "preserving." )
        else:
            print( msg + "reversing." )
        if ( pairing.isOrientationPreserving() != isPres or
                pairing.isOrientationReversing == isPres ):
            raise RuntimeError( "FAILED." )
        print()
    return


def _testIsIdentity():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.isIdentity() " )
    print( "------------------------------------------------------------" )
    print()
    iden = Pairing( 3, 3, 5, True )
    preserving = Pairing( 3, 4, 5, True )
    reversing = Pairing( 3, 3, 5, False )
    isIdentityTestCases = [
            [ iden, True ],
            [ preserving, False ],
            [ reversing, False ] ]
    for pairing, isIden in isIdentityTestCases:
        msg = "{}\n    Should ".format(pairing)
        if not isIden:
            msg += "not "
        print( msg + "be an identity map." )
        if pairing.isIdentity() != isIden:
            raise RuntimeError( "FAILED." )
        print()
    return


def _testImageStart():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.imageStart( start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    preserving = Pairing( 3, 7, 8, True )
    reversing = Pairing( 3, 7, 8, False )
    imageStartTestCases = [
            [ preserving, 2, 3, None ],
            [ reversing, 2, 3, None ],
            [ preserving, 3, 3, 7 ],
            [ reversing, 3, 3, 12 ],
            [ preserving, 5, 4, 9 ],
            [ reversing, 5, 4, 9 ],
            [ preserving, 8, 3, 12 ],
            [ reversing, 8, 3, 7 ],
            [ preserving, 9, 3, None ],
            [ reversing, 9, 3, None ] ]
    for pairing, start, width, expected in imageStartTestCases:
        msg = "{}\n    Image of [{}, {}] should ".format(
                pairing, start, start + width - 1 )
        answer = pairing.imageStart( start, width )
        if expected is None:
            print( msg + "be undefined." )
            if answer is not None:
                print(answer)
                raise RuntimeError( "FAILED." )
        else:
            print( msg + "have start point {}.".format(expected) )
            if answer != expected:
                print(answer)
                raise RuntimeError( "FAILED." )
        print()
    return


def _testInverseImageStart():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.inverseImageStart( start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    preserving = Pairing( 3, 7, 8, True )
    reversing = Pairing( 3, 7, 8, False )
    inverseImageStartTestCases = [
            [ preserving, 6, 3, None ],
            [ reversing, 6, 3, None ],
            [ preserving, 7, 3, 3 ],
            [ reversing, 7, 3, 8 ],
            [ preserving, 9, 4, 5 ],
            [ reversing, 9, 4, 5 ],
            [ preserving, 12, 3, 8 ],
            [ reversing, 12, 3, 3 ],
            [ preserving, 13, 3, None ],
            [ reversing, 13, 3, None ] ]
    for pairing, start, width, expected in inverseImageStartTestCases:
        msg = "{}\n    Inverse image of [{}, {}] should ".format(
                pairing, start, start + width - 1 )
        answer = pairing.inverseImageStart( start, width )
        if expected is None:
            print( msg + "be undefined." )
            if answer is not None:
                print(answer)
                raise RuntimeError( "FAILED." )
        else:
            print( msg + "have start point {}.".format(expected) )
            if answer != expected:
                print(answer)
                raise RuntimeError( "FAILED." )
        print()
    return


def _testPeriodicInterval():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.periodicInterval() " )
    print( "------------------------------------------------------------" )
    print()
    nonPeriodic = Pairing( 2, 6, 3, True )  # [2,4] <-> [6,8]
    periodic1 = Pairing( 1, 4, 3, True )    # [1,3] <-> [4,6], period 3
    periodic2 = Pairing( 2, 6, 5, True )    # [2,6] <-> [6,10], period 4
    periodic5 = Pairing( 5, 7, 7, True )    # [5,11] <-> [7,13], period 2
    periodic6 = Pairing( 6, 12, 8, True )   # [6,13] <-> [12,19], period 6
    periodic7 = Pairing( 7, 10, 7, True )   # [7,13] <-> [10,16], period 3
    periodicIntervalTestCases = [
            [ nonPeriodic, () ],
            [ periodic1, ( 1, 6, 3 ) ],
            [ periodic2, ( 2, 10, 4 ) ],
            [ periodic5, ( 5, 13, 2 ) ],
            [ periodic6, ( 6, 19, 6 ) ],
            [ periodic7, ( 7, 16, 3 ) ] ]
    for pairing, periodicInterval in periodicIntervalTestCases:
        msg = "{}\n    Should ".format(pairing)
        if periodicInterval:
            msg += "give periodic interval [{}, {}] with period {}.".format(
                    *periodicInterval )
        else:
            msg += "not be periodic."
        print(msg)
        if pairing.periodicInterval() != periodicInterval:
            print( pairing.periodicInterval() )
            raise RuntimeError( "FAILED." )
        print()
    return


def _testFixedPoints():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.fixedPoints( start, width ) " )
    print( "------------------------------------------------------------" )
    print()
    apart = Pairing( 6, 11, 4, True )       # [6,9] <-> [11,14]
    apart2_3 = [
            [2,4,3] ]
    apart3_7 = [
            [3,5,3] ]
    apart4_8 = [
            [4,5,2],
            [10,10,1] ]
    apart4_13 = [
            [4,5,2],
            [10,10,1],
            [15,16,2] ]
    apart6_3 = []
    apart7_4 = [
            [10,10,1] ]
    apart9_8 = [
            [10,10,1],
            [15,16,2] ]
    apart10_2 = [
            [10,10,1] ]
    apart10_6 = [
            [10,10,1],
            [15,15,1] ]
    apart12_3 = []
    apart13_5 = [
            [15,17,3] ]
    apart16_3 = [
            [16,18,3] ]
    touch = Pairing( 6, 10, 4, True )       # [6,9] <-> [10,13]
    touch2_3 = [
            [2,4,3] ]
    touch3_6 = [
            [3,5,3] ]
    touch4_10 = [
            [4,5,2] ]
    touch4_11 = [
            [4,5,2],
            [14,14,1] ]
    touch7_3 = []
    touch9_3 = []
    touch9_7 = [
            [14,15,2] ]
    touch10_4 = []
    touch10_7 = [
            [14,16,3] ]
    touch14_3 = [
            [14,16,3] ]
    reverse = Pairing( 6, 8, 5, False )     # [6,10] <-> [8,12]
    trimmed = reverse.clone()
    trimmed.trim()                          # [6,8] <-> [10,12]
    reverse2_3 = [
            [2,4,3] ]
    reverse3_4 = [
            [3,5,3] ]
    reverse4_6 = [
            [4,5,2],
            [9,9,1] ]
    reverse4_7 = [
            [4,5,2],
            [9,9,1] ]
    reverse5_10 = [
            [5,5,1],
            [9,9,1],
            [13,14,2] ]
    reverse6_3 = []
    reverse6_4 = [
            [9,9,1] ]
    reverse7_6 = [
            [9,9,1] ]
    reverse7_8 = [
            [9,9,1],
            [13,14,2] ]
    reverse9_1 = [
            [9,9,1] ]
    reverse9_3 = [
            [9,9,1] ]
    reverse9_7 = [
            [9,9,1],
            [13,15,3] ]
    reverse11_2 = []
    reverse12_4 = [
            [13,15,3] ]
    reverse14_3 = [
            [14,16,3] ]
    fixedPointsCases = [
            [ apart.clone(), 2, 3, apart, apart2_3 ],
            [ apart.clone(), 3, 7, apart, apart3_7 ],
            [ apart.clone(), 4, 8, apart, apart4_8 ],
            [ apart.clone(), 4, 13, apart, apart4_13 ],
            [ apart.clone(), 6, 3, apart, apart6_3 ],
            [ apart.clone(), 7, 4, apart, apart7_4 ],
            [ apart.clone(), 9, 8, apart, apart9_8 ],
            [ apart.clone(), 10, 2, apart, apart10_2 ],
            [ apart.clone(), 10, 6, apart, apart10_6 ],
            [ apart.clone(), 12, 3, apart, apart12_3 ],
            [ apart.clone(), 13, 5, apart, apart13_5 ],
            [ apart.clone(), 16, 3, apart, apart16_3 ],
            [ touch.clone(), 2, 3, touch, touch2_3 ],
            [ touch.clone(), 3, 6, touch, touch3_6 ],
            [ touch.clone(), 4, 10, touch, touch4_10 ],
            [ touch.clone(), 4, 11, touch, touch4_11 ],
            [ touch.clone(), 7, 3, touch, touch7_3 ],
            [ touch.clone(), 9, 3, touch, touch9_3 ],
            [ touch.clone(), 9, 7, touch, touch9_7 ],
            [ touch.clone(), 10, 4, touch, touch10_4 ],
            [ touch.clone(), 10, 7, touch, touch10_7 ],
            [ touch.clone(), 14, 3, touch, touch14_3 ],
            [ reverse.clone(), 2, 3, trimmed, reverse2_3 ],
            [ trimmed.clone(), 3, 4, trimmed, reverse3_4 ],
            [ reverse.clone(), 4, 6, trimmed, reverse4_6 ],
            [ trimmed.clone(), 4, 7, trimmed, reverse4_7 ],
            [ reverse.clone(), 5, 10, trimmed, reverse5_10 ],
            [ trimmed.clone(), 6, 3, trimmed, reverse6_3 ],
            [ reverse.clone(), 6, 4, trimmed, reverse6_4 ],
            [ trimmed.clone(), 7, 6, trimmed, reverse7_6 ],
            [ reverse.clone(), 7, 8, trimmed, reverse7_8 ],
            [ trimmed.clone(), 9, 1, trimmed, reverse9_1 ],
            [ reverse.clone(), 9, 3, trimmed, reverse9_3 ],
            [ trimmed.clone(), 9, 7, trimmed, reverse9_7 ],
            [ reverse.clone(), 11, 2, trimmed, reverse11_2 ],
            [ trimmed.clone(), 12, 4, trimmed, reverse12_4 ],
            [ reverse.clone(), 14, 3, trimmed, reverse14_3 ] ]
    for pairing, start, width, pairingAfter, fixed in fixedPointsCases:
        msg = "{}\n    Inside [{},{}], ".format(
                pairing, start, start + width - 1 )
        if not fixed:
            print( msg + "there should be no fixed points." )
        else:
            print( msg + "the fixed points should be described by:" )
            for f in fixed:
                print( "        {}".format(f) )
        computed = pairing.fixedPoints( start, width )
        if computed != fixed:
            print(computed)
            raise RuntimeError( "FAILED." )
        if pairing != pairingAfter:
            raise RuntimeError( "FAILED." )
        print()
    return


def _testContract():
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
    return


def _testTruncate():
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
    return


def _testTrim():
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
    return


def _testMergeWith():
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
    return


def _testTransmitBy():
    #######################################################################
    print( "============================================================" )
    print( " Pairing.transmitBy(other) " )
    print( "------------------------------------------------------------" )
    print()
    preserving = Pairing( 2, 7, 16, True )
    reversing = Pairing( 2, 7, 16, False )
    trimmed = reversing.clone()
    trimmed.trim()
    outOfRange = Pairing( 7, 17, 7, False )
    overshoot5 = Pairing( 6, 12, 7, True )
    overshoot3 = Pairing( 6, 14, 7, True )
    overshoot1 = Pairing( 6, 16, 7, False )
    shiftDom = Pairing( 13, 15, 7, True )
    transmitByTestCases = [
            [ outOfRange.clone(), preserving.clone(), False,
                outOfRange, preserving ],
            [ overshoot5.clone(), reversing.clone(), False,
                overshoot5, trimmed ],
            [ overshoot5.clone(), preserving.clone(), True,
                Pairing( 2, 6, 7, True ), preserving ],
            [ overshoot3.clone(), preserving.clone(), True,
                Pairing( 4, 6, 7, True ), preserving ],
            [ overshoot1.clone(), preserving.clone(), True,
                Pairing( 6, 6, 7, False ), preserving ],
            [ shiftDom.clone(), preserving.clone(), True,
                Pairing( 3, 5, 7, True ), preserving ],
            [ overshoot3.clone(), reversing.clone(), True,
                Pairing( 4, 6, 7, False ), trimmed ],
            [ overshoot1.clone(), trimmed.clone(), True,
                Pairing( 2, 6, 7, True ), trimmed ],
            [ shiftDom.clone(), reversing.clone(), True,
                Pairing( 3, 5, 7, True ), trimmed ] ]
    for trans, other, expCh, transAfter, otherAfter in transmitByTestCases:
        msg = "Transmit:\n    {}\nBy: {}\nShould ".format(
                trans, other )
        if expCh:
            print( msg + "yield:\n    {}\n    {}".format(
                transAfter, otherAfter ) )
        else:
            print( msg + "be impossible." )
        changed = trans.transmitBy(other)
        if changed != expCh or trans != transAfter or other != otherAfter:
            print( trans, transAfter )
            print( other, otherAfter )
            raise RuntimeError( "FAILED." )
        print()
    return


def _testPairing(testName):
    print()

    # Which set of tests are we running?
    knownTestNames = [
            "all",
            "periodicPairing",
            "eq",
            "width",
            "translationDistance",
            "domainRange",
            "preserving",
            "isIdentity",
            "imageStart",
            "inverseImageStart",
            "periodicInterval",
            "fixedPoints",
            "contract",
            "truncate",
            "trim",
            "mergeWith",
            "transmitBy" ]
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
    if testName in { "all", "periodicPairing" }:
        _testPeriodicPairing()
    if testName in { "all", "eq" }:
        _testEq()
    if testName in { "all", "width" }:
        _testWidth()
    if testName in { "all", "translationDistance" }:
        _testTranslationDistance()
    if testName in { "all", "domainRange" }:
        _testDomainRange()
    if testName in { "all", "preserving" }:
        _testPreserving()
    if testName in { "all", "isIdentity" }:
        _testIsIdentity()
    if testName in { "all", "imageStart" }:
        _testImageStart()
    if testName in { "all", "inverseImageStart" }:
        _testInverseImageStart()
    if testName in { "all", "periodicInterval" }:
        _testPeriodicInterval()
    if testName in { "all", "fixedPoints" }:
        _testFixedPoints()
    if testName in { "all", "contract" }:
        _testContract()
    if testName in { "all", "truncate" }:
        _testTruncate()
    if testName in { "all", "trim" }:
        _testTrim()
    if testName in { "all", "mergeWith" }:
        _testMergeWith()
    if testName in { "all", "transmitBy" }:
        _testTransmitBy()

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
    _testPairing(testName)
