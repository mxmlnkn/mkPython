"""
Todo:
    - only average trajectory over certain time interval, which maybe can be given ...
"""

from numpy import *
from matplotlib.pyplot import * #xlabel,ylabel,plot,legend,show,step,connect,title,setp
from matplotlib import animation
import argparse
import os.path

# Animation
DPI  = matplotlib.rcParams['figure.dpi']

data = genfromtxt( "./simdata.dat", dtype='float', comments='#' )

fig = figure( figsize = ( 800./DPI, 600./DPI ) )
ax = subplot( 111,
    xlim = ( 0, ceil(amax(data[0::2])) ),
    ylim = ( 0, ceil(amax(data[1::2])) )
)
scatter, = ax.plot( data[0], data[1], "bo" )

subplots_adjust( bottom=0.1, left=.05, right=.95, top=.90, hspace=.35 )

# Animation control stuff
clear = True
paused = False
currentFrame = 0

def init():
    scatter.set_data([],[])
    return scatter,

def animate(i):
    global currentFrame
    if not paused:
        currentFrame = (currentFrame + 1) % numberOfFrames
    if clear:
        scatter.set_data( data[2*currentFrame], data[2*currentFrame+1] )
    else:
        a = data[0]
        b = data[1]

        for k in range(1,currentFrame):
            a = np.concatenate( (a, data[2*k]  ) )
            b = np.concatenate( (b, data[2*k+1]) )

        scatter.set_data( a,b )
    return scatter,

numberOfFrames = data.shape[0] / 2
print "frames =",numberOfFrames
# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=numberOfFrames, interval=20, blit=True)
anim.save( "./Simulation2D60fps.mp4", fps=60, dpi=(DPI/800.*1920.), extra_args=['-vcodec', 'libx264'])

def key_analyzer(event):
    global clear, paused, currentFrame
    #print "Key "+str(event.key)+" pressed"
    if (event.key == 'home' or event.key == '0'):
        currentFrame = 0;
    if (event.key == 'end'):
        currentFrame = numberOfFrames-1
    if ( event.key == 'c' ):
        clear = not clear
    if ( event.key == ' ' or event.key == 'p' ):
        paused = not paused
    if ( event.key == 'right' or event.key == '+' ):
        currentFrame += 1
    if ( event.key == '-' ):
        currentFrame -= 1
    currentFrame = (currentFrame + 1) % numberOfFrames

connect('key_press_event', key_analyzer)

show()
exit()
