"""Extra utilities for state machines, to make them more usable."""


class ProxyString(str):

    """String that proxies every call to nested machine."""

    def __new__(cls, value, machine):
        """Create new string instance with reference to given machine."""
        string = super(cls, cls).__new__(cls, value)
        string.state_machine = machine
        return string

    def __getattr__(self, name):
        """Proxy call to machine."""
        return getattr(self.state_machine, name)


class PropertyMachine(object):

    """Descriptor to help using machines as properties."""

    def __init__(self, machine_type):
        """Create descriptor."""
        self._memory = {}
        self._machine_type = machine_type

    def _check_machine(self, obj):
        try:
            machine = self._memory[obj]
        except KeyError:
            machine = self._machine_type()
            self._memory[obj] = machine

    def __set__(self, obj, value):
        """Set state to machine."""
        self._check_machine(obj)
        self._memory[obj].set_(value)

    def __get__(self, obj, _type=None):
        """Get machine state."""
        if obj is None:
            return self

        self._check_machine(obj)

        machine = self._memory[obj]
        try:
            actual_state = machine.actual_state.value
        except AttributeError:
            actual_state = ''

        return ProxyString(actual_state, machine)
