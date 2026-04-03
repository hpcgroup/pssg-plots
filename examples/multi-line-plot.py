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
        "y": [0, 2, 1, 3, 4, 1, 3, 4, 5, 6, 0, 3, 3, 7, 8],
        "hue": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B", "C", "C", "C", "C", "C"],
    })

    simple_line = LinePlot()
    simple_line.plot(data=df, x="x", y="y", hue="hue", style="hue", title="A multi-line plot", markers=True)

    # Use .animate to save an animation of the plot
    simple_line.animate(by='hue', save_dir=Path('output'))

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save('output/multi-line-plot.pdf', format='pdf')
