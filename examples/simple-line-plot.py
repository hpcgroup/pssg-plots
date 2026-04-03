""" A simple line plot example """

from pathlib import Path

import pandas as pd

from pssgplot import PlotEnvironment, LinePlot

with PlotEnvironment(font_path=Path('../fonts/gillsans.ttf')):
    df = pd.DataFrame({
        "x": [0, 1, 2, 3, 4],
        "y": [0, 2, 1, 3, 4],
    })

    simple_line = LinePlot()
    simple_line.plot(data=df, x="x", y="y", title="A simple line plot", markers=True)

    # Use .animate to save an animation of the plot
    simple_line.animate(by='column', save_dir=Path('output'))

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save(Path('output/simple-line-plot.pdf'), format='pdf')
