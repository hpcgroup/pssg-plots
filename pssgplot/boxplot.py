"""Wrapper function to plot a boxplot."""

# std imports
from typing import Optional, Tuple
import os

# tpl imports
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns

# local imports
from pssgplot import Plot


class BoxPlot(Plot):
    def __init__(self):
        pass

    def plot(  # type: ignore[override]
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hatch: bool = True,
        hatches: Optional[list[str]] = None,
        title: Optional[str] = None,
        title_fontsize: Optional[int] = None,
        xlabel: Optional[str] = None,
        xlabel_fontsize: Optional[int] = None,
        ylabel: Optional[str] = None,
        ylabel_fontsize: Optional[int] = None,
        logx: Optional[int] = None,
        logy: Optional[int] = None,
        xlim: Optional[Tuple[Optional[float], Optional[float]]] = None,
        ylim: Optional[Tuple[Optional[float], Optional[float]]] = None,
        error: Optional[str] = None,
        labels: Optional[str] = None,
        label_fontsize: Optional[int] = None,
        label_fmt: str = "{:.1f}",
        ax: Optional[Axes] = None,
        figsize: Tuple[float, float] = (5, 3),
        tight_layout: bool = True,
        legend: bool = False,
        legend_title: Optional[str] = None,
        legend_loc: Optional[str] = None,
        legend_bbox: Optional[Tuple[float, float]] = None,
        legend_fontsize: Optional[int] = None,
        legend_ncol: Optional[int] = None,
        **kwargs,
    ) -> Axes:
        self.data = data
        self.x = x
        self.y = y
        self.kwargs = kwargs

        self.fig = plt.figure(figsize=figsize)
        self.ax = sns.boxplot(data=data, x=x, y=y, ax=ax, zorder=3, **kwargs)

        if title is not None:
            self.ax.set_title(title, fontsize=title_fontsize)

        if xlabel is not None:
            self.ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)

        if ylabel is not None:
            self.ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

        if logx is not None:
            self.ax.set_xscale("log", basex=logx)

        if logy is not None:
            self.ax.set_yscale("log", basey=logy)

        if xlim is not None:
            self.ax.set_xlim(xlim)

        if ylim is not None:
            self.ax.set_ylim(ylim)

        if error is not None:
            if error not in data.columns:
                raise ValueError(f"Column {error} not in data.")
            self.ax.errorbar(
                x=data[x],
                y=data[y],
                yerr=data[error],
                fmt="none",
                color="#606060",
                capsize=5,
                elinewidth=2,
                capthick=2,
            )

        if legend:
            legend_kwargs = dict(
                loc=legend_loc,
                bbox_to_anchor=legend_bbox,
                fontsize=legend_fontsize,
                title=legend_title,
            )
            if legend_ncol is not None:
                legend_kwargs["ncol"] = legend_ncol
            self.ax.legend(**legend_kwargs)

        self.ax.yaxis.grid(linestyle="dashed", zorder=0)
        self.ax.spines["left"].set_color("#606060")
        self.ax.spines["bottom"].set_color("#606060")

        if labels is not None:
            for p in self.ax.patches:
                if p.get_width() <= 0:
                    continue
                self.ax.annotate(
                    label_fmt.format(p.get_height()),
                    (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center",
                    va="center",
                    xytext=(0, 10),
                    textcoords="offset points",
                    fontsize=label_fontsize,
                )

        if hatch:
            hatches = hatches or [
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

            if "hue" in kwargs:
                n_groups = len(data[kwargs["hue"]].unique())
                group_size = len(data[x].unique())
            else:
                n_groups = len(data[x].unique())
                group_size = 1

            for i, bar in enumerate(self.ax.patches):
                bar.set_hatch(hatches[i // group_size])
                bar.set_edgecolor("k")

            if "hue" in kwargs:
                for i, p in enumerate(self.ax.get_legend().get_patches()):
                    p.set_hatch(hatches[i % n_groups])
                    p.set_edgecolor("k")

        if tight_layout:
            self.fig.tight_layout()

        if legend_title is not None:
            self.ax.get_legend().set_title(legend_title)

        return self.ax

    def _build_box_elements(self):
        """
        Build a list of (patch, [lines]) tuples, one per box, by associating each
        PathPatch with the Line2D objects that share its center x-position.

        Seaborn draws patches in hue-major order: [x0_h0, x1_h0, ..., x0_h1, x1_h1, ...]
        Lines follow the same hue-major order, with a variable number of lines per box
        (whisker lo/hi, cap lo/hi, median, plus zero-or-more flier points as one Line2D).

        We match lines to patches by center x, grouping consecutive runs of lines that
        share the same center x (or have no points, which inherit the previous center).
        """
        import numpy as np

        # Only PathPatch objects are actual box bodies; Rectangle entries are legend proxies
        box_patches = [p for p in self.ax.patches if type(p).__name__ == "PathPatch"]

        def patch_center_x(p):
            verts = p.get_path().vertices
            return float(np.mean(verts[:, 0]))

        patch_centers = [patch_center_x(p) for p in box_patches]

        # Group lines by their center x, matching to the nearest patch center.
        # Lines with no data points (empty flier lines) are assigned to the preceding group.
        box_lines: list[list] = [[] for _ in box_patches]

        current_group = None  # index into box_patches
        for line in self.ax.lines:
            xd = line.get_xdata()
            if len(xd) == 0:
                # Empty flier line — belongs to the same box as the previous line
                if current_group is not None:
                    box_lines[current_group].append(line)
                continue
            cx = float(np.mean(xd))
            # Find the closest patch center
            closest = int(np.argmin([abs(cx - pc) for pc in patch_centers]))
            current_group = closest
            box_lines[closest].append(line)

        return list(zip(box_patches, box_lines))

    def animate(  # type: ignore[override]
        self,
        by: str,
        save_dir: os.PathLike,
        left_to_right: bool = True,
        frame_format: str = "pdf",
        **kwargs,
    ):
        """
        Animate the boxplot. Produces a frame for each animation step. This is for creating plots
        where data is progressively added in for illustrative purposes.

        For by='column': each frame reveals one additional x-group (all hues for that group).
        For by='hue': each frame reveals one additional hue value across all x-groups.

        Seaborn draws boxes in hue-major order: [x0_h0, x1_h0, ..., x0_h1, x1_h1, ...].
        This method builds a (x_idx, h_idx) → box mapping using patch center x-positions
        so that frames are revealed in the correct left-to-right, hue-by-hue order.

        Args:
            by (str): Either 'column' or 'hue'. Animate by each x-group or by each hue.
            left_to_right (bool): Animate from left to right (currently always True).
            frame_format (str): File format for saved frames (e.g. 'pdf', 'png').
        """
        import numpy as np

        if not (hasattr(self, "ax") and hasattr(self, "fig") and self.ax and self.fig):
            raise ValueError("Plot must be created before animating.")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        x_groups = list(self.data[self.x].unique())
        n_x = len(x_groups)

        has_hue = "hue" in self.kwargs
        if has_hue:
            hue_col = self.kwargs["hue"]
            hue_groups = list(self.data[hue_col].unique())
            n_hue = len(hue_groups)
        else:
            n_hue = 1

        # Associate each box (patch + its lines) with (x_idx, h_idx) using center x.
        # Patches are in hue-major order: first n_x entries are hue 0, next n_x are hue 1, etc.
        # Within each hue block, patches are ordered left-to-right by x position.
        box_elements = self._build_box_elements()  # list of (patch, [lines]), hue-major order

        # Sort patch centers to determine x_idx rank (left-to-right position)
        patch_centers = []
        for patch, _ in box_elements:
            verts = patch.get_path().vertices
            patch_centers.append(float(np.mean(verts[:, 0])))

        # Within each hue block of n_x patches, rank by center_x to get x_idx
        # Hue-major layout: block h contains indices [h*n_x .. (h+1)*n_x - 1]
        box_map: dict[tuple[int, int], int] = {}  # (x_idx, h_idx) -> index in box_elements
        for h_idx in range(n_hue):
            block = list(range(h_idx * n_x, (h_idx + 1) * n_x))
            # Sort block indices by their patch center_x to assign x_idx rank
            sorted_block = sorted(block, key=lambda i: patch_centers[i])
            for x_idx, elem_idx in enumerate(sorted_block):
                box_map[(x_idx, h_idx)] = elem_idx

        def set_box_visible(elem_idx: int, visible: bool):
            patch, lines = box_elements[elem_idx]
            patch.set_visible(visible)
            for line in lines:
                line.set_visible(visible)

        # Hide all boxes initially
        for i in range(len(box_elements)):
            set_box_visible(i, False)

        if by == "column":
            for frame in range(n_x):
                for x_idx in range(frame + 1):
                    for h_idx in range(n_hue):
                        set_box_visible(box_map[(x_idx, h_idx)], True)
                self.fig.savefig(os.path.join(save_dir, f"frame_{frame}.{frame_format}"), **kwargs)

        elif by == "hue":
            if not has_hue:
                raise ValueError("'by=hue' requires 'hue' to be specified in the plot kwargs.")
            for frame in range(n_hue):
                for h_idx in range(frame + 1):
                    for x_idx in range(n_x):
                        set_box_visible(box_map[(x_idx, h_idx)], True)
                self.fig.savefig(os.path.join(save_dir, f"frame_{frame}.{frame_format}"), **kwargs)

        else:
            raise ValueError(
                "Invalid value for 'by'. Must be 'column' or 'hue' (with hue in plot kwargs)."
            )
