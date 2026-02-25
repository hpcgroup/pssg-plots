"""Use PlotEnvironment global settings with plain matplotlib."""

import os
import sys

sys.path.append(".")
sys.path.append("..")

from pssgplot import PlotEnvironment
from pssgplot.style import get_colors, get_hatches, get_linestyles, get_markers

import matplotlib.pyplot as plt

with PlotEnvironment():
    x = [0, 1, 2, 3, 4]
    y = [0, 2, 1, 3, 4]

    fig, ax = plt.subplots()
    ax.set_box_aspect(3 / 5)

    linestyles = get_linestyles()
    markers = get_markers()
    colors = get_colors()
    hatches = get_hatches()

    ax.plot(
        x,
        y,
        linestyle=linestyles[0],
        marker=markers[2],
        color=colors[0],
    )

    ax.set_title("Matplotlib with PSSG global settings")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    if not os.path.exists("output"):
        os.makedirs("output")

    fig.savefig("output/matplotlib-global-style.pdf", format="pdf")
