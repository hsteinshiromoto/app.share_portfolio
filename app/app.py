import os

import pandas as pd
import numpy as np

from flask import Flask, render_template

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource

from src.base import get_file, get_paths

app = Flask(__name__)

DEFAULT_PLOT_DICT = {"linewidth": 3
                     ,"marker": {"size": 8, "alpha": 1}
                     ,"ticks": {"fontsize": "16pt"}}

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

    price_source = ColumnDataSource(dict(
        dates=data.index,
        price=data.loc[:, (stock, "Close")],
        ewm=data.loc[:, (stock, "EWM")]
    ))

    # N.B.: The first argument in the tuples of tooltips must have the same
    # name as those defined in the dict of source
    # src: https://stackoverflow.com/questions/54316623/how-to-get-the-axis-values-on-the-hovertool-bokeh
    hover = HoverTool(
                    tooltips=[("Date", "@dates{%F}"),
                              ("Price", "@price")],
                    formatters={"dates": "datetime"},
                    mode='mouse'
                    )

    linewidth = DEFAULT_PLOT_DICT.get("linewidth")

    plot = figure(plot_width=1500, plot_height = 750, title = 'Close Price',
                  x_axis_label = 'Date [Days]', x_axis_type='datetime',
                  y_axis_label='Price', tools=[hover, 'box_select', 'box_zoom',
                                               'pan', 'reset', 'save'] )

    plot.line(x="dates", y="price", line_width=linewidth, color="blue", legend="Price",
                    alpha=0.5, line_dash="solid", muted_alpha=0, source=price_source)

    plot.line(x="dates", y="ewm", line_width=linewidth, color="red", legend="EWM",
              alpha=0.5, line_dash="solid", muted_alpha=0, source=price_source)

    for trade_type in ["Buy", "Sell"]:

        mask_trade = data.loc[:, (stock, "Trade")] == trade_type
        x_trade = data.loc[mask_trade, (stock, "Close")].index
        y_trade = data.loc[mask_trade, (stock, "Close")].values

        if trade_type == "Buy":
            color = "blue"

        else:
            color = "red"

        plot.circle(x_trade, y_trade, size=8, color=color, alpha=1,
                    fill_color="white", legend=trade_type, muted_alpha=0)



    return plot


def format_figure(plot):

    ticks_fontsize = DEFAULT_PLOT_DICT.get("ticks").get("fontsize")

    plot.outline_line_color = None

    plot.xgrid.visible = False
    plot.ygrid.visible = False

    plot.xgrid.visible = False
    plot.ygrid.visible = False

    plot.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    plot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    plot.xaxis.axis_line_width = 0
    plot.xaxis.axis_line_color = None

    plot.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    plot.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks

    plot.yaxis.axis_line_width = 0
    plot.yaxis.axis_line_color = None

    # Change ticks label font size
    # src: https://stackoverflow.com/questions/47220491/how-do-you-change-ticks-label-sizes-using-pythons-bokeh
    plot.xaxis.major_label_text_font_size = ticks_fontsize
    plot.xaxis.axis_label_text_font_size = ticks_fontsize

    plot.yaxis.major_label_text_font_size = ticks_fontsize
    plot.yaxis.axis_label_text_font_size = ticks_fontsize

    # Click in the legend to remove the corresponding line
    plot.legend.click_policy = "mute"
    plot.legend.label_text_font_size = ticks_fontsize

    return plot

@app.route('/')
def greet():
    greetings = 'Hello World, I am BOKEH'
    data = read_data()
    plot = make_figure(data, "QBE.AX")
    plot = format_figure(plot)
    script, div = components(plot)

    return render_template('index.html', greetings=greetings, script=script, div=div)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")