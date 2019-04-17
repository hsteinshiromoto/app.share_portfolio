import numpy as np

from flask import Flask, render_template

from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

def make_figure():
    plot = figure(width=750, height=450, title='United States Import/Exports')

    y = np.random.rand(100, 1).squeeze()
    x = np.array(range(len(y))).squeeze()

    plot.line(x, y, color='#A6CEE3', legend='Exports')

    return plot


@app.route('/')
def greet():
    greetings = 'Hello World, I am BOKEH'
    plot = make_figure()
    script, div = components(plot)

    return render_template('index.html', greetings=greetings, script=script, div=div)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

"""
Example from https://programminghistorian.org/en/lessons/visualizing-with-bokeh is working

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
                          ColumnDataSource, Panel,
                          FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
                                  Tabs, CheckboxButtonGroup,
                                  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16


# Make plot with histogram and return tab
def histogram_tab(flights):
    # Function to make a dataset for histogram based on a list of carriers
    # a minimum delay, maximum delay, and histogram bin width
    def make_dataset(carrier_list, range_start=-60, range_end=120, bin_width=5):
        # Dataframe to hold information
        by_carrier = pd.DataFrame(columns=['proportion', 'left', 'right',
                                           'f_proportion', 'f_interval',
                                           'name', 'color'])

        range_extent = range_end - range_start

        # Iterate through all the carriers
        for i, carrier_name in enumerate(carrier_list):
            # Subset to the carrier
            subset = flights[flights['name'] == carrier_name]

            # Create a histogram with 5 minute bins
            arr_hist, edges = np.histogram(subset['arr_delay'],
                                           bins=int(range_extent / bin_width),
                                           range=[range_start, range_end])

            # Divide the counts by the total to get a proportion
            arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 'left': edges[:-1], 'right': edges[1:]})

            # Format the proportion
            arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in
                                    zip(arr_df['left'], arr_df['right'])]

            # Assign the carrier for labels
            arr_df['name'] = carrier_name

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            by_carrier = by_carrier.append(arr_df)

        # Overall dataframe
        by_carrier = by_carrier.sort_values(['name', 'left'])

        return ColumnDataSource(by_carrier)

    def style(p):
        # Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width=700, plot_height=700,
                   title='Histogram of Arrival Delays by Airline',
                   x_axis_label='Delay (min)', y_axis_label='Proportion')

        # Quad glyphs to create a histogram
        p.quad(source=src, bottom=0, top='proportion', left='left', right='right',
               color='color', fill_alpha=0.7, hover_fill_color='color', legend='name',
               hover_fill_alpha=1.0, line_color='black')

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Carrier', '@name'),
                                    ('Delay', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                          mode='vline')

        p.add_tools(hover)

        # Styling
        p = style(p)

        return p

    def update(attr, old, new):
        carriers_to_plot = [carrier_selection.labels[i] for i in carrier_selection.active]

        new_src = make_dataset(carriers_to_plot,
                               range_start=range_select.value[0],
                               range_end=range_select.value[1],
                               bin_width=binwidth_select.value)

        src.data.update(new_src.data)

    # Carriers and colors
    available_carriers = list(set(flights['name']))
    available_carriers.sort()

    airline_colors = Category20_16
    airline_colors.sort()

    carrier_selection = CheckboxGroup(labels=available_carriers,
                                      active=[0, 1])
    carrier_selection.on_change('active', update)

    binwidth_select = Slider(start=1, end=30,
                             step=1, value=5,
                             title='Bin Width (min)')
    binwidth_select.on_change('value', update)

    range_select = RangeSlider(start=-60, end=180, value=(-60, 120),
                               step=5, title='Range of Delays (min)')
    range_select.on_change('value', update)

    # Initial carriers and data source
    initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]

    src = make_dataset(initial_carriers,
                       range_start=range_select.value[0],
                       range_end=range_select.value[1],
                       bin_width=binwidth_select.value)
    p = make_plot(src)

    # Put controls in a single element
    controls = WidgetBox(carrier_selection, binwidth_select, range_select)

    # Create a row layout
    layout = row(controls, p)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Histogram')


    return tab

# Read data into dataframes
flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'), index_col=0).dropna()

# Create each of the tabs
tab1 = histogram_tab(flights)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1])

# Put the tabs in the current document for display
curdoc().add_root(tabs)

"""

"""
Basic Example is working

# Command to run:
# bokeh serve app/app.py --port 5000 --address '0.0.0.0' --allow-websocket-origin=0.0.0.0:xxxxx,
# where xxxxx is the port mapped to 5000

from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

# add a text renderer to our plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

i = 0

ds = r.data_source

# create a callback that will add a number in a random location
def callback():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds.data['x'] + [random()*70 + 15]
    new_data['y'] = ds.data['y'] + [random()*70 + 15]
    new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i%3]]
    new_data['text'] = ds.data['text'] + [str(i)]
    ds.data = new_data

    i = i + 1

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
"""