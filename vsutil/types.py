"""
Enums and related functions.
"""
__all__ = ['Dither', 'Range']

# this file only depends on the stdlib and should stay that way
from enum import Enum
from typing import Any, Optional, Type, TypeVar, Union

E = TypeVar('E', bound=Enum)


class _NoSubmoduleRepr(Enum):
    def __repr__(self):
        """Removes submodule name from standard repr, helpful since we re-export everything at the top-level."""
        return '<%s.%s.%s: %r>' % (self.__module__.split('.')[0], self.__class__.__name__, self.name, self.value)


class Dither(str, _NoSubmoduleRepr):
    """
    Enum for `zimg_dither_type_e`.
    """
    NONE = 'none'
    """Round to nearest."""
    ORDERED = 'ordered'
    """Bayer patterned dither."""
    RANDOM = 'random'
    """Pseudo-random noise of magnitude 0.5."""
    ERROR_DIFFUSION = 'error_diffusion'
    """Floyd-Steinberg error diffusion."""


class Range(int, _NoSubmoduleRepr):
    """
    Enum for `zimg_pixel_range_e`.
    """
    LIMITED = 0
    """Studio (TV) legal range, 16-235 in 8 bits."""
    FULL = 1
    """Full (PC) dynamic range, 0-255 in 8 bits."""


def _readable_enums(enum: Type[Enum]) -> str:
    """
    Returns a list of all possible values in `enum`.
    Since VapourSynth imported enums don't carry the correct module name, use a special case for them.
    """
    if 'importlib' in enum.__module__:
        return ', '.join([f'<vapoursynth.{i.name}: {i.value}>' for i in enum])
    else:
        return ', '.join([repr(i) for i in enum])


def _resolve_enum(enum: Type[E], value: Any, var_name: str, module: Optional[str] = None) -> Union[E, None]:
    """
    Attempts to evaluate `value` in `enum` if value is not None, otherwise returns None.
    Basically checks if a supplied enum value is valid and returns a readable error message
    explaining the possible enum values if it isn't.
    """
    if value is None:
        return None
    try:
        return enum(value)
    except ValueError:
        raise ValueError(f'{var_name} must be in {_readable_enums(enum, module)}.') from None
