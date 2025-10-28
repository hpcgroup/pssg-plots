""" Defines PSSG plot environment.
"""
# std imports
from os import PathLike
from typing import List, Optional, Union

# tpl imports
from matplotlib.font_manager import FontProperties, fontManager
import matplotlib as mpl
import seaborn as sns


INTERACTIVE_BACKENDS = ['tkagg', 'qt5agg', 'qt6agg']


def get_colors():
    return ["#FD8A8A", "#A8D1D1", "#9EA1D4", "#FFCBCB", "#DFEBEB", "#F1F7B5"]


def get_darker_colors():
    # Return darker tones of the colors in get_colors()
    return ["#E03A3D", "#0072B2", "#643B9F", "#D55E00", "#009E73", "#CC79A7"]


def get_alt_colors():
    return [
        "#D55E00",
        "#009E73",
        "#0072B2",
        "#CC79A7",
        "#000000",
        "#E03A3D",
        "#F0E442",
    ]



class PlotEnvironment:
    """ PSSG plot environment.
    """

    _font_name: Optional[str] = None
    _font_scale: float = 1.0
    _color_palette: Optional[Union[str, List[str]]] = None

    def __init__(
        self,
        font_name: Optional[str] = None,
        font_path: Optional[PathLike] = None,
        font_scale: float = 1.0,
        color_palette: Optional[Union[str, List[str]]] = None,
        interactive: bool = False,
        backend: Optional[str] = None,
    ):
        """ Initialize PSSG plot environment.

        Args:
        
            font_name (str, optional): Name of font to use. Defaults to None.
            font_path (PathLike, optional): Path to font to use. Defaults to None.
            font_scale (float, optional): Font scale. Defaults to 1.0.
            color_palette (Union[str, List[str]], optional): Color palette to use. Defaults to None.
            interactive (bool, optional): If True, uses matplotlib backend 'Agg', 'TkAgg', 'QtAgg' to enable interactive plots. Defaults to False.
            backend (str, optional): Name of backend to use. Defaults to None.

        Raises:
            
            ValueError: If neither font_name nor font_path is specified.
            ValueError: If font_scale is not positive.
            ValueError: If interactive is True, but Agg, TkAgg, Qt5Agg, or Qt6Agg are not available.
            ValueError: If both interactive and backend are specified.
        """
        if interactive and backend is not None:
            raise ValueError("interactive and backend cannot both be specified.")

        if font_name is not None and font_path is not None:
            raise ValueError("Only one of font_name and font_path may be specified.")
        
        if font_path is not None:
            font_name = self._load_font(font_path)

        if font_scale <= 0:
            raise ValueError("font_scale must be positive.")

        if interactive:
            available_backends = mpl.rcsetup.interactive_bk
            available_interactive_backends = list(set(available_backends).intersection(INTERACTIVE_BACKENDS))
            if len(available_interactive_backends) == 0:
                raise ValueError("No interactive backends available.")
            backend = available_interactive_backends[0]
            mpl.use(backend)
        elif backend is not None:
            mpl.use(backend)

        self._font_name = font_name or "sans-serif"
        self._font_scale = font_scale
        self._color_palette = color_palette or sns.color_palette(['#D55E00', '#009E73','#0072B2', '#CC79A7', '#643B9F', '#E03A3D'], 6)
        self._interactive = interactive


    def __enter__(self):
        """ Enter context.
        """
        self._previous_color_palette = sns.color_palette()
        self._sns_context = sns.plotting_context(
            font_scale=self._font_scale,
            context={
                'axes.spines.right': False,
                'axes.spines.top': False,
                'lines.linewidth': 2, 
                'lines.markersize': 8,
                'font.family': self._font_name,
            }
        )
        self._sns_context.__enter__()
        sns.set_palette(self._color_palette)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Exit context.
        """
        self._sns_context.__exit__(exc_type, exc_value, traceback)
        sns.set_palette(self._previous_color_palette)

    def _load_font(self, font_path: PathLike) -> str:
        """ load a font into matplotlib and return its name """
        fontManager.addfont(font_path)
        return FontProperties(fname=font_path).get_name()
