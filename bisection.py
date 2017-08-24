
def bisection(f,a,b,eps=1e-7):
    """
    finds the zero of f(x)=0 in th interval [a,b]
    """
    while ( abs(b-a) > eps ):
        left  = f(a)*f( 0.5*(a+b) )
        right = f(b)*f( 0.5*(a+b) )
        if ( left < 0 and right < 0 ):
            print "Warning! Two zeros in given interval exist, choose left one."
            right = +1
        elif left < 0:
            b = 0.5*(a+b)
        elif right < 0:
            a = 0.5*(a+b)
    return 0.5*(a+b)
