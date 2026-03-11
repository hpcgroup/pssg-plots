""" Wrapper class to plot a heatmap. """
# std imports
from typing import Callable, List, Optional, Tuple, Union
import os

# tpl imports
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.axes import Axes
from matplotlib.colors import Colormap, Normalize
import numpy as np
import pandas as pd
import seaborn as sns

# local imports
from pssgplot import Plot


class Heatmap(Plot):

    def __init__(self):
        self.fig = None
        self.ax = None
        self.data = None

    @staticmethod
    def _pivot_data(
        data: pd.DataFrame,
        row: Optional[str],
        col: Optional[str],
        value: Optional[str],
    ) -> pd.DataFrame:
        specified = [x for x in (row, col, value) if x is not None]
        if len(specified) == 0:
            return data
        if len(specified) == 3:
            return data.pivot(index=row, columns=col, values=value)
        raise ValueError(
            "row, col, and value must all be provided together, or all omitted "
            "(to pass a pre-pivoted DataFrame)."
        )

    @staticmethod
    def _build_norm(
        bounds: Optional[List[float]],
        colors: Optional[List[str]],
        cmap: Union[str, Colormap, None],
        vmin: Optional[float],
        vmax: Optional[float],
        extend: Union[str, None] = "neither",
    ) -> Tuple[Union[str, Colormap], Optional[Normalize]]:
        if bounds is not None:
            if colors is None:
                raise ValueError(
                    "When 'bounds' is provided, 'colors' must also be provided and not None."
                )

            listed = mcolors.ListedColormap(colors)
            norm = mcolors.BoundaryNorm(
                bounds,
                ncolors=len(colors),
                clip=extend is None,
                extend=extend,
            )
            return listed, norm
        elif vmin is not None or vmax is not None:
            norm = Normalize(vmin=vmin, vmax=vmax)
            return cmap, norm
        else:
            return cmap, None

    @staticmethod
    def _build_annot_matrix(
        pivot: pd.DataFrame,
        annot_fmt: Union[str, Callable[[float], str]],
    ) -> np.ndarray:
        result = np.empty(pivot.shape, dtype=object)
        for i in range(pivot.shape[0]):
            for j in range(pivot.shape[1]):
                v = pivot.iloc[i, j]
                if pd.isna(v):
                    result[i, j] = ""
                elif callable(annot_fmt):
                    result[i, j] = annot_fmt(v)
                else:
                    result[i, j] = annot_fmt.format(v)
        return result

    def plot(
        self,
        data: pd.DataFrame,
        row: Optional[str] = None,
        col: Optional[str] = None,
        value: Optional[str] = None,
        title: Optional[str] = None,
        title_fontsize: Optional[int] = None,
        xlabel: Optional[str] = None,
        xlabel_fontsize: Optional[int] = None,
        ylabel: Optional[str] = None,
        ylabel_fontsize: Optional[int] = None,
        figsize: Tuple[float, float] = (6, 4.5),
        ax: Optional[Axes] = None,
        tight_layout: bool = True,
        cmap: Union[str, Colormap, None] = "YlOrRd",
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        bounds: Optional[List[float]] = None,
        colors: Optional[List[str]] = None,
        annot: bool = True,
        annot_fmt: Union[str, Callable[[float], str], None] = None,
        annot_fontsize: Optional[int] = None,
        cbar: bool = True,
        cbar_label: Optional[str] = None,
        cbar_ticks: Optional[List[float]] = None,
        cbar_ticklabels: Optional[List[str]] = None,
        cbar_extend: Optional[str] = "neither",
        linewidths: float = 0.5,
        linecolor: str = "white",
        **kwargs,
    ) -> Axes:
        self.data = self._pivot_data(data, row, col, value)

        if ax is None:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        else:
            self.ax = ax
            self.fig = ax.get_figure()

        resolved_cmap, norm = self._build_norm(bounds, colors, cmap, vmin, vmax, cbar_extend)

        if annot and annot_fmt is not None:
            annot_data = self._build_annot_matrix(self.data, annot_fmt)
            fmt = ""
        else:
            annot_data = annot
            fmt = ".2g"

        cbar_kws = {}
        if cbar_ticks is not None:
            cbar_kws["ticks"] = cbar_ticks

        heatmap_kwargs = dict(
            cmap=resolved_cmap,
            norm=norm,
            annot=annot_data,
            fmt=fmt,
            annot_kws={"fontsize": annot_fontsize} if annot_fontsize is not None else {},
            linewidths=linewidths,
            linecolor=linecolor,
            cbar=cbar,
            cbar_kws=cbar_kws,
        )
        if norm is None:
            heatmap_kwargs["vmin"] = vmin
            heatmap_kwargs["vmax"] = vmax

        sns.heatmap(self.data, ax=self.ax, **heatmap_kwargs, **kwargs)

        if cbar and (cbar_label is not None or cbar_ticklabels is not None):
            colorbar = self.ax.collections[0].colorbar
            if cbar_label is not None:
                colorbar.set_label(cbar_label)
            if cbar_ticklabels is not None:
                colorbar.set_ticklabels(cbar_ticklabels)

        if title is not None:
            self.ax.set_title(title, fontsize=title_fontsize)
        if xlabel is not None:
            self.ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)
        if ylabel is not None:
            self.ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

        self.ax.spines['left'].set_color('#606060')
        self.ax.spines['bottom'].set_color('#606060')

        if tight_layout:
            self.fig.tight_layout()

        return self.ax

    def animate(
        self,
        by: str,
        save_dir: os.PathLike,
        frame_format: str = 'pdf',
        **kwargs,
    ):
        """
        Animate the heatmap by progressively revealing rows or columns.

        Produces one frame per step and saves each to save_dir.

        Args:
            by (str): Either 'row' or 'col'.
            save_dir (PathLike): Directory to save frames into.
            frame_format (str): File format for frames (e.g. 'pdf', 'png').
        """
        if self.ax is None or self.fig is None:
            raise ValueError("plot() must be called before animate().")
        if by not in ('row', 'col'):
            raise ValueError("'by' must be 'row' or 'col'.")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        original = self.data.values.astype(float)
        n_frames = original.shape[0] if by == 'row' else original.shape[1]
        mesh = self.ax.collections[0]

        for frame in range(n_frames):
            masked = np.full_like(original, np.nan)
            if by == 'row':
                masked[:frame + 1, :] = original[:frame + 1, :]
            else:
                masked[:, :frame + 1] = original[:, :frame + 1]
            mesh.set_array(masked.ravel())
            self.fig.savefig(
                os.path.join(save_dir, f"frame_{frame}.{frame_format}"),
                **kwargs,
            )
