import os

import pandas as pd
import numpy as np

from flask import Flask, render_template

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, CDSView, GroupFilter
from bokeh.models.widgets import Select
# The resources are the JS and CSS scripts needed to load the plots
from bokeh.resources import INLINE

from src.base import get_file, get_paths

app = Flask(__name__)

DEFAULT_PLOT_DICT = {"linewidth": 3
                     ,"marker": {"size": 8, "alpha": 1}
                     ,"ticks": {"fontsize": "16pt"}}


def get_source(path=None):

    if not path:
        paths = get_paths()
        path = paths.get("data").get("processed")

    filename = get_file(path, extension=".csv", latest=True)
    filename = os.path.join(path, filename)

    data = pd.read_csv(filename, index_col=0, header=[0, 1])
    data.index = pd.to_datetime(data.index)

    data.loc[:, ("y", "Close")] = data.loc[:, ("QBE.AX", "Close")]
    data.loc[:, ("y", "EWM")] = data.loc[:, ("QBE.AX", "EWM")]
    data.loc[:, ("y", "Trade")] = data.loc[:, ("QBE.AX", "Trade")]
    source = ColumnDataSource(data)

    return data, source


def make_figure(source, shares):
    """
    Generates the plot and select objects

    :param source: data source [bokeh.models.sources.ColumnDataSource]
    :param shares: share prices to be plotted [list]
    :return: plot, select
    """

    """
    1. Definitions
    """

    # Plot keyarguments definitions
    linewidth = DEFAULT_PLOT_DICT.get("linewidth")

    # Hover object [bokeh.models.HoverTool]

    # N.B.: The first argument in the tuples of tooltips must have the same
    # name as those defined in the dict of source
    # src: https://stackoverflow.com/questions/54316623/how-to-get-the-axis-values-on-the-hovertool-bokeh
    hover = HoverTool(
        tooltips=[("Date", "@Date{%F}"),
                  ("Price", "@y_Close"),
                  ("EWM", "@y_EWM"),
                  ("Trade", "@y_Trade")],
        formatters={"Date": "datetime"},
        mode='mouse'
    )

    # Plot object [bokeh.plotting.figure]
    plot = figure(plot_width=1500, plot_height=750, title='Close Price',
                  x_axis_label='Date [Days]', x_axis_type='datetime',
                  y_axis_label='Price', tools=[hover, 'box_select', 'box_zoom',
                                               'pan', 'reset', 'save'])

    """
    2. Add Plot Elements
    """

    # 2.1. Price line plots
    # Note that the _Close is necessary to read the double-header dataframe
    plot.line(x="Date", y="y_Close", line_width=linewidth, color="blue", legend="Price",
              alpha=0.5, line_dash="solid", muted_alpha=0, source=source)

    plot.line(x="Date", y="y_EWM", line_width=linewidth, color="red", legend="EWM",
              alpha=0.5, line_dash="solid", muted_alpha=0, source=source)

    # 2.2. Filter source data for trading points
    buy = CDSView(source=source, filters=[GroupFilter(column_name='y_Trade', group='Buy')])

    # Plot circles for buy / sell points
    plot.circle(x="Date", y="y_Close", size=8, color="blue", alpha=1, source=source,
                fill_color="white", legend="Buy", muted_alpha=0, view=buy)

    sell = CDSView(source=source, filters=[GroupFilter(column_name='y_Trade', group='Sell')])

    plot.circle(x="Date", y="y_Close", size=8, color="red", alpha=1, source=source,
                fill_color="white", legend="Sell", muted_alpha=0, view=sell)

    """
    3. Define Plot Dynamic Elements
    """

    # 3.1. Instantiate drop-down menu with shares
    select = Select(title="Share Code:", value="QBE.AX", options=shares)

    # 3.2. Define JS callback to update plot
    callback = CustomJS(args={'source': source}, code="""
                    // print the selectd value of the select widget - 
                    // this is printed in the browser console.
                    // cb_obj is the callback object, in this case the select 
                    // widget. cb_obj.value is the selected value.
                    console.log(' changed selected option', cb_obj.value);

                    // create a new variable for the data of the column data source
                    // this is linked to the plot
                    var data = source.data;

                    // allocate the selected column to the field for the y values
                    // Note that the _Close is necessary to read the double-header dataframe
                    data['y_Close'] = data[cb_obj.value + "_Close"];
                    data['y_EWM'] = data[cb_obj.value + "_EWM"];
                    data['y_Trade'] = data[cb_obj.value + "_Trade"];

                    // register the change - this is required to process the change in 
                    // the y values
                    source.change.emit();
                    """)

    # 3.3. Add callback to drop-down menu
    select.callback = callback

    return plot, select


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

@app.route("/")
def index():
    greetings = 'Welcome to Bokeh'

    data, source = get_source()

    shares = [column[0] for column in data.columns.values.squeeze() if column[0] != "y"]
    shares = sorted(list(set(shares)))
    plot, select = make_figure(source, shares)
    plot = format_figure(plot)

    script, div = components({"plot": plot, "select": select})

    return render_template('index.html', resources=INLINE.render(),
                           greetings=greetings, script=script, div=div)

""""
An MWE
"""
from bokeh.io import show
from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource, CustomJS

@app.route("/mwe")
def mwe():

    df = pd.DataFrame()
    df['x'] = np.random.randint(1, 1000, 1000)
    df['y'] = np.random.randint(1, 1000, 1000)
    df['val1'] = np.random.randint(1, 1000, 1000)
    df['val2'] = np.random.randint(1, 1000, 1000)
    df['val3'] = np.random.randint(1, 1000, 1000)

    from bokeh.plotting import figure
    from bokeh.models import LinearColorMapper
    from bokeh.palettes import RdYlBu11 as palette

    p = figure(x_range=(0, 1000), y_range=(0, 1000))
    source = ColumnDataSource(df)
    source_orig = ColumnDataSource(df)
    color_mapper = LinearColorMapper(palette=palette)
    p.rect('x', 'y', source=source, width=4, height=4,
           color={'field': 'val1', 'transform': color_mapper})

    from bokeh.models.widgets import Select
    select = Select(title="Option:", value="val1", options=["val1", "val2", "val3"])

    callback = CustomJS(args={'source': source}, code="""
            // print the selectd value of the select widget - 
            // this is printed in the browser console.
            // cb_obj is the callback object, in this case the select 
            // widget. cb_obj.value is the selected value.
            console.log(' changed selected option', cb_obj.value);

            // create a new variable for the data of the column data source
            // this is linked to the plot
            var data = source.data;

            // allocate the selected column to the field for the y values
            data['y'] = data[cb_obj.value];

            // register the change - this is required to process the change in 
            // the y values
            source.change.emit();
    """)

    # Add the callback to the select widget.
    # This executes each time the selected option changes
    select.callback = callback
    script, div = components({"plot": p, "select":select})

    return render_template('mwe.html', resources=INLINE.render(), script=script, div=div, greetings="MWE")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")

"""
References:

src: https://stackoverflow.com/questions/35298029/embedding-bokeh-plot-and-datatable-in-flask
src: https://stackoverflow.com/questions/55301063/how-to-embed-a-datatable-widget-in-a-python-flask-web-app
"""
