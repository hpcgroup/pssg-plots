"""Use PlotEnvironment global settings with plain matplotlib."""

import os
import sys

sys.path.append(".")
sys.path.append("..")

from pssgplot import PlotEnvironment
from pssgplot.style import get_colors, get_hatches, get_linestyles, get_markers, setup_local

import matplotlib.pyplot as plt

with PlotEnvironment():
    x = [0, 1, 2, 3, 4]
    y = [0, 2, 1, 3, 4]

    ax = setup_local()
    ax.plot(
        x,
        y,
    )

    ax.set_title("Matplotlib with PSSG global settings")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.tight_layout()

    if not os.path.exists("output"):
        os.makedirs("output")

    plt.savefig("output/matplotlib-global-style.pdf", format="pdf")
