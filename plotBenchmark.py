#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def calcStatisticsFromDupes( x, y ):
    # If x contains duplicates, then those elements will be merged and the
    # corresponding elements in y will be calculated to mean + standard deviation
    # x,y must be numpy arrays
    assert( x.size == y.size )
    todo = ones( x.size, dtype=bool )
    i = 0
    xres = empty( x.size )
    yres = empty( y.size )
    yerr = empty( y.size )
    while todo.sum() > 0:
        assert( i < x.size )
        dupes = x == x[todo][0]
        xres[i] = x[dupes][0]
        yres[i] = mean( y[dupes] )
        yerr[i] = std( y[dupes] ) if y[dupes].size >= 3 else  0.
        i += 1
        # no found dupes should already be found!
        nextTodo = logical_and( todo, logical_not( dupes ) )
        assert( dupes.sum() == todo.sum() - nextTodo.sum() )
        todo = nextTodo
    return xres[:i], yres[:i], yerr[:i]

def plotBenchmark( ax, rx,ry,rz=None, label=None, color=None ):
    """
    " Creates multiple lines for each different z-Values (so there shouldn't
    " be too may different z values or the plot will get chaotic.
    " ^ y             +-----+
    " |           .´  |..z=1|
    " |  .'',   .'.´  |..z=2|
    " |.'.'',´'`.'.´  |..z=3|
    " |.'.'',´'`.'    +-----+
    " |.'    ´'`            x
    " +--------------------->
    " If there are multiple duplicate x-values to one z value, then the
    " corresponding st of y values will get merged to mean y +- std y
    """
    assert len(rx) == len(ry)
    if rz != None:
        assert len(ry) == len(rz)
    else:
        rz = zeros( len(rx) )
        params = array( [0] )
    # Sort z-values for correct coloring and overlay z-order
    params = sort( unique(rz) )
    colors = linspace( 0,1, len( params ) )
    for i in range( len(params) ):
        filter = rz == params[i]
        x = array( rx[filter] )
        y = array( ry[filter] )

        x,y,sy = calcStatisticsFromDupes( x, y )

        # sort by x-value or else the connecting line will make zigzags
        sorted = argsort( x )
        x  = x [sorted]
        y  = y [sorted]
        sy = sy[sorted]

        ax.errorbar( x, y, sy, linestyle='-', marker='.',
                     label=None if label == None else (
                        label if isinstance( label, basestring ) else
                        label( params[i] )
                     ), color=color if color != None or len(params) == 1 else
                            plt.get_cmap( 'cool' )(colors[i]) )

    autoRangeXY( ax, 0,0, 0.1,0.1 )
