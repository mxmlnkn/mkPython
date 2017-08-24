
def relErr( x, y ):
    from numpy import zeros,abs
    assert( len(x) == len(y) )
    non0 = abs(y) > 1e-16
    #non0 = abs(y) != 0
    tmp = ( x[non0] - y[non0] ) / y[non0]
    res = zeros( len(y) )
    res[non0] = tmp
    return y[non0], abs(res[non0])
