""" Wrapper function to plot a barplot.
"""
# std imports
from typing import Optional, Tuple, Union
import os

# tpl imports
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import pandas as pd
import seaborn as sns

# local imports
from pssgplot import Plot, HATCHES

class BarPlot(Plot):

    def __init__(self):
        pass

    def plot(  # type: ignore[override]
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hatch: bool = True,
        linewidth: float = 0,
        edgecolor: str = 'black',
        gap: float = 0.03,
        title: Optional[str] = None,
        title_fontsize: Optional[int] = None,
        xlabel: Optional[str] = None,
        xlabel_fontsize: Optional[int] = None,
        ylabel: Optional[str] = None,
        ylabel_fontsize: Optional[int] = None,
        logx: Optional[int] = None,
        logy: Optional[int] = None,
        xlim: Union[Tuple[float, float], float, None] = None,
        ylim: Union[Tuple[float, float], float, None] = None,
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
        self.ax = sns.barplot(
            data=data,
            x=x,
            y=y,
            ax=ax,
            zorder=3,
            linewidth=linewidth,
            edgecolor=edgecolor,
            gap=gap,
            **kwargs
        )

        if title is not None:
            self.ax.set_title(title, fontsize=title_fontsize)

        if xlabel is not None:
            self.ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)

        if ylabel is not None:
            self.ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

        if logx is not None:
            self.ax.set_xscale('log', base=logx)

        if logy is not None:
            self.ax.set_yscale('log', base=logy)

        if xlim is not None:
            self.ax.set_xlim(xlim)

        if ylim is not None:
            self.ax.set_ylim(ylim)
        else:
            ylim = self.ax.get_ylim()
            yticks = self.ax.get_yticks()
            tick_step = yticks[1] - yticks[0]
            tick_list = self.ax.get_yticks()
            if yticks[-1] < ylim[1]:
                tick_list = np.append(tick_list, yticks[-1] + tick_step)
            if yticks[0] > ylim[0]:
                tick_list = np.insert(tick_list, 0, yticks[0] - tick_step)
            self.ax.set_yticks(tick_list)

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
        leg_obj = self.ax.get_legend()


        self.ax.yaxis.grid(linestyle='dotted', zorder=0, clip_on=False)
        self.ax.spines['left'].set_color('#606060')
        self.ax.spines['bottom'].set_color('#606060')

        self.ax.tick_params(axis='both', which='both', direction='in', color='#606060')

        if labels is not None:
            for p in self.ax.patches:
                if not isinstance(p, plt.Rectangle):
                    continue
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
            hatches = HATCHES

            if 'hue' in kwargs:
                n_groups = len(data[kwargs['hue']].unique())
                group_size = len(data[x].unique())
            else:
                n_groups = len(data[x].unique())
                group_size = 1

            for i, bar in enumerate(self.ax.patches):
                bar.set_hatch(hatches[i // group_size])
                bar.set_edgecolor(edgecolor)

            if 'hue' in kwargs and leg_obj is not None:
                for i, p in enumerate(leg_obj.get_patches()):
                    p.set_hatch(hatches[i % n_groups])
                    p.set_edgecolor(edgecolor)

        if tight_layout:
            self.fig.tight_layout()

        if legend_title is not None and leg_obj is not None:
            leg_obj.set_title(legend_title)

        return self.ax

    def animate(self, by: str, save_dir: os.PathLike, left_to_right: bool = True, frame_format: str = 'pdf', **kwargs):  # type: ignore[override]
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
