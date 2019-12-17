class CircuitMap:

    def __init__(self):
        self._map = {
            'broadcast': '*',
            'bai': 'Heater',
            'mc': 'Mixer',
            'hwc': 'Water'
        }

    def add(self, ebusname, humanname):
        """Add mapping."""
        self._map[ebusname] = humanname

    def get_humanname(self, ebusname):
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
