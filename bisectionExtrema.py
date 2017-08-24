
def bisectionExtrema( f,a,b,nIterations=16,debug=False ):
    """
    " finds the extremum of f(x) in the interval (a,b)
    " assumes that b > a and that only one extremum exists in [a,b]
    """
    """
    " ^
    " |           .´
    " |  .'',   .'
    " |.'    ´'`
    " +--------------------
    "  a  c  b
    """
    extremaWasInside = True
    for i in range(nIterations):
        if b < a:
            a,b = b,a
        c  = 0.5 *(a+b)
        # everything smaller than interval width / 6 should basically be enough
        # if the factor is too small it may result in problems like the
        # bisection quitting too early, thereby giving back wrong maxima!
        dx = 1e-2*(b-a)
        # if floating point precision exhausted then these differences will be 0
        # for a and b do only onesided, because else we would leave the given interval!
        left   = f(a+dx) > f(a   )
        middle = f(c+dx) > f(c-dx)
        right  = f(b   ) > f(b-dx)
        if left == middle and middle == right and i == 0:
            extremaWasInside = False

        if debug:
            print "f at x=",a,"going up?",left  ," ( f(x+dx)=",f(a+dx),", f(x   =",f(a   )
            print "f at x=",c,"going up?",middle," ( f(x+dx)=",f(c+dx),", f(x-dx)=",f(c-dx)
            print "f at x=",b,"going up?",right ," ( f(x   )=",f(b   ),", f(x-dx)=",f(b-dx)

        # If the sign of the derivative is the same for all, then
        # the maximum is not inside the specified interval!
        if ( left == middle and middle == right ):
            if extremaWasInside:
                break   # this can also happen if dx is too small to resolve, so we break the search
            else:
                raise Exception(
                    "Specified Interval seems to not contain any extremum!\n" +
                    "  ["+str(a)+","+str(b)+"]: f(a)=" + str(f(a)) +
                    ", f((a+b)/2)=" + str(f(c)) + "f(b)=" + str(f(b))
                )
                return None, None, None # unreasonable result, therefore error code
        elif left == middle:
            a = c
        elif middle == right:
            b = c
        else:
            # This happens if there are two extrema inside interval
            raise Exception( "Specified Interval has more than one extremum!" )
            return None, None, None

    c = 0.5*(a+b)
    return f(c), c, 0.5*(b-a)
