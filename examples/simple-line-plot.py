""" A simple line plot example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment
from pssgplot.lineplot import LinePlot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with PlotEnvironment():
    df = pd.DataFrame({
        "x": [0, 1, 2, 3, 4],
        "series_a": [0, 2, 1, 3, 4],
        "series_b": [1, 2.5, 2, 3.5, 4.5],
        "series_c": [0.5, 1.2, 0.8, 1.8, 2.2],
    })
    df_long = df.melt(id_vars="x", var_name="series", value_name="y")

    simple_line = LinePlot()
    simple_line.plot(
        data=df_long,
        x="x",
        y="y",
        hue="series",
        title="A simple line plot",
        markers=True,
        legend=True,
    )

    # Use .animate to save an animation of the plot
    simple_line.animate(by='column', save_dir='output')

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save('output/simple-line-plot.pdf', format='pdf')
