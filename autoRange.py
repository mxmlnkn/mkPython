#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        x = line.get_xdata()
        y = line.get_ydata()
        if axis == 'y':
            x,y = y,x

        import numpy as np
        unmasked = np.logical_not( np.isnan(y) )
        if isLog:
            np.logical_and( unmasked, x > 0 )

        xmin = np.nanmin( np.concatenate( [ [xmin], np.array(x)[unmasked] ] ) )
    return xmin

def axisMax( ax, axis ):
    xmax=float('-inf')
    isLog = axisIsLog( ax, axis )
    # this is bugged when using axvline or axhline, because it doesn't ignore
    # the huge values set by those functions. Workaround: Call autoRange
    # before ax[v|h]line, but that is not always wanted
    for line in ax.get_lines():
        x = line.get_xdata()
        y = line.get_ydata()
        if axis == 'y':
            x,y = y,x

        import numpy as np
        # mask not only NaNs per each x,y, but also mask all y-values whose
        # corresponding x-values are NaN!
        unmasked = np.logical_not( np.isnan(y) )
        if isLog:
            np.logical_and( unmasked, x > 0 )
        # have to use numpy here, because of:
        # https://stackoverflow.com/questions/4237914/python-max-min-builtin-functions-depend-on-parameter-order
        xmax = np.nanmax( np.concatenate( [ [xmax], np.array(x)[unmasked] ] ) )
    return xmax

def autoRange( axisObject, axisName, lb, rb = None ):
    if lb is None:
        return
    if rb is None:
        rb = lb
    ax = axisObject
    isLog = axisIsLog( ax, axisName )

    xmin = axisMin( ax, axisName )
    xmax = axisMax( ax, axisName )
    print( axisName + ": " + str(xmin) + "," + str(xmax) )

    from math import log,exp

    if isLog:
        dx   = log(xmax) - log(xmin)
        xmin /= exp( lb*( dx ) )
        xmax *= exp( rb*( dx ) )
    else:
        dx = xmax - xmin
        xmin -= lb*dx
        xmax += rb*dx

    if axisName == 'x':
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

from math import ceil
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
