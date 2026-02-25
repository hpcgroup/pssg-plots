from typing import Optional, Tuple
import os
import math
import matplotlib as mpl
from matplotlib.markers import MarkerStyle
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
import pandas as pd
from pandas.api.types import is_numeric_dtype
import seaborn as sns
from pssgplot import Plot

""" Wrapper function to plot a line plot.
"""
# std imports

# tpl imports
import matplotlib.pyplot as plt

# local imports


class LinePlot(Plot):

    def __init__(self):
        self._lines_data = None  # To store original line data for animation

    def plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        markers: bool = True,
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
        self.ax = sns.lineplot(data=data, x=x, y=y, ax=ax, marker='o' if markers else None, **kwargs)

        if title is not None:
            self.ax.set_title(title, fontsize=title_fontsize)

        if xlabel is not None:
            self.ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)

        if ylabel is not None:
            self.ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

        if logx is not None:
            self.ax.set_xscale('log', basex=logx)

        if logy is not None:
            self.ax.set_yscale('log', basey=logy)

        if xlim is not None:
            self.ax.set_xlim(xlim)

        if ylim is not None:
            self.ax.set_ylim(ylim)

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

        legend_kwargs = None
        if legend:
            legend_kwargs = {}
            if legend_loc is not None:
                legend_kwargs["loc"] = legend_loc
            if legend_bbox is not None:
                legend_kwargs["bbox_to_anchor"] = legend_bbox
            if legend_fontsize is not None:
                legend_kwargs["fontsize"] = legend_fontsize
            if legend_ncol is not None:
                legend_kwargs["ncol"] = legend_ncol
            if legend_title is not None:
                legend_kwargs["title"] = legend_title

        tick_color = '#606060'
        tick_width = 0.8
        self.ax.tick_params(
            axis='both',
            which='both',
            direction='in',
            colors=tick_color,
            labelcolor=tick_color,
            width=tick_width,
            length=0,
        )
        self.ax.yaxis.grid(
            linestyle=(0, (0.5, 2.4)),
            color=tick_color,
            linewidth=tick_width,
            dash_capstyle='round',
            zorder=0,
        )
        for gridline in self.ax.get_ygridlines():
            gridline.set_clip_on(False)
        if not hasattr(self, "_custom_tick_lines"):
            self._custom_tick_lines = []
        for line in self._custom_tick_lines:
            line.remove()
        self._custom_tick_lines = []
        self.ax.spines['left'].set_color('#606060')
        self.ax.spines['bottom'].set_color('#606060')

        lines = self.ax.get_lines()
        data_lines = []
        proxy_lines = []
        for line in lines:
            try:
                xdata = line.get_xdata()
            except AttributeError:
                xdata = []
            if len(xdata) > 0:
                data_lines.append(line)
            else:
                proxy_lines.append(line)

        if len(data_lines) > 1:
            base_dash_patterns = [
                (4, 2.5),  # orange
                (6, 2, 1, 2, 1, 2),  # green
                (6, 2, 2, 2),  # blue
            ]
            base_markers = ['o', 'x', 's']
            extra_dash_pattern = (1, 1)
            extra_marker = '^'
            def _make_marker(marker_name):
                if marker_name == 'x':
                    return MarkerStyle(marker_name, capstyle='round', joinstyle='round')
                if marker_name == 's':
                    return MarkerStyle(marker_name, joinstyle='round')
                return marker_name
            styles_by_index = []
            styles_by_color = {}
            for idx, line in enumerate(data_lines):
                if idx < len(base_dash_patterns):
                    dash = base_dash_patterns[idx]
                    marker = base_markers[idx]
                else:
                    dash = extra_dash_pattern
                    marker = extra_marker
                    line.set_color('black')
                line.set_dashes(dash)
                line.set_dash_capstyle('round')
                if markers:
                    line.set_marker(_make_marker(marker))
                line.set_linewidth(1.4)
                styles_by_index.append((dash, marker))
                styles_by_color.setdefault(line.get_color(), (dash, marker))

            for idx, line in enumerate(proxy_lines):
                dash_marker = styles_by_color.get(line.get_color())
                if dash_marker is None and idx < len(styles_by_index):
                    dash_marker = styles_by_index[idx]
                if dash_marker is not None:
                    dash, marker = dash_marker
                    line.set_dashes(dash)
                    line.set_dash_capstyle('round')
                    if markers:
                        line.set_marker(_make_marker(marker))
                    line.set_linewidth(1.4)

        if markers:
            facecolor = self.ax.get_facecolor()
            for line in lines:
                marker_value = line.get_marker()
                if isinstance(marker_value, MarkerStyle):
                    marker_name = marker_value.get_marker()
                else:
                    marker_name = marker_value
                if marker_name not in (None, 'None', ''):
                    if marker_name == 'x':
                        line.set_markerfacecolor('none')
                    else:
                        line.set_markerfacecolor(facecolor)
                    line.set_markeredgecolor(line.get_color())
                    line.set_markeredgewidth(1.2)

        if legend_kwargs is not None:
            legend_kwargs.setdefault("handlelength", 3.2)
            self.ax.legend(**legend_kwargs)

        def _nice_num(value, round_to):
            if value == 0:
                return 1
            exponent = math.floor(math.log10(value))
            fraction = value / (10 ** exponent)
            if round_to:
                if fraction < 1.5:
                    nice_fraction = 1
                elif fraction < 3:
                    nice_fraction = 2
                elif fraction < 7:
                    nice_fraction = 5
                else:
                    nice_fraction = 10
            else:
                if fraction <= 1:
                    nice_fraction = 1
                elif fraction <= 2:
                    nice_fraction = 2
                elif fraction <= 5:
                    nice_fraction = 5
                else:
                    nice_fraction = 10
            return nice_fraction * (10 ** exponent)

        def _set_linear_limits(series, axis, set_lim):
            data_max = series.max()
            if pd.isna(data_max) or data_max <= 0:
                return
            desired_ticks = 6
            step = _nice_num(data_max / (desired_ticks - 1), True)
            upper = math.ceil(data_max / step) * step
            set_lim(0, upper)
            n = int(round(upper / step))
            ticks = [i * step for i in range(n + 1)]
            axis.set_ticks(ticks)

        if xlim is None and logx is None and is_numeric_dtype(data[x]):
            _set_linear_limits(data[x], self.ax.xaxis, self.ax.set_xlim)

        if ylim is None and logy is None and is_numeric_dtype(data[y]):
            _set_linear_limits(data[y], self.ax.yaxis, self.ax.set_ylim)

        if tight_layout:
            self.fig.tight_layout()

        fig = self.ax.figure
        fig.canvas.draw()
        bbox = self.ax.get_window_extent()
        xtick_len = mpl.rcParams['xtick.major.size']
        ytick_len = mpl.rcParams['ytick.major.size']
        xtick_len_ax = (xtick_len * fig.dpi / 72.0) / bbox.height
        ytick_len_ax = (ytick_len * fig.dpi / 72.0) / bbox.width
        x_offset = (tick_width * fig.dpi / 72.0) / bbox.height / 2.0
        y_offset = (tick_width * fig.dpi / 72.0) / bbox.width / 2.0

        for x_tick in self.ax.get_xticks():
            line = Line2D(
                [x_tick, x_tick],
                [x_offset, x_offset + xtick_len_ax],
                transform=self.ax.get_xaxis_transform(),
                color=tick_color,
                linewidth=tick_width,
                solid_capstyle='round',
                zorder=3,
                clip_on=False,
            )
            self.ax.add_line(line)
            self._custom_tick_lines.append(line)

        for y_tick in self.ax.get_yticks():
            line = Line2D(
                [y_offset, y_offset + ytick_len_ax],
                [y_tick, y_tick],
                transform=self.ax.get_yaxis_transform(),
                color=tick_color,
                linewidth=tick_width,
                solid_capstyle='round',
                zorder=3,
                clip_on=False,
            )
            self.ax.add_line(line)
            self._custom_tick_lines.append(line)

        if legend_title is not None and self.ax.get_legend():
            self.ax.get_legend().set_title(legend_title)

        # Store original data from the lines for animation
        self._lines_data = []
        for line in self.ax.get_lines():
            # Copy the full data for each line
            xdata = line.get_xdata().copy()
            ydata = line.get_ydata().copy()
            self._lines_data.append((xdata, ydata))
        return self.ax

    def animate(self, by: str, save_dir: os.PathLike, left_to_right: bool = True, frame_format: str = 'pdf', **kwargs):
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
