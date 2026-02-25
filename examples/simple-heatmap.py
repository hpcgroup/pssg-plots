""" A simple heatmap example """
import sys
sys.path.append('.')
sys.path.append('..')
from pssgplot import PlotEnvironment, Heatmap
import pandas as pd
import numpy as np

with PlotEnvironment(font_path='../fonts/gillsans.ttf'):
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
        row="x",
        col="y",
        value="value",
        title="Simple Heatmap",
        bounds=[0.25, 0.5, 0.9, 1.1, 1.5, 2.0],
        colors=["#BD0026", "#FD8D3C", "#C7E9B4", "#41B6C4", "#253494"],
        annot_fmt=lambda v: f"{v:.1f}" if v >= 1 else f"{v:.2f}",
        cbar_label="Speedup",
        cbar_ticks=[0.5, 0.75, 1, 2, 4, 8],
    )

    # use .animate to save a row-by-row animation of the heatmap
    hm.animate(by='row', save_dir='output')

    # use .show or .save to output the figure
    # hm.show()
    hm.save('output/simple-heatmap.pdf', format='pdf')
