"""A simple box plot example"""

from pathlib import Path

import numpy as np
import pandas as pd

from pssgplot import PlotEnvironment, BoxPlot

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
    #simple_box.show()
    simple_box.save(Path("output/simple-box-plot.pdf"), format="pdf")
