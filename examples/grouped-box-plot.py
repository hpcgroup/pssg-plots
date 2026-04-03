"""A grouped box plot example demonstrating hue-wise animation."""

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
    rng = np.random.default_rng(42)
    groups = ["A", "B", "C", "D"]
    hues = ["Control", "Treatment 1", "Treatment 2"]

    records: list[pd.DataFrame] = []
    for i, group in enumerate(groups):
        for j, hue in enumerate(hues):
            values = rng.normal(loc=i + j * 0.5, scale=1.0 + j * 0.3, size=80)
            records.append(pd.DataFrame({"value": values, "group": group, "condition": hue}))
    df = pd.concat(records, ignore_index=True)

    grouped_box = BoxPlot()
    grouped_box.plot(
        data=df,
        x="group",
        y="value",
        hue="condition",
        title="Grouped box plot",
        xlabel="Group",
        ylabel="Value",
        legend=True,
        legend_title="Condition",
        legend_loc="upper left",
        figsize=(7, 4),
    )

    os.makedirs("output", exist_ok=True)
    grouped_box.save("output/grouped-box-plot.pdf", format="pdf")

    # Animate by column: each frame adds one x-group (with all conditions)
    grouped_box.animate(
        by="column",
        save_dir=Path("output/grouped-box-plot-anim-column"),
        frame_format="pdf",
    )

    # Re-plot so patches are fresh, then animate by hue
    grouped_box2 = BoxPlot()
    grouped_box2.plot(
        data=df,
        x="group",
        y="value",
        hue="condition",
        title="Grouped box plot",
        xlabel="Group",
        ylabel="Value",
        legend=True,
        legend_title="Condition",
        legend_loc="upper left",
        figsize=(7, 4),
    )

    grouped_box2.animate(
        by="hue",
        save_dir=Path("output/grouped-box-plot-anim-hue"),
        frame_format="pdf",
    )
