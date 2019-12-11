
from plotnine import *
from plotnine.data import mpg, txhousing

import subprocess as sp


class TestGraphViz:
    def __init__(self):
        pass

    def make_bar_graph(self, df, x, fill=None, target_filename=None, height=8, width=20):
        """
        Creates a simple plot for test purpose.

        :param x: The column name for X axis in the plot.
        :param target_filename: The target filepath to save the generated visualization image
        :param height: Height of the image for saving
        :param width: Width of the image for saving
        :return: None, saves the image
        """

        list_aes = ["x=x"]
        if(fill != None):
            list_aes.append("fill='"+fill+"'")


        resulted_aes = "aes("
        for anAes in list_aes:
            resulted_aes += anAes + ","
        resulted_aes += ")"

        print(resulted_aes)

        e = "(ggplot(df) + geom_bar("+  resulted_aes +") + theme_minimal()).save(filename=target_filename, height=height, width=width)"
        exec(e)





if __name__ == '__main__':
    tv = TestGraphViz()

    print(mpg.head())
    tv.make_bar_graph(df=mpg, x='cyl',  fill="fl", target_filename='../webapp/static/vizAI_plots/bar_graph_only_x1.png')
    tv.make_bar_graph(df=mpg, x='cty', fill="fl", target_filename='../webapp/static/vizAI_plots/bar_graph_only_x2.png')

    print(txhousing.head())
    tv.make_bar_graph(df=txhousing, x='month', fill='city', target_filename='/home/golammostaeen/Documents/My Projects/vizAI/vizAI/webapp/static/images/sampleChart.png')