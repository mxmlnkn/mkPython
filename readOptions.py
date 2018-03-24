#!/usr/bin/env python
# -*- coding: utf-8 -*-

def readOptions( fname ):
    """
    Reads variables from comments like:
        # Smin=0 Smax=1 nSections=10 dt=0.0333333 nMoments=4
    """
    defs = {}
    with open( fname ) as f:
        for line in f:
            if line[0] != '#' or '=' not in line:
                continue
            #print( "[readOptions] line = " + line )
            lastKey = None
            # strip first char '#' and last char '\n' and split at spaces
            words = line[1:-1].split( ' ' )
            for i in range(len(words)):
                word = words[i]
                if word == '' or word == "=":
                    continue
                #print( "[readOptions] word = " + word )

                kv = word.split( '=' )      # key value pair
                assert( len(kv) <= 2 )

                if len(kv) == 1:
                    if i < len(words)-1 and words[i+1].count('=') != 0:
                        lastKey = kv[0]
                        defs[lastKey] = []
                    else:
                        assert( lastKey != None )
                        if isinstance( defs[lastKey], list ):
                            defs[lastKey] += [ kv[0] ]
                        else:
                            defs[lastKey] = [ defs[lastKey], kv[0] ]
                else:
                    lastKey       = kv[0]
                    defs[lastKey] = kv[1]
    return defs
