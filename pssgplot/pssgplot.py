""" Defines PSSG plot environment.
"""
# std imports
from os import PathLike
from pathlib import Path
from typing import List, Optional, Union
import warnings

# tpl imports
from matplotlib.font_manager import FontProperties, fontManager
import matplotlib as mpl
import seaborn as sns


INTERACTIVE_BACKENDS = ['tkagg', 'qt5agg', 'qt6agg']
PALETTE = ['#D55E00', '#0072B2', '#009E73', '#000000', '#800080', '#CC79A7', '#E69F00', '#56B4E9']
HATCHES = ['xxx', '//', '|||', 'OO', '++', '**', '\\\\\\']
MARKERS = ['o', '^', 's', 'D', 'X', 'p']
LINESTYLES = [(),                 # solid
              (1, 2),             # dotted
              (4, 2),             # dashed
              (3, 1, 1, 1),       # densely dashdotted
              (3, 1, 1, 1, 1, 1), # densely dashdotdotted
              (5, 1),             # densely dashed
              (7, 2, 1, 2)]       # dashdot

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

        font_name = self._resolve_font(font_name, font_path)

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
        self._color_palette = color_palette or sns.color_palette(PALETTE, len(PALETTE))
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
                'hatch.linewidth': 0.5,
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

    def _resolve_font(self, font_name: Optional[str], font_path: Optional[str]) -> str:
        """ Resolves the font to use for plotting.
            If neither font_name nor font_path is specified, look for the Gill Sans MT or Gill Sans font packaged with this library.
                If it is not found, look for a systems Gill Sans or Gill Sans MT font. If it is still not found, print a warning and use the default font.
            If font_name is specified, use it.
            If font_path is specified, load the font from the path and use it.
            If both are specified, raise an error.
        """
        if font_name is not None and font_path is not None:
            raise ValueError("Only one of font_name and font_path may be specified.")

        if font_path is not None:
            return self._load_font(font_path)

        if font_name is not None:
            return font_name

        # Use bundled Gill Sans font if available
        bundled_font_path = Path(__file__).parent.parent / "fonts" / "gillsans.ttf"
        if bundled_font_path.exists():
            return self._load_font(bundled_font_path)

        # Look for system Gill Sans or Gill Sans MT fonts
        available_fonts = [f.name for f in fontManager.ttflist]
        for font_candidate in ['Gill Sans MT', 'Gill Sans', 'GillSans']:
            if font_candidate in available_fonts:
                return font_candidate

        # Fall back to default font with warning
        warnings.warn(
            "Gill Sans font not found. Using default sans-serif font. "
            "For best results, install Gill Sans or specify a custom font.",
            UserWarning
        )
        return "sans-serif"
