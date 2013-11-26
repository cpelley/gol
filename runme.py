import curses
import matplotlib.pyplot as plt
import numpy as np
import numpy.lib.stride_tricks as stride
import time


def window_views(grid, xsize=3, ysize=3, xstep=1, ystep=1):
    """
    Generate view ndarray of the grid.

    Args:

    * grid (2darray)
        Grid on which to stride.

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

        Numpy ndarray which represents a views of the grid.

    """
    strides = (grid.strides[0] * xstep,
               grid.strides[1] * ystep,
               grid.strides[0],
               grid.strides[1])
    window = ((grid.shape[0] - 2) // xstep, (grid.shape[1] - 2) // ystep,
              xsize, ysize)
    all_windows = stride.as_strided(grid, window, strides)
    return all_windows


def mpl_plot(grid):
    """
    Simple predefined plotting using matplotlib.

    Args:

    * grid (2darray):
        Grid to plot.

    Returns:

        None

    """
    plt.gcf()
    plt.pcolor(grid)
    plt.show()


class Plot(object):
    """Abstract class for a GOL simulation plotting backend."""
    def __enter__(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def __exit__(self):
        raise NotImplementedError()


class CursePlot(Plot):
    """Curses context manager for fast plotting an ndarray."""
    def __init__(self, grid, window=None, fps=None):
        """
        Curses context manager for fast plotting an ndarray.

        Args:

        * grid (2darray):
            Grid to plot.

        Kwargs:

        * window (ndarray):
            ndarray view of the grid (see :func:`window_views`).
        * fps (int):
            ~ Numbers of frames per second.

        Returns:

            None

        """
        self.fps = fps
        if window:
            self.window = window
        else:
            self.window = curses.initscr()
        self.grid = grid

        # No echo of input characters
        curses.noecho()
        #curses.start_color()
        #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        #curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)

        # Visibility of cursor
        curses.curs_set(0)

    def __enter__(self):
        return self

    def update(self):
        """
        Update the curses window with the current content of our grid.

        """
        for ind, line in enumerate(self.grid):
            pout = ''.join(line.astype('|S1')).replace('0', ' ')
            self.window.addstr(ind, 0, pout)
        self.window.refresh()

        if self.fps:
            time.sleep(1. / self.fps)

    def __exit__(self):
        # Close curses.
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()


def game_of_life(size=(40, 140), plot_tool=CursePlot, iterations=1000):
    """
    Game of life simulation.

    Kwargs:

    * size (length 2 tuple):
        Grid size dimensions, expected in (size_y, size_x).
    * plot_tool (:class:`Plot` subclass):
        Plotting backend for plotting each GOL iteration.
    * iterations (int):
        Number of iterations for the simulation.

    Returns:

        None

    """
    # Adjust dimensions to suitable value
    size = [dim + (2 - diff) for dim, diff in
            zip(size, [ss % 3 for ss in size])]

    grid = np.random.randint(0, 2, size)
    grid.astype(np.uint8)
    grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = 0

    views = window_views(grid)

    mask = np.array([[True, True, True],
                     [True, False, True],
                     [True, True, True]])

    with plot_tool(grid) as plot:
        for i in xrange(iterations):
            neighbours = views[..., mask].sum(2)
            views[..., 1, 1] = (views[..., 1, 1] & ~(neighbours > 3) &
                                ~(neighbours < 2) | neighbours == 3)
            plot.update()


if __name__ == '__main__':
    game_of_life(plot_tool=CursePlot)
