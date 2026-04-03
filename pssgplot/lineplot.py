""" Wrapper function to plot a line plot.
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
from pssgplot import Plot, LINESTYLES, MARKERS

class LinePlot(Plot):

    def __init__(self):
        self._lines_data = None  # To store original line data for animation

    def plot(  # type: ignore[override]
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        markers: bool = True,
        markeredgewidth: float = 0,
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
        legend: bool = False,
        legend_title: Optional[str] = None,
        legend_loc: Optional[str] = None,
        legend_bbox: Optional[Tuple[float, float]] = None,
        legend_fontsize: Optional[int] = None,
        legend_ncol: Optional[int] = None,
        ax: Optional[Axes] = None,
        figsize: Tuple[float, float] = (5, 3),
        tight_layout: bool = True,
        **kwargs,
    ) -> Axes:

        self.data = data
        self.x = x
        self.y = y
        self.kwargs = kwargs

        self.fig = plt.figure(figsize=figsize)

        # Create a lineplot using seaborn
        if 'style' in kwargs:
            kwargs['dashes'] = LINESTYLES
            kwargs['markers'] = MARKERS
        else:
            kwargs['marker'] = 'o' if markers else None
        self.ax = sns.lineplot(
            data=data, x=x, y=y, ax=ax, markeredgewidth=markeredgewidth, **kwargs
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

        # Need to trim margins before adjusting ticks to avoid dropping ticks
        self.ax.margins(0)

        if xlim is not None:
            self.ax.set_xlim(xlim)
        else:
            xlim = self.ax.get_xlim()
            xticks = self.ax.get_xticks()
            tick_step = xticks[1] - xticks[0]
            tick_list = self.ax.get_xticks()
            if xticks[-1] < xlim[1]:
                tick_list = np.append(tick_list, xticks[-1] + tick_step)
            if xticks[0] > xlim[0]:
                tick_list = np.insert(tick_list, 0, xticks[0] - tick_step)
            self.ax.set_xticks(tick_list)

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
            # Plot error bars using matplotlib's errorbar. Assumes the error column provides y-error values.
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
        elif 'hue' in kwargs:
            sns.move_legend(self.ax, "upper left", reverse=True)
        leg_obj = self.ax.get_legend()

        self.ax.yaxis.grid(linestyle='dotted', zorder=0)
        self.ax.spines['left'].set_color('#606060')
        self.ax.spines['bottom'].set_color('#606060')

        self.ax.tick_params(axis='both', direction='in', color='#606060')

        if tight_layout:
            self.fig.tight_layout()

        if legend_title is not None and leg_obj is not None:
            leg_obj.set_title(legend_title)

        # Store original data from the lines for animation
        self._lines_data = []
        for line in self.ax.get_lines():
            # Copy the full data for each line
            xdata = np.array(line.get_xdata()).copy()
            ydata = np.array(line.get_ydata()).copy()
            self._lines_data.append((xdata, ydata))
        return self.ax

    def animate(self, by: str, save_dir: os.PathLike, left_to_right: bool = True, frame_format: str = 'pdf', **kwargs):  # type: ignore[override]
        """
        Animate the line plot. Produces a frame for each animation step.
        There are two animation modes:
            - by='column': progressively reveal data points along each line.
            - by='hue': progressively reveal entire lines (useful if multiple lines exist due to a hue grouping).

        Args:
            by (str): Either 'column' or 'hue'.
            left_to_right (bool): If True, reveal data in order of the x-axis.
            frame_format (str): Format for saving frames.
        """
        if not (hasattr(self, 'ax') and hasattr(self, 'fig') and self.ax and self.fig):
            raise ValueError("Plot must be created before animating.")
        if self._lines_data is None:
            raise ValueError("Original line data not stored; cannot animate.")

        # Ensure output directory exists and is empty
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #elif os.listdir(save_dir):
        #    raise ValueError(f"Directory {save_dir} is not empty.")

        if by == 'column':
            # Determine maximum number of data points among all lines
            num_frames = max(len(xdata) for xdata, _ in self._lines_data)
            # Animate by revealing more points along each line
            for frame in range(num_frames):
                for idx, line in enumerate(self.ax.get_lines()):
                    xdata, ydata = self._lines_data[idx]
                    n = min(frame + 1, len(xdata))
                    line.set_data(xdata[:n], ydata[:n])
                self.fig.savefig(os.path.join(save_dir, f"frame_{frame}.{frame_format}"), **kwargs)
        elif by == 'hue' and 'hue' in self.kwargs:
            # Animate by revealing one entire line at a time based on hue grouping.
            lines = self.ax.get_lines()
            total_lines = len(lines)
            # Initially hide all lines
            for line in lines:
                line.set_visible(False)
            for frame in range(total_lines):
                for idx, line in enumerate(lines):
                    if idx <= frame:
                        line.set_visible(True)
                    else:
                        line.set_visible(False)
                self.fig.savefig(os.path.join(save_dir, f"frame_{frame}.{frame_format}"), **kwargs)
        else:
            raise ValueError("Invalid value for 'by'. Must be 'column' or 'hue' with 'hue' in kwargs.")
