#!/usr/bin/env python
##a good example fromhttp://www.answermysearches.com/making-dynamic-charts-and-graphs-for-your-webpage/135/
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # force the antigrain backend
from matplotlib import rc
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.cbook import iterable
import matplotlib.numerix as nx

def make_fig():
    """ make a chart """
    fig = Figure()
    # add an axes at left, bottom, width, height; by making the bottom
    # at 0.3, we save some extra room for tick labels
    ax = fig.add_axes([0.2, 0.3, 0.7, 0.6]) #ie set sides of chart box
    #now we make the plots
    line,  = ax.plot([0,2,3,4],[100,200,230,250], 'ro--', markersize=12, markerfacecolor='g',label='Meters', linewidth=2)
    line,  = ax.plot([0,2,4],[1.5,25,3.5], 'bv--', markersize=12, markerfacecolor='g',label='Checks', linewidth=2)
    ax.legend() #stick in a legend
    # add some text decoration
    ax.set_title('Sales to Blue Credit')
    ax.set_ylabel('$Amount')
    ax.set_xticks( (0,1,2,3,4) ) #set these the same as x input into plot
    labels = ax.set_xticklabels(('2006-01-01', '2006-01-15', '2006-02-01', '2006-03-01'))
    canvas = FigureCanvasAgg(fig)

    #now let's handle the temp file stuff and print the output
    tempfilenum,tempfilename=tempfile.mkstemp(suffix='.png') #function print_figure below requires a suffix
    canvas.print_figure(tempfilename, dpi=150)
    imagefile=file(tempfilename,'rb')
    print "Content-type: image/png\\n"
    imagefile.seek(0)
    print imagefile.read()
    imagefile.close()
    os.close(tempfilenum) #close what tempfile.mkstemp opened
    os.remove(tempfilename) #clean up by removing this temp file

if __name__=='__main__':
    make_fig()