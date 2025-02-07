

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt


class Plot(ABC):

    @abstractmethod
    def plot(self):
        pass

    def show(self, **kwargs):
        plt.show(**kwargs)

    def save(self, path: str, **kwargs):
        plt.savefig(path, **kwargs)

    @abstractmethod
    def animate(self):
        pass
