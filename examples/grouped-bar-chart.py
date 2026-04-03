""" A simple bar chart example """

from pathlib import Path

import pandas as pd

from pssgplot import PlotEnvironment, BarPlot

with PlotEnvironment(font_path=Path('../fonts/gillsans.ttf')):
    df = pd.DataFrame({
        "x": ["A", "A", "B", "B", "C", "C"],
        "y": [1.3, 2.4, 3.5, 4.6, 5.7, 6.8],
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
    simple_bars.animate(by='hue', save_dir=Path('output'))

    # use .show or .save to output the figure
    #simple_bars.show()
    simple_bars.save(Path('output/grouped-bar-chart.pdf'), format='pdf')
