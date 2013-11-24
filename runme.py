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


def curse_plot(window, grid, fps=None, verbose=False):
    for ind, line in enumerate(grid):
        if not verbose:
            characters = line > 0
            for col, character in enumerate(characters):
                if character > 0:
                    #pass
                    window.addch(ind, col, 'X', curses.color_pair(2))
                else:
                    window.addch(ind, col, 'X', curses.color_pair(1))
        else:
            window.addstr(ind, 0, ''.join(line.astype('|S1')))
    window.refresh()

    if fps:
        time.sleep(1. / fps)


def main():
    size = (38, 143)
    if np.any([ss % 3 != 2 for ss in size]):
        msg = 'Grid size {} does not conform to size_x % 3 == 2'.format(size)
        raise ValueError(msg)

    # Make the cursor visible
    stdscr = curses.initscr()
    # No echo of input characters
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)

    # Visibility of cursor
    curses.curs_set(0)
    stdscr.refresh()

    grid = np.random.randint(0, 2, size)
    grid.astype(np.uint8)
    grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = 0

    views = window_views(grid)

    mask = np.array([[True, True, True],
                     [True, False, True],
                     [True, True, True]])

    for i in xrange(1000):
        neighbours = views[..., mask].sum(2)
        views[..., 1, 1] = (views[..., 1, 1] & ~(neighbours > 3) &
                            ~(neighbours < 2) | neighbours == 3)
        curse_plot(stdscr, grid)

    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    np.random.seed(0)
    main()
