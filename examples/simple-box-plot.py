"""A simple box plot example"""

import sys
import os
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(".")
sys.path.append("..")
from pssgplot import PlotEnvironment
from pssgplot.boxplot import BoxPlot

with PlotEnvironment(font_path=Path("../fonts/gillsans.ttf")):
    df = pd.DataFrame(
        {
            "value": np.concatenate([np.random.normal(0, 1 + i, 100) for i in range(5)]),
            "group": np.concatenate([[name] * 100 for name in ["A", "B", "C", "D", "E"]]),
        }
    )

    simple_box = BoxPlot()
    simple_box.plot(data=df, x="group", y="value", title="A simple box plot")

    # Use .animate to save an animation of the plot
    simple_box.animate(
        by="column", save_dir=Path("output/simple-box-plot-anim"), frame_format="pdf"
    )

    # Use .show or .save to output the figure
    os.makedirs("output", exist_ok=True)
    simple_box.save("output/simple-box-plot.pdf", format="pdf")
