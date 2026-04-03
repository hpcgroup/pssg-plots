""" A simple bar chart example """

from pathlib import Path

import pandas as pd

from pssgplot import PlotEnvironment, BarPlot

with PlotEnvironment(font_path=Path("../fonts/gillsans.ttf")):
    df = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": [1, 2, 3, 4],
    })

    simple_bars = BarPlot()
    simple_bars.plot(data=df, x="x", y="y", title="A simple bar chart")

    # use .animate to save an animation of the plot
    simple_bars.animate(by='column', save_dir=Path('output'))

    # use .show or .save to output the figure
    #simple_bars.show()
    simple_bars.save(Path('output/simple-bar-chart.pdf'), format='pdf')
