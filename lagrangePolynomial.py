
def lagrangePolynomial(x0,y0):
    """
    This function approximates f so that f(x0)=y0 and returns f
    """
    assert( len(x0) == len(y0) )
    # number of values. Approximating polynomial is of degree n-1
    n = len(x0)
    assert( n > 1 )
    def tmp(x):
        res = 0
        for k in range(n):
            prod = y0[k]
            for j in range(n):
                if j != k:
                    prod *= (x0[j]-x)/(x0[j]-x0[k])
            res += prod
    return tmp


def lagrangePolynomial(x0,y0,x):
    """
    This function approximates f so that f(x0)=y0 and returns f(x) (not f)
    """
    return lagrangePolynomial(x0,y0)(x)
