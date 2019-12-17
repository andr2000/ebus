class CircuitMap:

    def __init__(self, circuitmap=None):
        """
        Mapping of EBUS circuit names to human-readable names with some predefined names.

        >>> c = CircuitMap()
        >>> c.load()
        >>> for ebusname, humanname in c:
        ...     print(ebusname, '=', humanname)
        broadcast = *
        bai = Heater
        mc = Mixer
        hwc = Water

        Custom mappigns are added via :any:`add()`:

        >>> c.add('boo', 'My Boo')
        >>> c.add('mc.4', 'Mixer Unit 2')
        >>> c.get_humanname('bai')
        'Heater'
        >>> c.get_humanname('bai.3')
        'Heater#3'
        >>> c.get_humanname('mc.4')
        'Mixer Unit 2'
        """
        self._map = {}
        if circuitmap:
            for ebusname, humanname in circuitmap.items():
                self.add(ebusname, humanname)

    def add(self, ebusname, humanname):
        """Add mapping."""
        self._map[ebusname] = humanname

    def __iter__(self):
        yield from self._map.items()

    def get_humanname(self, ebusname):
        """Return human-readable name for `ebusname`."""
        # lookup full name
        humanname = self._map.get(ebusname, None)
        # loopup basename
        if humanname is None and '.' in ebusname:
            basename, suffix = ebusname.split('.')
            humanname = self._map.get(basename, None)
            if humanname is not None:
                humanname = f'{humanname}#{suffix}'
        # use ebusname as default
        if humanname is None:
            humanname = ebusname
        return humanname

    def load(self):
        """Load Defaults."""
        self.add('broadcast', '*')
        self.add('bai', 'Heater')
        self.add('mc', 'Mixer')
        self.add('hwc', 'Water')
