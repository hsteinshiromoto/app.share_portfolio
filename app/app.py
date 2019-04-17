import os

import pandas as pd
import numpy as np

from flask import Flask, render_template

from bokeh.plotting import figure
from bokeh.embed import components

from src.base import get_file, get_paths

app = Flask(__name__)

def read_data(path=None):

    if not path:
        paths = get_paths()
        path = paths.get("data").get("processed")

    filename = get_file(path, extension=".csv", latest=True)
    filename = os.path.join(path, filename)

    data = pd.read_csv(filename, index_col=0, header=[0, 1])

    return data


def make_figure():
    plot = figure(width=750, height=450, title='United States Import/Exports')

    y = np.random.rand(100, 1).squeeze()
    x = np.array(range(len(y))).squeeze()

    plot.line(x, y, color='#A6CEE3', legend='Exports')

    return plot


@app.route('/')
def greet():
    greetings = 'Hello World, I am BOKEH'
    data = read_data()
    plot = make_figure()
    script, div = components(plot)

    return render_template('index.html', greetings=greetings, script=script, div=div)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")