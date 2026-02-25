"""Shared styling helpers for PSSG plots."""

import math
from typing import Iterable, List, Optional

from cycler import cycler
from matplotlib.axes import Axes


PSSG_COLORS = ["#D55E00", "#009E73", "#0072B2", "#CC79A7", "#643B9F", "#E03A3D"]

PSSG_LINESTYLES = [
    "solid",
    "dotted",
    "dashed",
    "dashdot",
    (0, (3, 5, 1, 5, 1, 5)),
    (0, (3, 10, 1, 10, 1, 10)),
]

PSSG_MARKERS = [
    "^",
    "s",
    "o",
    "d",
    "x",
    "P",
]

PSSG_HATCHES = [
    "x",
    "xxx",
    "\\\\",
    "||",
    "///",
    "+",
    "o",
    ".",
    "*",
    "-",
    "ooo",
    "+++",
    "...",
    "---",
    "xx",
    "++",
]


def get_colors() -> List[str]:
    return list(PSSG_COLORS)


def get_linestyles() -> List[object]:
    return list(PSSG_LINESTYLES)


def get_markers() -> List[str]:
    return list(PSSG_MARKERS)


def get_hatches() -> List[str]:
    return list(PSSG_HATCHES)


def make_prop_cycle(
    colors: Optional[Iterable[str]] = None,
    linestyles: Optional[Iterable[object]] = None,
    markers: Optional[Iterable[str]] = None,
):
    """Build a style cycle combining color, linestyle, and marker."""
    color_values = list(colors) if colors is not None else get_colors()
    linestyle_values = list(linestyles) if linestyles is not None else get_linestyles()
    marker_values = list(markers) if markers is not None else get_markers()

    cycle_len = min(len(color_values), len(linestyle_values), len(marker_values))
    if cycle_len == 0:
        raise ValueError("colors, linestyles, and markers must be non-empty.")

    return (
        cycler(color=color_values[:cycle_len])
        + cycler(linestyle=linestyle_values[:cycle_len])
        + cycler(marker=marker_values[:cycle_len])
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
