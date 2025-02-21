""" A simple bar chart example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment, BarPlot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


with PlotEnvironment(font_path='../fonts/gillsans.ttf'):
    df = pd.DataFrame({
        "x": ["A", "A", "B", "B", "C", "C"],
        "y": [1, 2, 3, 4, 5, 6],
        "category": ["foo", "bar", "foo", "bar", "foo", "bar"],
    })

    # use hue to group bars by a column
    simple_bars = BarPlot()
    simple_bars.plot(
        data=df, 
        x="x", 
        y="y", 
        hue="category",
        title="A simple bar chart"
    )
    
    # use .animate to save an animation of the plot
    # you can animate by group or individual column
    simple_bars.animate(by='hue', save_dir='output')

    # use .show or .save to output the figure
    #simple_bars.show()
    simple_bars.save('output/grouped-bar-chart.pdf', format='pdf')
