#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def finishPlot( fig, ax = None, fname = "finishPlot",
    loc='best', bbox_to_anchor = None,
    left = None, bottom = None, right = None, top = None,
    wspace = None, hspace = None, close = False, framealpha = 1, ncol = 1, fontsize = 10 ):
    """
    Give ax = [] in order to not draw a legend
    framealpha is by default turned off, because it produces transparency
    effects which are nto support by some laser printers and/or printer drivers
    resulting in the whole damn page to be rasterized visibly bad -.- >:|
    """
    fname = fname.replace( ":", "" )
    if ax is None:
        ax = fig.axes
    if not isinstance( ax, list):
        ax = [ ax ]
    for a in ax:
        # frameon = True necessary to work with seaborn
        l = a.legend( loc = loc, prop = { 'size' : fontsize }, labelspacing = 0.2, # fontsize=10 also works
                      fancybox = True, framealpha = framealpha, frameon = True,
                      bbox_to_anchor = bbox_to_anchor, ncol = ncol )
    #if l != None:
    #    l.set_zorder(0)  # alternative to transparency
    fig.tight_layout()
    fig.subplots_adjust( left = left, bottom = bottom, right = right, top = top, wspace = wspace, hspace = hspace )

    # eps output automatically kills all alphas even those in lines and other things
    # use eps2pdf then to convert them for pdflatex because pdlfatex can't include .eps images
    # actually that unfortunately only removes the alpha, not the color.
    # Therefore, for example, black with transparency 50% which looks gray becomes red!
    for ext in [ 'pdf', 'png' ]: #, 'eps' ]: # eps does not work with changed font.familys to lmodern it seems or rather \usepackage{lmodern} does not compile
        fig.savefig( fname + "." + ext )
        print( "[Saved '" + fname + "." + ext + "']" )

    fig.canvas.set_window_title( fname )
    if close:
        plt.close( fig )
