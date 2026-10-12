"""metonic_cycle_calculator

A small, dependency-free library for working with the 19-year Metonic
cycle as used in computus (the calculation of the date of Easter).
"""

from .core import (
    GOLDEN_NUMBER,
    PASCHAL_FULL_MOON_DATES,
    MetonicCycleCalculator,
    InvalidYearError,
)

__all__ = [
    "GOLDEN_NUMBER",
    "PASCHAL_FULL_MOON_DATES",
    "MetonicCycleCalculator",
    "InvalidYearError",
]

__version__ = "1.0.0"
