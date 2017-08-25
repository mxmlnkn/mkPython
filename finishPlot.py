#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def finishPlot( fig, ax = None, fname = "finishPlot", loc='best', left = None, bottom = None, right = None, top = None, wspace = None, hspace = None, close = False ):
    """
    Give ax = [] in order to not draw a legend
    """
    fname = fname.replace( ":", "" )
    if ax is None:
        ax = fig.axes
    if not isinstance( ax, list):
        ax = [ ax ]
    for a in ax:
        # frameon = True necessary to work with seaborn
        l = a.legend( loc = loc, prop = {'size':10}, labelspacing = 0.2, # fontsize=10 also works
                      fancybox = True, framealpha = 0.5, frameon = True )
    #if l != None:
    #    l.set_zorder(0)  # alternative to transparency
    fig.tight_layout()
    fig.subplots_adjust( left = left, bottom = bottom, right = right, top = top, wspace = wspace, hspace = hspace )

    fig.savefig( fname+".pdf" )
    print( "[Saved '"+fname+".pdf']" )
    fig.savefig( fname+".png" )
    print( "[Saved '"+fname+".png']" )

    fig.canvas.set_window_title( fname )
    if close:
        plt.close( fig )
