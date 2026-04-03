# Plot Scripts

## Overview

A lightweight Python plotting library for creating plots in the PSSG style.

## Simple Bar Chart Demo

A quick demo of plotting a simple bar chart:

```python
from pssgplot import PlotEnvironment, BarPlot
import pandas as pd

with PlotEnvironment():
    df = pd.DataFrame({
        "x": ["A", "B", "C", "D"],
        "y": [1, 2, 3, 4],
    })

    chart = BarPlot()
    chart.plot(data=df, x="x", y="y", title="A simple bar chart")

    # animate bar-by-bar or group-by-group to use in slides
    chart.animate(by='column', save_dir='output')
    
    chart.save('output/simple-bar-chart.png')
```

## Installing and Setup

Setting up with _uv_ is straightforward:

```bash
uv venv
source .venv/bin/activate

uv pip install -e pssg-plots/

uv run plotting-script.py
```

You can also just use vanilla pip and virtualenvs if you'd like.

## Use Global PSSG Style with Matplotlib

You can use `PlotEnvironment` without pssgplots functionalities such as `BarPlot` and `LinePlot`, and still get PSSG global styling.

If you need axis-level styling on demand, `pssgplot.apply_axes_style(ax)` is also available.

## Examples

For more details and demos, check out the example files:
- [Simple Bar Chart](examples/simple-bar-chart.py)
- [Grouped Bar Chart](examples/grouped-bar-chart.py)
- [Simple Line Plot](examples/simple-line-plot.py)
- [Matplotlib Global Style Simple Line Plot](examples/simple-line-plot-matplotlib.py)
