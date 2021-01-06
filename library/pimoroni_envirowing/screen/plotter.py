class ScreenPlotter:
    def __init__(self, colours, bg_colour=None, max_value=None, min_value=None,
                 display=None, top_space=None, width=None, height=None,
                 extra_data=16):
        """__init__

        :param list colours: a list of colours to use for data lines

        :param int bg_colour: a background colour to use (default black)

        :param int max_value: the max value to show on the plotter (the top)

        :param int min_value: the min value to show on the plotter (the bottom)

        :param display: a supplied display object (creates one if not supplied)

        :param int top_space: the number of pixels in height to reserve for titles and labels (and not draw lines in)

        :param int width: the width in pixels of the plot (uses display width if not supplied)

        :param int height: the height in pixels of the plot (uses display width if not supplied)

        :param int extra_data: the number of updates that can be applied before a draw (16 if not supplied)
        """
        import displayio

        if not display:
            from pimoroni_envirowing import screen

            self.display = screen.Screen()
        else:
            self.display = display

        self.num_colours = len(colours) + 1

        plot_width = display.width if width is None else width
        plot_height = display.height if height is None else height
        if top_space:
            self.bitmap = displayio.Bitmap(plot_width, plot_height - top_space,
                                           self.num_colours)
            self.top_offset = top_space
        else:
            self.bitmap = displayio.Bitmap(plot_width, plot_height,
                                           self.num_colours)
            self.top_offset = 0

        self.palette = displayio.Palette(self.num_colours)

        if bg_colour:
            self.palette[0] = bg_colour
        else:
            self.palette[0] = 0x000000  # black

        for i, j in enumerate(colours):
            self.palette[i + 1] = j

        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette, y=self.top_offset)

        self.group = displayio.Group(max_size=12)

        self.group.append(self.tile_grid)

        self.display.show(self.group)

        if max_value:
            self.max_value = max_value
        else:
            self.max_value = 2**16 - 1  # max 16 bit value (unsigned)

        if min_value:
            self.min_value = min_value
        else:
            self.min_value = 0  # min 16 bit value (unsigned)

        self.value_range = self.max_value - self.min_value

        # The extra list element is a gap used for this implementation
        # of a circular buffer
        self.data_len = plot_width + extra_data + 1
        self.data_points = [None] * self.data_len
        self.data_head = 0
        self.data_tail = 0
        self.display_tail = 0
        self.displayed_points = 0

    def remap(self, value, old_min, old_max, new_min, new_max):
        return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

    def update(self, *values, draw=True):
        """update

        :param *values: the values to send to the plotter

        :param bool draw: if set to false, will not draw the line graph, just update the data points
        """
        values = list(values)

        if self.data_tail == (self.data_head - 1) % self.data_len:
            raise OverflowError("data_points full")

        if len(values) > self.num_colours - 1:
            raise OverflowError("The list of values shouldn't have more entries than the list of colours")

        for i, j in enumerate(values):
            if j > self.max_value:
                values[i] = self.max_value
            if j < self.min_value:
                values[i] = self.min_value

        self.data_points[self.data_tail] = values
        self.data_tail = (self.data_tail + 1) % self.data_len

        if draw:
            self.draw()

    def draw(self, full_refresh=False):
        """draw

        :param bool full_refresh: select clear bitmap algorithm when scrolling,
                                  default is to undraw individual prevously drawn pixels
        """
        new_points = (self.data_tail - self.display_tail if self.data_tail >= self.display_tail
                      else self.data_len - self.display_tail + self.data_tail)
        if new_points == 0:
            return

        restore_auto_refresh = False
        if self.display.auto_refresh:
            self.display.auto_refresh = False
            restore_auto_refresh = True

        num_points = (self.data_tail - self.data_head if self.data_tail >= self.data_head
                      else self.data_len - self.data_head + self.data_tail)
        heightm1 = self.bitmap.height - 1
        if num_points > self.bitmap.width:
            # scrolling
            if not full_refresh:
                for index, dpnew_index in zip(range(self.bitmap.width),
                                              range(self.data_tail - self.bitmap.width, self.data_tail)):
                    # undraw old pixels if they were in a different position
                    old_values = self.data_points[self.display_tail - self.displayed_points + index] if index < self.displayed_points else []
                    for old_value in old_values:
                        self.bitmap[index, round(self.remap(old_value, self.min_value, self.max_value, heightm1, 0))] = 0

                    # draw new pixels - this must be performed unconditionally
                    # to cater for overlapping lines
                    for subindex, new_value in enumerate(self.data_points[dpnew_index]):
                        self.bitmap[index, round(self.remap(new_value, self.min_value, self.max_value, heightm1, 0))] = subindex + 1
            else:
                # clear bitmap
                self.bitmap.fill(0)

                data_start = self.data_tail - self.bitmap.width
                for index in range(self.bitmap.width):
                    for subindexp1, point in enumerate(self.data_points[data_start + index],
                                                       start=1):
                        self.bitmap[index, round(self.remap(point, self.min_value, self.max_value, heightm1, 0))] = subindexp1
            self.displayed_points = self.bitmap.width
        else:
            # not yet scrolling
            for index in range(self.data_head + self.displayed_points, self.data_tail):
                for subindexp1, point in enumerate(self.data_points[index], start=1):
                    self.bitmap[index, round(self.remap(point, self.min_value, self.max_value, heightm1, 0))] = subindexp1
            self.displayed_points = self.data_tail

        # remove data points which have scrolled off the screen
        if num_points > self.bitmap.width:
            self.data_head = (self.data_tail - self.bitmap.width) % self.data_len
        self.display_tail = self.data_tail

        if restore_auto_refresh:
            self.display.auto_refresh = True
