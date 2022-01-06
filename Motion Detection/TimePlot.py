from bokeh.core.property.container import ColumnData
from bokeh.models.layouts import Column
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.io import curdoc
from bokeh.models import HoverTool, ColumnDataSource
import pandas

#runs MotionDetector files and pulls df from there
from MotionDetector import df

#creates new columns in df with the date as string in the format of Day Hour:Minute:Second for use with HoverTool
df['strStart'] = df['Start'].dt.strftime("%D %H:%M:%S")
df['strEnd'] = df['End'].dt.strftime("%D %H:%M:%S")

#sets data source as df
cds = ColumnDataSource(df)

#changes theme to a dark theme
curdoc().theme = 'dark_minimal'

#sets figure up
p = figure(x_axis_type = 'datetime', height = 100, width =500, title = 'Motion Graph')

#makes the model full screen
p.sizing_mode = 'scale_both'

#removes minor ticker and makes only 1 tick on graph
p.yaxis.minor_tick_line_color = None
p.yaxis.ticker.desired_num_ticks = 1

#adds Hovertool so that it displays the start and end time of motion using the strings created before
hover = HoverTool(tooltips = [("Start ", '@strStart'), ('End ', '@strEnd')])
p.add_tools(hover)

#creates the quads in the plots (writing source neglects the need of df['col'])
q = p.quad(left = 'Start', right = 'End', bottom = 0, top = 1, source = cds)

#outs the file and displays it in a  browser window
output_file('TimePlot.html')
show(p)
