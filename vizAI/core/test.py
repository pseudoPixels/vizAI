
from plotnine import *
from plotnine.data import mpg


class Test:
    def __init__(self):
        pass

    def make_simple_plot(self,x='class', target_filename='../webapp/static/images/sampleChart.png', height=8, width=20):
        """
        Creates a simple plot for test purpose.

        :param x: The column name for X axis in the plot.
        :param target_filename: The target filepath to save the generated visualization image
        :param height: Height of the image for saving
        :param width: Width of the image for saving
        :return: None, saves the image
        """

        p = ggplot(mpg) + geom_bar(aes(x=x) ) + theme_minimal()
        p.save(filename=target_filename, height=height, width=width)
