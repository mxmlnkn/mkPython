
def readNamedColFile( fname, requiredSpecifier=[], allowedSpecifier=None, forbiddenSpecifier=[] ):
    """
    fname  : filename those data to load into a dictionary
    Was programmed for files with interleaved data, e.g.:
        #FORMAT x,y
        1.735092e-001
        3.603727e-001
        1.735477e-001
        3.603742e-001
        1.735861e-001
        3.603756e-001
    Here the the 1.7... values are for the x-position at different time steps
    (Was programmed for plotting Rutherod experiment simulated data
    """
    # allowed e.g. [ "t", "x", "y", "z", "px", "py", "pz", "dpx", "dpy", "dpz" ]
    data = genfromtxt( fname, dtype='float', comments='#', skip_footer=1 )

    # search for format identifier
    format       = None
    firstcomment = ""    # for downwards compatbility
    for line in open(fname):
        # ignore non-comment lines
        if line[0] != '#':
            break
        if firstcomment == "":
            firstcomment = line
        # read header
        if line.startswith( "#FORMAT" ):
            format = line[ len("#FORMAT") : ].strip()
            for c in format:
                # use the first non-alpha character after #FORMAT as the separator. That way both space and tabs as sepearator can be used and if tabs are used, space can be used in headings
                if not c.isalpha():
                    separator = c
                    break
            format = [x for x in format.split( separator ) if x] # ignore empty  split list entries
            break  # first header found will be used

    # downwards compatibility where no FORMAT was necessary (order was just assumend)
    # mimi = ""; print mimi.split() will at least return an empty list
    # so if format is None, then FORMAT was even found (in contrast to there
    # being no specifier after FORMAT)
    if format == None and firstcomment != "":
        format = firstcomment[1:].strip().split("\t")  # strip hashtag
        columns = True
    else:
        columns = False  # if FORMAT found, then anticipate strided columns where the 'columns' are other particles
    # downwards compatibility to old Electrons.dat files
    if not format:
        format = ['x','y']

    # check if all required columns are available and if none is forbidden
    correct  = True
    for id in requiredSpecifier:
        reqfound[id] = False
    for id in format:
        if not allowedSpecifier==None and not id in allowedSpecifier:
            print "unknown format specifier found (",id,") !"
            correct = False
        if id in forbiddenSpecifier:
            print "specifier >",id,"< is reserved and may not be used!"
            correct = False
        if sum( format == id ) > 1:
            print "specifier >",id,"< was used multiple times, not allowed!"
            correct = False
        if id in requiredSpecifier:
            reqfound[id] = True
    for id in requiredSpecifier:
        if reqfound[id] == False:
            print "required specifier >",id,"< wasn't found in header!"
            correct = False
    if not correct:
        exit()

    datadict = { 'N' : 0 }
    # get entry number which is length of column or if all data was written
    # in one columen with certain strides: len(col)/len(format)
    if len(data) > 0 and not columns:
        stride = len(format)
        # unweave data
        for i in range(stride):
            datadict.update( { format[i] : data[i::stride] } )
        # reshape if necessary and set number of particles
        if len(data.shape) > 1:
            datadict['N'] = len(data[0]) # number of columns in raw data
        else:
            datadict['N'] = 1  # N-Particles / strided columns
            # Changes 1D to 2D array where the second dimension will be the
            # particle number, that's why the time entries shouldn't be
            # changed in this manner only particle attributes
            for id in format:
                if id != "t":
                    datadict[id] = datadict[id].reshape( ( len(datadict[id]), datadict['N'] ) )
    if columns:
        assert( len(data[0]) == len(format) )
        datadict['N'] = len(data[:,0])
        # copy columns in respective dictionary entries
        for i in range(len(format)):
            datadict.update( { format[i] : data[:,i] } )
    print "Format = ",format,", Strided Multiparticle? ",not columns
    return datadict
