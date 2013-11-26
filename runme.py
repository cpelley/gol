# The MIT License (MIT)
#
# Copyright (c) 2013 cpelley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import numpy as np
import numpy.lib.stride_tricks as stride

import plot


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


def game_of_life(size=(40, 140), plot_tool=plot.CursePlot,
                 iterations=1000):
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
    game_of_life(plot_tool=plot.CursePlot)
