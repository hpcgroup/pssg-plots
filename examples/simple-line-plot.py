""" A simple line plot example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment
from pssgplot.lineplot import LinePlot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with PlotEnvironment(font_path='../fonts/gillsans.ttf'):
    df = pd.DataFrame({
       "x": [0, 1, 2, 3, 4] * 3,
       "y": [0, 2, 1, 3, 4,
             1, 3, 2, 4, 5,
             2, 4, 3, 5, 6],
       "line": ["A"] * 5 + ["B"] * 5 + ["C"] * 5
    })

    simple_line = LinePlot()
    simple_line.plot(
        data=df, x="x", y="y",
        hue="line",
        title="A simple line plot",
        markers=True,
        legend=True,
        legend_title="Line"
    )
    
    # Use .animate to save an animation of the plot
    simple_line.animate(by='column', save_dir='output')

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save('output/simple-line-plot.pdf', format='pdf')
