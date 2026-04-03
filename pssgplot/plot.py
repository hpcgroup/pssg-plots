""" Base class for all plots. """
# std imports
from os import PathLike
from abc import ABC, abstractmethod

# tpl imports
import matplotlib.pyplot as plt


class Plot(ABC):

    @abstractmethod
    def plot(self):
        pass

    def show(self, **kwargs):
        plt.show(**kwargs)

    def save(self, path: PathLike, **kwargs):
        plt.savefig(path, **kwargs)

    @abstractmethod
    def animate(self):
        pass
