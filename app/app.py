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