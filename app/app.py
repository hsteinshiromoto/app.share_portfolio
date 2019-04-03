from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange

app = Flask(__name__)

# Load the Iris Data Set
feature_names = ["fruits", "2015", "2016", "2017"]


# Create the main plot
def create_figure(current_feature_name, bins):

    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']

    data = {'fruits': fruits,
            '2015': [2, 1, 4, 3, 2, 4],
            '2016': [5, 3, 3, 2, 4, 6],
            '2017': [3, 2, 4, 4, 5, 3]}

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x = [(fruit, year) for fruit in fruits for year in years]
    counts = sum(zip(data['2015'], data['2016'], data['2017']), ())  # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), plot_height=250, title="Fruit Counts by Year",
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.yaxis.axis_label = 'Count'
    return p


# Index page
@app.route('/')
def index():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Sepal Length"

    # Create the plot
    plot = create_figure(current_feature_name, 10)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("iris_index1.html", script=script, div=div,
                           feature_names=feature_names, current_feature_name=current_feature_name)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True, host="0.0.0.0")

