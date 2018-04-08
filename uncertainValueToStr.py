#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def uncertainValueToStr( x, sx ):
    import numpy as np
    def getMagnitude( x ):
        return int( np.floor( np.log10( np.abs( x ) ) ) ) # -0 for < 10, 1 for 10 <= x < 100, -1 for 0.1 < x < 0, ...
    def roundToSignificant( x, n ):
        mag = getMagnitude( x )
        # around only rounds to n-given decimals AFTER the dot, therefore we need to do the magnitude scaling, but this is actually helpful later for rounding the value in respect to the precision of the standard deviation
        return np.around( x / 10**mag, n-1 ) * 10**mag
    def getFirstDigit( x ):
        mag = getMagnitude( x )
        return int( x / 10**mag )

    # Format exponent and error https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4483789/
    # Can't find that particular standard right now, but I thought some standard specified two significant digits for the first digit being < 3 and else one significant digits on the errors. And of course the mean should have as much precision as the error has
    nDigitsErr = 2 if getFirstDigit( sx ) in [1,2] else 1
    magSx   = getMagnitude( sx )
    sxShort = str( roundToSignificant( sx, nDigitsErr ) )
    # pad with 0s if necessary, showing the rounding, i.e. avoid situations like 2.093 +- 0.02 (0.0213...)
    def existingDigits( s ):
        s = str(s)
        firstNonZero = [ s.find(d) for d in '123456789' if d in s ]
        firstNonZero = min( firstNonZero ) if len( firstNonZero ) > 0 else len(s)
        nDigits = np.sum( [ s[ firstNonZero: ].split('e')[0].count(d) for d in '0123456789' ] )
        #print( s, "first non-zero:", firstNonZero, "# digits:", nDigits )
        return nDigits
    xShort  = str( np.around( x / 10**magSx, nDigitsErr ) * 10**magSx )
    xShort += '0' * max( 0, nDigitsErr - existingDigits( str( np.around( x / 10**magSx, nDigitsErr ) ).split('.')[-1] ) )
    return xShort, sxShort
