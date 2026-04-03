""" A simple heatmap example """

from pathlib import Path

import pandas as pd

from pssgplot import PlotEnvironment, Heatmap

with PlotEnvironment(font_path=Path('../fonts/gillsans.ttf')):
    df = pd.DataFrame({
        "x": [0,1,2,3,
              0,1,2,3,
              0,1,2,3],
        "y": [0,0,0,0,
              1,1,1,1,
              2,2,2,2],
        "value": [0.8,0.5,0.3,0.1,
                  0.5,0.3,0.1,0.2,
                  1.2,1.05,1.6,2.1]
    })
    hm = Heatmap()
    hm.plot(
        data=df,
        row="y",
        col="x",
        value="value",
        title="Simple Heatmap",
        bounds=[0.25, 0.5, 0.9, 1.1, 1.5, 1.75],
        colors=["#d73027","#fc8d59","#fee090","#ffffbf","#e0f3f8","#91bfdb","#4575b4"],
        annot_fmt=lambda v: f"{v:.1f}" if v >= 1 else f"{v:.2f}",
        cbar_label="Speedup",
        cbar_extend="both"
    )

    # use .animate to save a row-by-row animation of the heatmap
    hm.animate(by='row', save_dir=Path('output'))

    # use .show or .save to output the figure
    # hm.show()
    hm.save(Path('output/simple-heatmap.pdf'), format='pdf')
