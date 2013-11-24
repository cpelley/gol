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


def mpl_plot(grid):
    plt.figure()
    plt.pcolor(grid)
    plt.show()


class CursePlot(object):
    def __init__(self, grid, window=None, fps=None):
        self.fps = fps
        if window:
            self.window = window
        else:
            self.window = curses.initscr()
        self.grid = grid

        # No echo of input characters
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)

        # Visibility of cursor
        curses.curs_set(0)

    def __enter__(self):
        return self

    def update(self):
        for ind, line in enumerate(self.grid):
            pout = ''.join(line.astype('|S1')).replace('0', ' ')
            self.window.addstr(ind, 0, pout)
        self.window.refresh()

        if self.fps:
            time.sleep(1. / self.fps)

    def __exit__(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()


def game_of_life(size=(40, 140), plot_tool=CursePlot):
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
        for i in xrange(1000):
            neighbours = views[..., mask].sum(2)
            views[..., 1, 1] = (views[..., 1, 1] & ~(neighbours > 3) &
                                ~(neighbours < 2) | neighbours == 3)
            plot.update()


if __name__ == '__main__':
    game_of_life(plot_tool=CursePlot)
