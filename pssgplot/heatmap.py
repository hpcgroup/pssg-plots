from typing import Optional, Tuple
import os
from matplotlib.axes import Axes
import pandas as pd
import seaborn as sns
from pssgplot import Plot

""" Wrapper function to plot a line plot.
"""
# std imports

# tpl imports
import matplotlib.pyplot as plt


class HeatMap(Plot):

    def __init__(self):
        pass

    def plot(
        self,
        df: pd.DataFrame,
        title: Optional[str] = None,
        title_fontsize: Optional[int] = None,
        xlabel: Optional[str] = None,
        xlabel_fontsize: Optional[int] = None,
        ylabel: Optional[str] = None,
        ylabel_fontsize: Optional[int] = None,
        figsize: tuple = (12, 8),
        tight_layout: bool = False,
        xtick_rotation: int = 0,
        ytick_rotation: int = 0,
        **kwargs
    ) -> Axes:
        """Plot a heatmap"""
        plt.figure(figsize=figsize)
        ax = sns.heatmap(data=df, **kwargs)

        if title:
            ax.set_title(title, fontsize=title_fontsize)

        if xlabel:
            ax.set_xlabel(xlabel, fontsize=xlabel_fontsize)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=ylabel_fontsize)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=xtick_rotation)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=ytick_rotation)

        if tight_layout:
            plt.tight_layout()

        return ax

    def animate(
        self,
        by: str,
        save_dir: os.PathLike,
        left_to_right: bool = True,
        frame_format: str = "pdf",
        **kwargs
    ):
        pass
