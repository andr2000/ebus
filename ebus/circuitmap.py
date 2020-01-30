class CircuitMap:
    def __init__(self, circuitmap=None):
        """
        Mapping of EBUS circuit names to human-readable names with some predefined names.

        >>> c = CircuitMap({
        ...     'broadcast': '*',
        ...     'bai': 'Heater',
        ...     'mc': 'Mixer',
        ...     'hwc': 'Water',
        ... })
        >>> for circuitname, humanname in c:
        ...     print(circuitname, '=', humanname)
        broadcast = *
        bai = Heater
        mc = Mixer
        hwc = Water
        >>> tuple(c.iter_circuits())
        ('broadcast', 'bai', 'mc', 'hwc')

        Custom mappigns are added via :any:`add()`:

        >>> c = CircuitMap()
        >>> c.add('bai', 'Heater')
        >>> c.add('boo', 'My Boo')
        >>> c.add('mc.4', 'Mixer Unit 2')
        >>> c.get_humanname('bai')
        'Heater'
        >>> c.get_humanname('bai.3')
        'Heater#3'
        >>> c.get_humanname('mc.4')
        'Mixer Unit 2'
        >>> c.get_humanname('unknown')
        'unknown'
        >>> c.get_humanname('unknown.4')
        'unknown.4'
        """
        self._map = {}
        if circuitmap:
            for circuitname, humanname in circuitmap.items():
                self.add(circuitname, humanname)

    def add(self, circuitname, humanname):
        """Add mapping."""
        self._map[circuitname] = humanname

    def __iter__(self):
        yield from self._map.items()

    def iter_circuits(self):
        """Iterate over circuit names."""
        yield from self._map

    def get_humanname(self, circuitname):
        """Return human-readable name for `circuitname`."""
        # lookup full name
        humanname = self._map.get(circuitname, None)
        # loopup basename
        if humanname is None and "." in circuitname:
            basename, suffix = circuitname.split(".")
            humanname = self._map.get(basename, None)
            if humanname is not None:
                humanname = f"{humanname}#{suffix}"
        # use circuitname as default
        if humanname is None:
            humanname = circuitname
        return humanname
