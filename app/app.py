import os

import pandas as pd
import numpy as np

from flask import Flask, render_template

from bokeh.plotting import figure
from bokeh.embed import components

from src.base import get_file, get_paths

app = Flask(__name__)

DEFAULT_PLOT_DICT = {"linewidth": 3}

def read_data(path=None):

    if not path:
        paths = get_paths()
        path = paths.get("data").get("processed")

    filename = get_file(path, extension=".csv", latest=True)
    filename = os.path.join(path, filename)

    data = pd.read_csv(filename, index_col=0, header=[0, 1])
    data.index = pd.to_datetime(data.index)

    return data


def make_figure(data, stock):

    linewidth = DEFAULT_PLOT_DICT.get("linewidth")

    plot = figure(plot_width=1500, plot_height = 750, title = 'Close Price',
           x_axis_label = 'Date [Days]', x_axis_type='datetime', y_axis_label='Price')

    x = data.index
    y = data.loc[x, (stock, "Close")]

    plot.line(x, y, line_width=linewidth, color="blue", legend="Price",
                    alpha=0.5, line_dash="solid", muted_alpha=0)

    return plot


@app.route('/')
def greet():
    greetings = 'Hello World, I am BOKEH'
    data = read_data()
    plot = make_figure(data, "QBE.AX")
    script, div = components(plot)

    return render_template('index.html', greetings=greetings, script=script, div=div)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")