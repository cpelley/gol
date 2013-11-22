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

    # Make the cursor visible
    stdscr = curses.initscr()
    # No echo of input characters
    curses.noecho()
    # Visibility of cursor
    curses.curs_set(1)
    stdscr.refresh()




    size = (37, 72)
    grid = np.random.randint(0, 2, size)
    grid.astype(np.uint8)
    grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = 0

    views = window_views(grid)

    mask = np.array([[True, True, True],
                     [True, False, True],
                     [True, True, True]])

    for i in xrange(10000):
#        print i
        #plot(grid)
#        break
        for ind, view in enumerate(views):
            for inds, view_sub in enumerate(view):
                neighbours = np.sum(view_sub[mask] > 0)
                # Cell is alive.
                if view_sub[1, 1]:
                    if neighbours < 2:
                        view_sub[1, 1] = 0
                    elif neighbours > 3:
                        view_sub[1, 1] = 0
                # Cell is dead.
                else:
                    if neighbours == 3:
                        view_sub[1, 1] += 1

                stdscr.addch(ind + 1, inds + 1, str(neighbours))
                stdscr.addch(ind + 1, inds + 1 + 73, '1' if view_sub[1, 1] else '0')
        stdscr.addstr(40, 5, str(i))
        stdscr.refresh()

    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    main()
