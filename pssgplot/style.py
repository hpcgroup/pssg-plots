"""Shared styling helpers for PSSG plots."""

import math
from typing import Iterable, List, Optional

from cycler import cycler
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

LINESTYLES_BY_NAME = {
     'solid':                 (0, ()),
     'loosely dotted':        (0, (1, 10)),
     'dotted':                (0, (1, 5)),
     'densely dotted':        (0, (1, 1)),

     'long dash with offset': (5, (10, 3)),
     'loosely dashed':        (0, (5, 10)),
     'dashed':                (0, (5, 5)),
     'densely dashed':        (0, (5, 1)),

     'loosely dashdotted':    (0, (3, 10, 1, 10)),
     'dashdotted':            (0, (3, 5, 1, 5)),
     'densely dashdotted':    (0, (3, 1, 1, 1)),

     'dashdotdotted':         (0, (3, 5, 1, 5, 1, 5)),
     'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
     'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))}


PSSG_COLORS = ["#D55E00", "#0072B2", "#009E73", "#000000", "#800080", "#CC79A7", "#E69F00", "#56B4E9"]
PSSG_BAR_COLORS = [c for c in PSSG_COLORS if c != "#000000"]

PSSG_LINESTYLE_NAMES = [
    "solid",
    "dotted",
    "dashed",
    "densely dashdotted",
    "densely dashdotdotted",
    "densely dashed",
    "dashdotted",
    "dashdotdotted",
]
PSSG_LINESTYLES = [LINESTYLES_BY_NAME[n] for n in PSSG_LINESTYLE_NAMES]

PSSG_MARKERS = [
    "o",
    "^",
    "s",
    "d",
    "X",
    "p",
    "*",
    "P",
]

PSSG_HATCHES = [
    "xxx",
    "//",
    "|||",
    "OO",
    "++",
    "**",
    "\\\\\\",
    "..",
    "---",
]


def get_colors(plot_type: Optional[str] = "line") -> List[str]:
    if plot_type == "bar":
        return list(PSSG_BAR_COLORS)
    else:
        return list(PSSG_COLORS)


def get_linestyles() -> List[object]:
    return list(PSSG_LINESTYLES)


def get_markers() -> List[str]:
    return list(PSSG_MARKERS)


def get_hatches() -> List[str]:
    return list(PSSG_HATCHES)


def make_prop_cycle(
    colors: Optional[Iterable[str]] = get_colors(),
    linestyles: Optional[Iterable[object]] = get_linestyles(),
    markers: Optional[Iterable[str]] = get_markers(),
):
    cycle_len = min(len(colors), len(linestyles), len(markers))
    if cycle_len == 0:
        raise ValueError("colors, linestyles, and markers must be non-empty.")

    return (
        cycler(color=colors[:cycle_len])
        + cycler(linestyle=linestyles[:cycle_len], marker=markers[:cycle_len])
    )


def apply_axes_style(
    ax: Axes,
    grid_linestyle: str = "dotted",
    grid_axis: str = "y",
    spine_color: str = "#606060",
) -> Axes:
    """Apply PSSG axis-level styling to an axes."""
    ax.grid(axis=grid_axis, linestyle=grid_linestyle)
    ax.spines["left"].set_color(spine_color)
    ax.spines["bottom"].set_color(spine_color)
    ax.set_axisbelow(True)
    return ax


# TODO: Review carefully. There might be some edge cases
# where this doesn't work perfectly.
def set_aspect_ratio(ax, ratio=3 / 5, logx=None, logy=None):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()

    if logx is not None:
        if x0 <= 0 or x1 <= 0:
            raise ValueError("x limits must be > 0 for logx")
        x0, x1 = math.log(x0, logx), math.log(x1, logx)

    if logy is not None:
        if y0 <= 0 or y1 <= 0:
            raise ValueError("y limits must be > 0 for logy")
        y0, y1 = math.log(y0, logy), math.log(y1, logy)

    dx, dy = abs(x1 - x0), abs(y1 - y0)
    if dy == 0:
        raise ValueError("y range is zero; cannot set aspect")
    ax.set_aspect((dx / dy) * ratio)

def setup_local(ax=None, grid=True, color="#606060",
                spines=['left', 'bottom'], aspect_ratio=3/5):
    if ax is None:
        plt.clf()
        ax = plt.gca()

    if grid:
        ax.yaxis.grid(linestyle='dotted', color=color)

    for s in spines:
        ax.spines[s].set_color("#606060")

    set_aspect_ratio(ax, aspect_ratio)
    ax.set_prop_cycle(make_prop_cycle())

    return ax
