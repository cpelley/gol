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
from abc import ABCMeta, abstractmethod
import curses
import time


class Plot(object):
    """Abstract class for a GOL simulation graphical backend."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
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

    def __exit__(self, type, value, traceback):
        # Close curses.
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()
