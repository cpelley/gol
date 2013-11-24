import curses
import matplotlib.pyplot as plt
import numpy as np
import numpy.lib.stride_tricks as stride
import time


def window_views(grid, xsize=3, ysize=3, xstep=1, ystep=1):
    """
    Generate view ndarray of the grid.

    Kwargs:

    * xsize (int):
        Window dim-0 size.
    * ysize (int):
        Window dim-1 size.
    * xstep (int):
        Window dim-0 step, corresponding to window center.
    * ystep(int):
        Window dim-1 step, corresponding to window center.

    Returns:
        Numpy ndarray which represents a view of the grid.

    .. note::

    This function is not currently in use.

    """
    strides = (grid.strides[0] * xstep,
               grid.strides[1] * ystep,
               grid.strides[0],
               grid.strides[1])
    window = ((grid.shape[0] - 2) // xstep, (grid.shape[1] - 2) // ystep,
              xsize, ysize)
    all_windows = stride.as_strided(grid, window, strides)
    return all_windows


def plot(grid):
    plt.figure()
    plt.pcolor(grid)
    plt.show()


def main():
    size = (7, 7)
    grid = np.random.randint(0, 2, size)
    grid.astype(np.uint8)
    grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = 0

    views = window_views(grid)

    mask = np.array([[True, True, True],
                     [True, False, True],
                     [True, True, True]])

    for i in xrange(10000):
        print i
        neighbours = views[..., mask].sum(2)
        views[..., 1, 1] = (views[..., 1, 1] & ~(neighbours > 3) &
                            ~(neighbours < 2) | neighbours == 3)


if __name__ == '__main__':
    main()
