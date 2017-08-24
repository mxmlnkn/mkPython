
def axisIsLog( ax, axis ):
    if axis == 'x':
        return ax.get_xscale() == 'log'
    elif axis == 'y':
        return ax.get_yscale() == 'log'
    else:
        assert( False, "axis neither 'x' nor 'y'!" )


def axisMin( ax, axis ):
    xmin=float('+inf')
    isLog = axisIsLog( ax, axis )
    for line in ax.get_lines():
        if axis == 'x':
            x = line.get_xdata()
        else:
            x = line.get_ydata()
        if isLog:
            x = x[ x>0 ]
        xmin = min( xmin, min(x) )
    return xmin

def axisMax( ax, axis ):
    xmax=float('-inf')
    isLog = axisIsLog( ax, axis )
    for line in ax.get_lines():
        if axis == 'x':
            x = line.get_xdata()
        else:
            x = line.get_ydata()
        if isLog:
            x = x[ x>0 ]
        xmax = max( xmax, max(x) )
    return xmax

def autoRange( ax, axis, lb, rb = None ):
    if rb == None:
        rb = lb
    isLog = axisIsLog( ax, axis )

    xmin = axisMin( ax, axis )
    xmax = axisMax( ax, axis )

    from math import log,exp

    if isLog:
        dx   = log(xmax) - log(xmin)
        xmin /= exp( lb*( dx ) )
        xmax *= exp( rb*( dx ) )
    else:
        dx = xmax - xmin
        xmin -= lb*dx
        xmax += rb*dx

    if axis == 'x':
        ax.set_xlim( [xmin,xmax] )
    else:
        ax.set_ylim( [xmin,xmax] )

def autoRangeXY( ax, lb = 0.1, rb = None, bb = None, tb = None ):
    if rb == None:
        rb = lb
    if tb == None:
        tb = lb
    if bb == None:
        bb = lb

    autoRange( ax, 'x', lb, rb )
    autoRange( ax, 'y', bb, tb )

def autoLabel( ax, axis, nbins=5, roundFunc=ceil ):
    """
    This functions is a workaround for ticks being too many or too few in
    log scale.
    https://github.com/matplotlib/matplotlib/issues/6549
    """
    from math import log10,ceil,floor
    xmin  = axisMin( ax, axis )
    xmax  = axisMax( ax, axis )
    isLog = axisIsLog( ax, axis )
    assert isLog # Autolabeling only implemented for log scale yet
    if isLog:
        dx = roundFunc( ( log10(xmax) - log10(xmin) ) / nbins )

    from numpy import arange
    n0 = int( floor( log10( xmin ) ) )
    n1 = int( ceil ( log10( xmax ) ) )
    #print "n0 =",n0,", n1 =",n1,", dx =",dx
    xpos = 10.**( n0 + arange(nbins+2)*dx )
    ax.set_xticks( xpos )
    #print "set xlabels at : ", xpos
