"""Errors module."""


class TransitionError(RuntimeError):
    """Raised for situation, when transition is not allowed."""


class AmbiguityError(RuntimeError):
    """Raised when can't decide on which solution is proper one."""
