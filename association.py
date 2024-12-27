import numpy as np

import matplotlib.pyplot as plt

from pandas import DataFrame


def association_matrix(df:DataFrame, method:str ='pearson', figsize=(15, 15)):
  """
  Creates a matrix visualization to explore relationships between pairs of columns in a DataFrame.
  
  The function generates a grid of subplots where:
  - The diagonal cells contain histograms for the individual columns.
  - The lower triangular cells display scatter plots with a regression line for pairs of columns.
  - The upper triangular cells show correlation coefficients scaled by their magnitude.
  
  Parameters:
  ----------
  df : pandas.DataFrame
      The input DataFrame containing the data to visualize. All columns must be numeric.
  method : str, optional 
      The correlation method to use for calculating pandas.DataFrame.corr() correlation coefficients. Can be 'pearson' or 'spearman'.
  figsize : tuple, optional 
    figsize parameter for the Matplotlib figure.
  
  Returns:
  -------
  fig : matplotlib.figure.Figure
      The Matplotlib figure object for the generated association matrix.
  ax : numpy.ndarray
      A 2D array of Axes objects corresponding to the subplots.
  
  Notes:
  -----
  - Correlation coefficients are rounded to two decimal places and displayed in the upper triangular cells.
  - The font size of the correlation coefficients is dynamically scaled based on their magnitude.
  - Scatter plots in the lower triangular cells include regression lines.
  - Tick positions and labels alternate based on cell position for better readability.
  - Histogram bins are fixed at 10, and densities are normalized.
  
  Examples:
  --------
  >>> import pandas as pd
  >>> import numpy as np
  >>> df = pd.DataFrame({
  ...     'A': np.random.rand(100),
  ...     'B': np.random.rand(100),
  ...     'C': np.random.rand(100)
  ... })
  >>> fig, ax = association_matrix(df)
  >>> plt.show()
  """

  columns = df.columns

  d = df.corr(method=method).to_numpy().round(2)

  fig, axis = plt.subplots(len(columns), len(columns), figsize=figsize)
  
  plt.subplots_adjust(left=.01, right=.99, top=.99, bottom=.01, wspace=.03, hspace=.03)

  for i, r in enumerate(axis):
    for j, ax in enumerate(r):


      v = df[[columns[i], columns[j]]]
  
      bbox = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
      ax_width, ax_height = bbox.width * ax.figure.dpi, bbox.height * ax.figure.dpi  
      s = (sum([ax_width, ax_height])/2)


      if j>i:
        ax.scatter(v[columns[j]], v[columns[i]], s=s/100, alpha=0)
        ax.text(.5, .5, d[(j, i)], ha='center', va='center', fontsize=(s/4)*(abs(d[(i, j)])), transform=ax.transAxes)

      elif j==i:
        ax.hist(v.iloc[:, 0].values, bins=10, density=True)
        ax.text(.5, .75, df.columns[i], ha='center', va='center', fontsize=(s/8)*(abs(d[(i, j)])), transform=ax.transAxes, 
                bbox=dict(facecolor='white', alpha=.5, boxstyle='round,pad=.5'))


      else:
        x, y = v[columns[j]], v[columns[i]]
        ax.scatter(x, y, s=s/100)

        coefficients = np.polyfit(x, y, 1)
        slope, intercept = coefficients

        x_line = np.linspace(min(x), max(x), 100)
        y_line = slope * x_line + intercept

        ax.plot(x_line, y_line, color='black', label=f'y = {slope:.2f}x + {intercept:.2f}')


      if i==0:
        if j%2==0:
          ax.set_xticks([])

        else:
          ax.xaxis.set_ticks_position('top')
          ax.xaxis.tick_top()
          ax.xaxis.set_label_position('top')
          ax.tick_params(axis='x', labelrotation=45)

      elif i==len(columns)-1:
        if j%2==1:
          ax.set_xticks([])

        else:
          ax.xaxis.set_ticks_position('bottom')
          ax.xaxis.tick_bottom()
          ax.xaxis.set_label_position('bottom')
          ax.tick_params(axis='x', labelrotation=45)

      else:
        ax.set_xticks([])

      if j==0:
        if i%2==0:
          ax.set_yticks([])

        else:
          ax.yaxis.set_ticks_position('left')
          ax.yaxis.tick_left()
          ax.yaxis.set_label_position('left')

      elif j==len(columns)-1:
        if i%2==1:
          ax.set_yticks([])

        else:
          ax.yaxis.set_ticks_position('right')
          ax.yaxis.tick_right()
          ax.yaxis.set_label_position('right')

        
      else:
        ax.set_yticks([])

  return fig, ax


