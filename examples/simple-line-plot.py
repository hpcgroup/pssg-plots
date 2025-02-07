""" A simple line plot example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment
from pssgplot.lineplot import LinePlot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with PlotEnvironment(font_path='fonts/gillsans.ttf'):
    df = pd.DataFrame({
        "x": [0, 1, 2, 3, 4],
        "y": [0, 2, 1, 3, 4],
    })

    simple_line = LinePlot()
    simple_line.plot(data=df, x="x", y="y", title="A simple line plot", markers=True)
    
    # Use .animate to save an animation of the plot
    simple_line.animate(by='column', save_dir='output')

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save('output/simple-line-plot.png')