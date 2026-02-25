""" A simple bar chart example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment, BarPlot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


with PlotEnvironment():
    df = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": [1, 2, 3, 4],
    })

    simple_bars = BarPlot()
    simple_bars.plot(data=df, x="x", y="y", title="A simple bar chart")

    # use .animate to save an animation of the plot
    simple_bars.animate(by='column', save_dir='output')

    # use .show or .save to output the figure
    #simple_bars.show()
    simple_bars.save('output/simple-bar-chart.pdf', format='pdf')
