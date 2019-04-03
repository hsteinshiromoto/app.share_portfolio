# from flask import Flask, render_template, request
# import pandas as pd
# from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.models import ColumnDataSource, FactorRange
#
# app = Flask(__name__)
#
# # Load the Iris Data Set
# feature_names = ["fruits", "2015", "2016", "2017"]
#
#
# # Create the main plot
# def create_figure(current_feature_name, bins):
#
#     fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
#     years = ['2015', '2016', '2017']
#
#     data = {'fruits': fruits,
#             '2015': [2, 1, 4, 3, 2, 4],
#             '2016': [5, 3, 3, 2, 4, 6],
#             '2017': [3, 2, 4, 4, 5, 3]}
#
#     # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
#     x = [(fruit, year) for fruit in fruits for year in years]
#     counts = sum(zip(data['2015'], data['2016'], data['2017']), ())  # like an hstack
#
#     source = ColumnDataSource(data=dict(x=x, counts=counts))
#
#     p = figure(x_range=FactorRange(*x), plot_height=250, title="Fruit Counts by Year",
#                toolbar_location=None, tools="")
#
#     p.vbar(x='x', top='counts', width=0.9, source=source)
#
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.1
#     p.xaxis.major_label_orientation = 1
#     p.xgrid.grid_line_color = None
#     p.yaxis.axis_label = 'Count'
#     return p
#
#
# # Index page
# @app.route('/')
# def index():
#     # Determine the selected feature
#     current_feature_name = "fruits"
#
#     # Create the plot
#     plot = create_figure(current_feature_name, 10)
#
#     # Embed plot into HTML via Flask Render
#     script, div = components(plot)
#     return render_template("iris_index1.html", script=script, div=div,
#                            feature_names=feature_names, current_feature_name=current_feature_name)
#
#
# # With debug=True, Flask server will auto-reload
# # when there are code changes
# if __name__ == '__main__':
#     app.run(port=5000, debug=True, host="0.0.0.0")
#

# myapp.py

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