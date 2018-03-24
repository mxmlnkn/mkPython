#!/usr/bin/env python
# -*- coding: utf-8 -*-

def shiftYWithAxisRatio( ax, y, r ):
    """
    returns a new y data point which represents the old y0 shifted by
    a ratio of the visible ylim, i.e. r=1 will increase y0 such that the new
    point would lie one y-axis-height above y0 (without a rescale)
    """
    y = np.array( y )
    y0 = ax.get_ylim()[0]
    y1 = ax.get_ylim()[1]
    from numpy import exp, log
    # r=0 => return y0, r=1 => return y1
    return y * exp( r * log( y1/y0 ) )

def addScaling( ax, x, y, exponent = None, xLabelPos = 0.5, interval = None, distance = 0.02, logscaling = None, color = 'k' ):
    """
    x,y     plot data, e.g. ax.get_lines()[-1].get_xdata() and get_ydata()
            can be used intuitively to add a scaling to the last plotted data
    exponent    the exponent for power scaling O(x^exponent) if logscaling = None
    logscaling  can be either 'log', 'nlog' or 'nlog2' for log scaling,
                O(n log(n)) and O(n log^2(n)) scaling. If further scalings are
                needed maybe it would be better to give some kind of functional
                as input
    xLabelPos   Useful if the label clashes with something else.
                0.5 means the center (in log-log-plot) of the plotted scaling.
                0 means the label will be centered about the mostleft scaling
                plot point
    distance    If distance is negative, then the scaling and the label will be
                put left / above of the data points x,y. distance = 0 will
                plot the scaling as fitted, although that might not be exactly
                ontop of each other if the scaling is drawn further than
                appliable
                The value itself was intended to be a ratio for the range of
                y data given. I.e. distance=1 will shift the scaling out of
                range if the plot range is chosen to fit exactly the range of y
    interval    if set to a tuple [0,1]^2 then the scaling will be plotted in
                that range where 1 is the mostright value 0 the first lowest
                0.5 specifies the center between min and max in log-log(!) plot
    """
    import numpy as np

    assert len(x) == len(y)
    assert ( exponent is None ) != ( logscaling is None ) # only one may be set!

    # Find significant intervals in (x,y) which scale with x^exponent
    x = np.log10( x )
    y = np.log10( y )
    from scipy.stats import linregress
    nPointsPerSection = min( 5, len( x ) )
    slopes = []
    from mkPython.ceilDiv import ceilDiv
    for iSection in range( ceilDiv( len(x), nPointsPerSection ) ):
        xSub = x[ iSection * nPointsPerSection : (iSection+1) * nPointsPerSection ]
        ySub = y[ iSection * nPointsPerSection : (iSection+1) * nPointsPerSection ]
        slope = linregress( xSub, ySub )[0]
        slopes += [ slope ]
    slopes = np.array( slopes )
    #print "slopes =",slopes

    # this is a dirty hack, because logscaling is not yet exactly implemented
    # in the calculation of the fitting interval ...
    if logscaling is not None:
        exponent = 1

    if ( interval is None ) or ( len( interval ) == 0 ) or ( interval[0] is None ) or ( ( len( interval ) > 1 ) and interval[1] is None ):
        # select all those 30% close to exponent
        iCloseSlopes = np.less_equal( np.abs( ( slopes - exponent ) / exponent ), 0.3 )
        #print "iCloseSlopes =",iCloseSlopes
        # fill in some gaps shorther than 1 per 5 sections
        # gabs does not the first and last sequences.
        # Also only fill gaps which are false i.e. not close enough to the
        # exponent
        iPos, lengths = findSequences( iCloseSlopes )
        for i in range( 1, len( lengths )-1 ):
            if lengths[i] < len( iCloseSlopes ) / 5:
                iCloseSlopes[ iPos[i] : iPos[i] + lengths[i] ] = True
        #print "iCloseSlopes (filled) =",iCloseSlopes

        # Find the longest sequence now
        iPos, lengths = findSequences( iCloseSlopes )
        iStart = iPos[ np.argmax( lengths ) ] * nPointsPerSection
        #print "iPos =",iPos,", lengths =",lengths
        #print "iStart =",iStart,", max(lengths) =", np.max(lengths)
        xScaling = x[ iStart : iStart + np.max( lengths ) * nPointsPerSection ]
        yScaling = y[ iStart : iStart + np.max( lengths ) * nPointsPerSection ]

        iFix = iStart + np.max( lengths ) * nPointsPerSection / 2
    else:
        if 0 <= interval[0] and interval[0] <= 1:
            xmin = np.min(x) + interval[0] * ( np.max(x) - np.min(x) )
        else:
            xmin = np.log10( interval[0] )
        if 0 <= interval[1] and interval[1] <= 1:
            xmax = np.min(x) + interval[1] * ( np.max(x) - np.min(x) )
        else:
            xmax = np.log10( interval[1] )
        iToUse = np.flatnonzero( np.logical_and( x >= xmin, x <= xmax ) )
        xScaling = x[ iToUse ]
        yScaling = y[ iToUse ]
        # @todo use a point in the middle to affix the y-shift instead off the
        #       the first or the last which can have a noticable different slope
        iFix = iToUse[ len( iToUse ) / 2 ]
    x0 = np.min( xScaling )  # is already the log of the source data!
    x1 = np.max( xScaling )
    y0 = np.min( yScaling )
    #print "x0 =",x0,", x1 =",x1,", y0 =",y0
    #print "iFix =",iFix

    def scaling(x):
        if logscaling is None:
            return x ** exponent
        elif logscaling == 'log':
            return np.log2( x )
        elif logscaling == 'nlog':
            return x * np.log2( x )
        elif logscaling == 'nlog2':
            return x * np.log2( x )**2
    xScaling = 10.**( np.linspace( x0, x1, 200 ) )
    yScaling = scaling( xScaling )
    yScaling *= 10**y[iFix] / scaling( 10**x[iFix] )

    # arrange the scaling data to look good, shift it a bit away from the data
    # in loglogplot to shift by d orthogonal this means we need to shift y by
    #  a > .''.d .'
    #    .'y|  :'  cos a = d / y
    #  .'___|.'
    #.'  ^ .'
    #    a = atan2( exp, 1 )
    #  => y = d / cos atan2( exp, 1 )
    #distance = 0.02
    yDistance = -distance / np.cos( np.arctan2( exponent, 1 ) )
    #print "yDistance =",yDistance,", exponent =",exponent
    yScaling = shiftYWithAxisRatio( ax, yScaling, yDistance )

    ax.plot( xScaling, yScaling, linestyle = '-', color = color )
    # add text label
    xLabel = xScaling[ int( xLabelPos * len( xScaling ) ) ]
    yLabel = yScaling[ int( xLabelPos * len( xScaling ) ) ]
    #distance = 0
    yDistance = 0# -distance / np.cos( np.arctan2( exponent, 1 ) )
    yLabel = shiftYWithAxisRatio( ax, yLabel, yDistance )

    if logscaling is None:
        formula = "N"
        if exponent != 1:
            formula += r"^" + str( exponent )
    elif logscaling == 'log':
        formula = r"\mathrm{log}\left( N \right)"
    elif logscaling == 'nlog':
        formula = r"N \mathrm{log}\left( N \right)"
    elif logscaling == 'nlog2':
        formula = r"N \mathrm{log}^2\left( N \right)"
    ax.annotate( r"$\mathcal{O}\left(" + formula + r"\right)$",
                 ( xLabel, yLabel ),
                 horizontalalignment = 'left' if distance > 0 else 'right',
                 verticalalignment = 'top' if distance > 0 else 'bottom',
                 color = color )
