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

## Examples

For more details and demos, check out the example files:
- [Simple Bar Chart](examples/simple-bar-chart.py)
- [Grouped Bar Chart](examples/grouped-bar-chart.py)
- [Simple Line Plot](examples/simple-line-plot.py)