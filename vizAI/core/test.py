import pandas as pd
import numpy as np

from plotnine import *
from plotnine.data import mpg

p = ggplot(mpg) + geom_bar(aes(x='class', fill='drv') ) + theme_minimal()
p.save(filename='../webapp/static/images/sampleChart.png', height=8, width=20)
