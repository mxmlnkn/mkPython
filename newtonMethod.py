
def newtonMethod(f,x0,eps=1e-7):
    """
    " finds the zero of f(x)=0 by iterating the derivative at xn and the
    " intersection point with the x-axis: t(x)=0 with t(xn)=f(xn) and
    " t'(xn)=f'(xn) => t(x) = f(xn) + f'(xn)*(x-xn)
    " t(x)=0 => x = xn - f(xn)/f'(xn) works only if f'(xn)=:m!=0
    """
    iterations = 0
    while ( abs(f(x0)) > eps ):
        iterations += 1
        m = (f(x0+eps)-f(x0-eps))/(2.0*eps)   # CDS
        #m = ( (f(x0+eps)-f(x0-eps))*2.0/3.0 - (f(x0+2.0*eps)-f(x0+2.0*eps))/12.0 )/eps # CDS O(eps**4)
        x0 = x0 - f(x0)/m
    print iterations,"Iterations needed to find x0 =",x0
    return x0
