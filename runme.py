import Image
import numpy as np
import numpy.lib.stride_tricks as stride


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
    window = (((grid.shape[0] - 1) / (xsize - 1)),
              ((grid.shape[1] - 1) / (ysize - 1)),
              xsize,
              ysize)
    all_windows = stride.as_strided(grid, window, strides)
    return all_windows


def main():
    size = (100, 100)
    grid = np.zeros([size[0] + 2, size[1] + 2], dtype=np.uint16)
    grid[50:53, 50:53] = 1
    views = window_views(grid)

    mask = np.array([[False, False, False],
                     [False, True, False],
                     [False, False, False]])

    # WindowObject which represents the whole screen
    stdscr = curses.initscr()
    # Make cursor invisible
    curses.curs_set(1)
    # Echoing of input characters is turned off
    curses.noecho()
    stdscr.refresh()

    curses.start_color()
    bg = curses.COLOR_WHITE
    fg = curses.COLOR_BLACK
    curses.init_pair(0, fg, bg)
    curses.init_pair(1, bg, fg)
    

    for i in xrange(10):
        for view in views:
            for view_sub in view:
                neighbours = np.sum(view_sub[mask] > 0)
                # Cell is alive.
                if view_sub[1, 1]:
                    if neighbours < 2:
                        view_sub[1, 1] = 0
                    elif neighbours > 3:
                        view_sub[1, 1] = 0
                # Cell is dead.
                else:
                    if neighbours is 3:
                        view_sub[1, 1] += 1
        image = Image.fromarray(grid, 'L')
        image.show()


if __name__ == '__main__':
    main()
