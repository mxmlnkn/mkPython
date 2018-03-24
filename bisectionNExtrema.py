#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def bisectionNExtrema( f,a,b,nExtrema,nIterations=16,maxLevel=8,debug=False ):
    """
    " finds at least nExtrema extrema of f(x) in the interval (a,b)
    " assumes that b > a and that only one extremum exists in (a,b)
    " maxLevel ... specifies maximum iterations. In every iteration the
    "              interval count will be doubled in order to find more
    "              extrema
    """
    assert( nExtrema != 0 )
    nExtremaFound      = 0
    nIntervals         = nExtrema+1
    for curLevel in range(maxLevel):
        if nExtremaFound >= nExtrema:
            break
        xi = np.linspace( a,b,nIntervals )
        # not simply *2, because we don't want half of the xi be on the same
        # positions like in the last iteration as that could be unwanted if
        # one such x is exactly on an extrema
        dx = 1e-7*(b-a)
        assert( dx < 0.5*(xi[1]-xi[0]) )
        fIncreasing =  f(xi+dx) > f(xi-dx)
        nExtremaFound = np.sum( np.logical_xor( fIncreasing[:-1], fIncreasing[1:] ) )
        if debug:
            print "nIntervals = ",nIntervals," with ",nExtremaFound," extrema"
        nIntervals = nIntervals*2+1

    if nExtremaFound < nExtrema:
        return np.zeros(0)  # error code

    extrema = np.empty( nExtremaFound )
    curExtremum = 0
    extremumInInterval = np.logical_xor( fIncreasing[:-1], fIncreasing[1:] )
    for i in range(len(extremumInInterval)):
        if not extremumInInterval[i]:
            continue
        if debug:
            sys.stdout.write( "Find extremum in ["+str(xi[i])+","+str(xi[i+1])+"] : " )
        xmax = bisectionExtrema( f, xi[i], xi[i+1], nIterations, debug )
        if (xi[i] <= xmax) and (xmax <= xi[i+1]):  # check for error code of bisectionExtrema
            extrema[curExtremum] = xmax
            curExtremum += 1

        if debug:
            if (xi[i] <= xmax) and (xmax <= xi[i+1]):  # check for error code of bisectionExtrema
                print "found at ",xmax
            else:
                print "not found!"

    return extrema
