class Logger:
    def __init__(self, measurements, headers=None, filename=None, use_SD=True, spi=None, SD_CS=None):
        """__init__

        :param int measurements: The number of different measurements that will be taken per reading.

        :param list headers: A list of strings of headers for the different measurements. List length must be equal to `measurements`. If None, headers will not be used.

        :param string filename: Filename of the log. Defaults to `log.txt` if none is supplied.

        :param bool use_SD: Whether to write to the SD card or the local filesystem. Defaults to SD.

        :param spi: A supplied spi bus. Creates it's own if none is supplied. Only used if `use_SD` is `True`.

        :param SD_CS: The SD card's chip select pin. if none is supplied, it will try the inbuilt `board.SD_CS`
        """

        self.reading_no = 0
        self.num_measurements = 0

        if headers:
            assert (measurements == len(headers)), "The number of headers must equal the number of different measurements"

            self.num_measurements = measurements

            self.headers = ["Reading no"] + headers

        if filename:
            self.filename = filename
        else:
            self.filename = "log.txt"
        
        import storage

        if use_SD:
            import adafruit_sdcard, digitalio

            if spi:
                self.spi = spi
            else:
                import board
                self.spi = board.SPI()
            
            if SD_CS:
                self.SD_CS = SD_CS
            else:
                import board
                try:
                    self.SD_CS = board.SD_CS
                except AttributeError:
                    raise AttributeError("Your board does not have a built in SD card, please supply the chip select pin for the SD card of the addon board")
            
            self.sdcard = adafruit_sdcard.SDCard(self.spi, digitalio.DigitalInOut(self.SD_CS))
            self.vfs = storage.VfsFat(self.sdcard)
            storage.mount(self.vfs, "/sd")

            self.filepath = "/sd/" + self.filename
        
        else:
            #print("WARNING!! This will not work unless you have set up boot.py to mount the filesystem as rw, see https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage")

            try:
                storage.remount("/")

                self.filepath = "/" + self.filename
            except RuntimeError as e:
                raise RuntimeError(str(e) + "\nLocal filesystem logging will only work when CIRCUITPY is not mounted by a computer") # will only work once running a release after https://github.com/adafruit/circuitpython/commit/8e8eb07
        
        try:
            with open(self.filepath, "r") as f:
                # check if continuing last log or starting a new one
                firstline = f.readline().split(",")
                for index, value in enumerate(firstline):
                    firstline[index] = value.strip()
                if firstline == self.headers or firstline[0] == "0":
                    for line in f:
                        if line != "\n":
                            lastline = line
                    lastline = lastline.split(",")
                    self.reading_no = int(lastline[0]) + 1
                    self.num_measurements = len(lastline) - 1
                    newfileneeded = False
                else:
                    from os import rename
                    rename(self.filepath, self.filepath + ".old")
                    newfileneeded = True

        except OSError as e:
            if e.args[0] == 2:
                # no such file
                newfileneeded = True

            elif e.args[0] == 30:
                # read only fs
                raise RuntimeError("The filesystem has been mounted as read only")
        
        if newfileneeded:
            with open(self.filepath, "w") as f:
                if headers:
                    f.write(', '.join(str(x) for x in self.headers))
                    f.write("\n")
                
    def log(self, *values):
        """log
        
        :param *values: the values to send to the log. The number of values must equal the number of values in previous logs and/or headers.
        """
        if not self.num_measurements:
            self.num_measurements = len(values)
        
        assert (self.num_measurements == len(values)), "The number of measurements must be consistent. If you are being consistent, check you're not using the same filename as a previously run program"

        values = [self.reading_no] + list(values)

        self.reading_no += 1

        with open(self.filepath, "a") as f:
            f.write(', '.join(str(x) for x in values))
            f.write("\n")
        
