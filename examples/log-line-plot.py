"""A simple log-log line plot example"""

from pathlib import Path

import pandas as pd

from pssgplot import PlotEnvironment, LinePlot

with PlotEnvironment(font_path=Path("../fonts/gillsans.ttf")):
    df = pd.DataFrame(
        {
            "x": [1, 100, 2200, 3050, 40800],
            "y": [1, 200, 1000, 3000, 40000],
        }
    )

    simple_line = LinePlot()
    simple_line.plot(
        data=df, x="x", y="y", logx=10, logy=10, title="A log-log line plot", markers=True
    )

    # Use .animate to save an animation of the plot
    simple_line.animate(by="column", save_dir=Path("output"))

    # Use .show or .save to output the figure
    # simple_line.show()
    simple_line.save(Path("output/log-line-plot.pdf"), format="pdf")
