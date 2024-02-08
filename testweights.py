"""
Test suite for the Weights class.
"""
from weights import Weights


def testWeights():
    print()

    # Test Weights.setZero().
    print( "============================================================" )
    print( " Weights.setZero() " )
    print( "------------------------------------------------------------" )
    print()
    setZeroTestCases = [
            [ [ ( 2, [1,2,3] ),
                ( 3, [4,5,6] ),
                ( 2, [3,4,5] ),
                ( 3, [2,3,4] ),
                ( 3, [1,2,3] ) ], 4, 1, 7 ],]
    for data, start, width, subintervals in setZeroTestCases:
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
        print()
        print()
    #TODO
    w = Weights( [
        ( 2, [1,2,3] ),
        ( 3, [4,5,6] ),
        ( 2, [3,4,5] ),
        ( 3, [2,3,4] ),
        ( 3, [1,2,3] ) ] )
    print( w.detail() )

    print( "Set [2,3] to zero." )
    w.setZero( 2, 2 )
    print( w.detail() )

    print( "Set [5,10] to zero." )
    w.setZero( 5, 6 )
    print( w.detail() )


if __name__ == "__main__":
    testWeights()
