"""
The Bokeh applet to demonstrate the relatinship of news and BTC price
"""

import logging
logging.basicConfig(level=logging.DEBUG)

### bokeh import
from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm
### others
import numpy as np
import pandas as pd
import os
from datetime import datetime
input_folder = "data"

class SlidersApp(HBox):
    """The main app, where parameters and controllers are defined."""

    extra_generated_classes = [["SlidersApp", "SlidersApp", "HBox"]]

    inputs = Instance(VBoxForm)
    text = Instance(TextInput)
    threshold = Instance(Slider)
    plot = Instance(Plot)
    source = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        """One-time creation of app's objects.

        This function is called once, and is responsible for
        creating all objects (plots, datasources, etc)
        """
        ## create the obj of the app
        obj = cls()
        obj.source = ColumnDataSource(data=dict(x=[], y=[]))
        obj.text = TextInput(
            title="Title", name='title', value='BTC chart with news tag'
        )
        obj.threshold = Slider(
            title="Threshold", name='threshold',
            value=0.0, start=-1.0, end=1.0, step=0.1
        )
        toolset = "crosshair,pan,reset,resize,save,wheel_zoom"

        ## fixed time index limit (epoch)
        start_time = (datetime.strptime("1/1/12 16:30", "%d/%m/%y %H:%M") - datetime(1970,1,1)).total_seconds()*1000
        end_time = (datetime.strptime("1/5/15 16:30", "%d/%m/%y %H:%M") - datetime(1970,1,1)).total_seconds()*1000
        ## Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=600,
                      plot_width=1100,
                      tools=toolset,
                      title=obj.text.value,
                      # title="BTC chart with news",
                      x_axis_type="datetime",
                      x_range=[start_time, end_time],
                      y_range=[0, 1300]
        )
        plot.below[0].formatter.formats = dict(years=['%Y'], months=['%b %Y'], days=['%d %b %Y'])
        ## read the BTC price data
        raw_price = pd.read_csv(os.path.join(input_folder, "price.csv"), names=['time', 'price'], 
                           index_col='time', parse_dates=[0], 
                           date_parser=lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S"))
        raw_price['time_index'] = raw_price.index
        raw_price.drop_duplicates(subset='time_index', take_last=True, inplace=True)
        del raw_price['time_index']
        ## downsample to 12h data
        price_data = pd.DataFrame(raw_price.resample('12h', how='ohlc').ix[:, 3])
        price_data.columns = ['price']
        ## the price line plot
        plot.line(
            price_data.index, price_data['price'],
            # color='#A6CEE3',
            legend='BTC Price'
        )
        ## the news tag plot
        plot.circle('x', 'y', 
                    source=obj.source,
                    legend="News", 
                    size=8,
                    color = "red",
                    line_alpha = 0.8
        )
        obj.plot = plot
        obj.update_data()
        obj.inputs = VBoxForm(
            children=[
                obj.text, obj.threshold
            ]
        )
        obj.children.append(obj.inputs)
        obj.children.append(obj.plot)
        return obj

    def setup_events(self):
        """Attaches the on_change event to the value property of the widget.

        The callback is set to the input_change method of this app.
        """
        super(SlidersApp, self).setup_events()
        if not self.text:
            return
        # Text box event registration
        self.text.on_change('value', self, 'input_change')
        # Slider event registration
        getattr(self, "threshold").on_change('value', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        """Executes whenever the input form changes.

        It is responsible for updating the plot, or anything else you want.

        Args:
            obj : the object that changed
            attrname : the attr that changed
            old : old value of attr
            new : new value of attr
        """
        self.update_data()
        self.plot.title = self.text.value

    def update_data(self):
        """Called each time that any watched property changes.

        This updates the sin wave data with the most recent values of the
        sliders. This is stored as two numpy arrays in a dict into the app's
        data source property.
        """
        ## read data based on the threshold
        news_price = pd.read_csv(os.path.join(input_folder, "interpolated_alchemy_nyt_bitcoin.csv"), 
                                header=True, names=['time', 'price', 'headline', 'score'],
                                index_col=0, parse_dates=[0], 
                                date_parser=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))          
        x = news_price[news_price['score']>self.threshold.value].index
        y = news_price[news_price['score']>self.threshold.value].loc[:, 'price']
        logging.debug(
            "Threshold: %f" % self.threshold.value
        )
        ## plug back to source of the obj
        self.source.data = dict(x=x, y=y)

# The following code adds a "/bokeh/sliders/" url to the bokeh-server. This
# URL will render this sine wave sliders app. If you don't want to serve this
# applet from a Bokeh server (for instance if you are embedding in a separate
# Flask application), then just remove this block of code.
@bokeh_app.route("/bokeh/sliders/")
@object_page("sin")
def make_sliders():
    app = SlidersApp.create()
    return app
