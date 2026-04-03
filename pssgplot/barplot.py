""" Wrapper function to plot a barplot.
"""
# std imports
from typing import Optional, Tuple
import os

# tpl imports
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import seaborn as sns

# local imports
from .plot import Plot
from .style import apply_axes_style, get_hatches


class BarPlot(Plot):

    def __init__(self):
        pass

    def plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hatch: bool = True,
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
        self.ax = sns.barplot(data=data, x=x, y=y, ax=ax, zorder=3, **kwargs)

        if title is not None:
            self.ax.set_title(title, fontsize=title_fontsize)

        if xlabel is not None:
            self.ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)

        if ylabel is not None:
            self.ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

        if logx is not None:
<<<<<<< Updated upstream
            self.ax.set_xscale('log', base=logx)
        
        if logy is not None:
            self.ax.set_yscale('log', base=logy)
        
=======
            self.ax.set_xscale('log', basex=logx)

        if logy is not None:
            self.ax.set_yscale('log', basey=logy)

>>>>>>> Stashed changes
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
                fmt='none',
                color='#606060',
                capsize=5,
                elinewidth=2,
                capthick=2
            )

        if legend:
            self.ax.legend(loc=legend_loc, bbox_to_anchor=legend_bbox, fontsize=legend_fontsize, ncol=legend_ncol, title=legend_title)


        apply_axes_style(self.ax)

        if labels is not None:
            for p in self.ax.patches:
                if p.get_width() <= 0:
                    continue
                self.ax.annotate(
                    label_fmt.format(p.get_height()),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center',
                    va='center',
                    xytext=(0, 10),
                    textcoords='offset points',
                    fontsize=label_fontsize
                )

        if hatch:
            hatches = get_hatches()

            if 'hue' in kwargs:
                n_groups = len(data[kwargs['hue']].unique())
                group_size = len(data[x].unique())
            else:
                n_groups = len(data[x].unique())
                group_size = 1

            for i, bar in enumerate(self.ax.patches):
                hatch_idx = (i // group_size) % len(hatches)
                bar.set_hatch(hatches[hatch_idx])
                bar.set_edgecolor('k')

            legend = self.ax.get_legend()
            if 'hue' in kwargs and legend is not None:
                for i, p in enumerate(legend.get_patches()):
                    p.set_hatch(hatches[i % n_groups % len(hatches)])
                    p.set_edgecolor('k')

        if tight_layout:
            self.fig.tight_layout()

        if legend_title is not None and self.ax.get_legend() is not None:
            self.ax.get_legend().set_title(legend_title)

        return self.ax

    def animate(self, by: str, save_dir: os.PathLike, left_to_right: bool = True, frame_format: str = 'pdf', **kwargs):
        """
        Animate the barplot. Produces a frame for each animation step. This is for creating plots where data
        is progressively added in for illustrative purposes.

        Args:
            by (str): Either 'column' or 'hue'. Animate in each entire group or each hue.
            left_to_right (bool): Animate from left to right.
        """
        if not self.ax or not self.fig:
            raise ValueError("Plot must be created before animating.")

        self.ax.set_visible(False)

        if by == 'column':
            frames = len(self.data[self.x].unique())
            group_size = 1
        elif by == 'hue' and 'hue' in self.kwargs:
            frames = len(self.data[self.kwargs['hue']].unique())
            group_size = len(self.data[self.x].unique())
        else:
            raise ValueError("Invalid value for 'by'. Must be 'column' or 'hue' with 'hue' in kwargs.")

        # check if save_dir exists; if not, create it; if it does, error if it's not empty
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #elif os.listdir(save_dir):
        #    raise ValueError(f"Directory {save_dir} is not empty.")

        # save each frame as frame_format; and also save a gif
        for i in range(frames):
            self.ax.set_visible(True)
            for j, bar in enumerate(self.ax.patches):
                if j+1 <= (i+1)*group_size:
                #if j <= i:
                    bar.set_visible(True)
                else:
                    bar.set_visible(False)
            self.fig.savefig(os.path.join(save_dir, f"frame_{i}.{frame_format}"), **kwargs)
