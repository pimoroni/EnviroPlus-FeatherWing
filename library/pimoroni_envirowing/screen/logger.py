class ScreenLogger:
    def __init__(self, colours, bg_colour=None, max_value=None, min_value=None):
        """__init__

        :param list colours: a list of colours to use for data lines

        :param int bg_colour: a background colour to use (default black)

        :param int max_value: the max value to show on the plotter (the top)

        :param int min_value: the min value to show on the plotter (the bottom)
        """

        #region Screen setup
        """
        This region of code is used to setup the envirowing screen with displayio
        """

        import board, time
        import pimoroni_physical_feather_pins
        import displayio
        from adafruit_st7735r import ST7735R

        self.spi = board.SPI() # define which spi bus the screen is on
        self.spi.try_lock() # try to get control of the spi bus
        self.spi.configure(baudrate=100000000) # tell the spi bus how fast it's going to run
        # baudrate doesn't need to be this high in practice, it's just nice to have a quick screen refresh in this case
        self.spi.unlock() # unlocks the spi bus so displayio can control it
        #self.tft_dc = pimoroni_physical_feather_pins.pin19() # define which pin the command line is on
        #self.tft_cs = pimoroni_physical_feather_pins.pin20() # define which pin the chip select line is on

        displayio.release_displays() # release any displays that may exist from previous code run
        self.display_bus = displayio.FourWire(self.spi, command=pimoroni_physical_feather_pins.pin19(), chip_select=pimoroni_physical_feather_pins.pin20(), reset=pimoroni_physical_feather_pins.pin21()) # define the display bus

        self.display = ST7735R(self.display_bus, width=160, height=80, colstart=26, rowstart=1, rotation=270, invert=True)# define the display (these values are specific to the envirowing's screen)

        #endregion Screen setup

        self.num_colours = len(colours) + 1

        self.bitmap = displayio.Bitmap(160, 80, self.num_colours)

        self.palette = displayio.Palette(self.num_colours)

        if bg_colour:
            self.palette[0] = bg_colour
        else:
            self.palette[0] = 0x000000 # black

        for i,j in enumerate(colours):
            self.palette[i+1] = j
        
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)

        self.group = displayio.Group(max_size=12)

        self.group.append(self.tile_grid)

        self.display.show(self.group)

        if max_value:
            self.max_value = max_value
        else:
            self.max_value = 2**16 - 1 # max 16 bit value (unsigned)

        if min_value:
            self.min_value = min_value
        else:
            self.min_value = 0 # min 16 bit value (unsigned)
        
        self.value_range = self.max_value - self.min_value

        self.data_points = []

    def remap(self, Value, OldMin,OldMax, NewMin, NewMax):
        return (((Value - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    
    def update(self, *values):
        """update

        :param *values: the values to send to the logger
        """
        
        values = list(values)

        if len(values) > (self.num_colours - 1):
            raise Exception("The list of values shouldn't have more entries than the list of colours")
        
        for i,j in enumerate(values):
            if j > self.max_value:
                values[i] = self.max_value
            if j < self.min_value:
                values[i] = self.min_value

        """
        #TODO: Scroll the screen here
        for i in range(1, (self.bitmap.width*self.bitmap.height)):
            if (i + 1) % self.bitmap.width != 0:
                self.bitmap[i] = self.bitmap[i+1]
            else:
                self.bitmap[i] = 0

        for index,value in enumerate(values):
            self.bitmap[(self.bitmap.width - 1),round(((value - self.min_value) / self.value_range) * self.bitmap.height)] = index + 1
        """

        old_points = self.data_points

        self.data_points.append(values)

        if len(self.data_points) > self.bitmap.width:
            self.data_points = self.data_points[1:] # pop doesn't work in circuitpython
        
            difference = []

            for i,j in zip(self.data_points, old_points):
                subarray = []
                for value in zip(i,j):
                    subarray.append((value[0] - value[1]))
                difference.append(subarray)

            for index,value in enumerate(difference):
                for subindex,point in enumerate(value):
                    if point != 0:
                        #self.bitmap[index,round(((old_points[index][subindex] - self.min_value) / self.value_range) * -(self.bitmap.height -1) + (self.bitmap.height -1))] = 0
                        self.bitmap[index,round(self.remap(old_points[index][subindex], self.min_value, self.max_value, self.bitmap.height - 1, 0))] = 0
                        #self.bitmap[index,round(((self.data_points[index][subindex] - self.min_value) / self.value_range) * -(self.bitmap.height -1) + (self.bitmap.height -1))] = subindex + 1
                        self.bitmap[index,round(self.remap(self.data_points[index][subindex], self.min_value, self.max_value, self.bitmap.height - 1, 0))] = subindex + 1
        else:
            
            for subindex,point in enumerate(self.data_points[-1]):
                #self.bitmap[(len(self.data_points) - 1),round(((point - self.min_value) / self.value_range) * -(self.bitmap.height -1) + (self.bitmap.height -1))] = subindex + 1
                self.bitmap[(len(self.data_points) - 1),round(self.remap(point, self.min_value, self.max_value, self.bitmap.height - 1, 0))] = subindex + 1