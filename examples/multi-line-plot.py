""" A simple line plot example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment
from pssgplot.lineplot import LinePlot
import pandas as pd
from pathlib import Path

with PlotEnvironment(font_path=Path('../fonts/gillsans.ttf')):
    df = pd.DataFrame({
        "x": [0, 1, 2, 3, 4] * 3,
        "y": [0, 2.3, 1.5, 3.6, 4.7] + [1.3, 3.4, 4.5, 5.6, 6.7] + [0.3, 3.4, 3.5, 7.6, 8.7],
        "hue": ["C"] * 5 + ["B"] * 5 + ["A"] * 5,
    })

    simple_line = LinePlot()
    simple_line.plot(data=df, x="x", y="y", hue="hue", style="hue", title="A multi-line plot", markers=True)

    # Use .animate to save an animation of the plot
    simple_line.animate(by='hue', save_dir=Path('output'))

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save('output/multi-line-plot.pdf', format='pdf')
