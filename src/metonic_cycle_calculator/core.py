"""Core logic for the Metonic cycle calculator.

The Metonic cycle is a period of 19 years after which the phases of the
moon recur on the same days of the year. It forms the backbone of the
computus: the calculation of the date of Easter. In the Gregorian and
Julian calendars, each year is assigned a "golden number" derived from
its position in the 19-year cycle, and this number is used to look up a
nominal date for the Paschal full moon.

This module is deliberately focused: it answers the question "what is the
golden number and nominal Paschal full moon for a given year?" It does
not compute the actual date of Easter, which involves additional rules
(the following Sunday, epact corrections, and century-level solar
adjustments) that would obscure the small, specific job this library
exists to do.

Interpretation chosen
---------------------
The Gregorian computus applies century-level "solar corrections" to
the simple Julian golden-number scheme. These corrections (one per
century from 1900 onward, accumulating at a rate that approximates the
astronomical drift) shift the Paschal full moon by one day relative to
the classical tabulation. This library implements that corrected,
Gregorian tabulation rather than the raw Julian one, because a library
that claims to compute "the Metonic cycle for movable feasts" and
silently ignores the Gregorian correction is wrong on its face. The
cost is a lookup table that is strictly correct only for the range
1900-2199; outside that range the solar corrections have continued to
accumulate in the real calendar and this library will not match the
official tables.

The table below encodes the Gregorian Paschal full moon dates in effect
for the 20th through 22nd centuries. The 19 entries are indexed by the
classical golden number (1 through 19).
"""

from datetime import date
from typing import Dict, List


class InvalidYearError(ValueError):
    """Raised when a year is outside the supported range of the table."""


# The classical golden-number formula: (year mod 19) + 1.
# In the 19-year cycle, golden number 1 follows golden number 19, so
# the modulo arithmetic maps 19 -> 19 and wraps at 20, which the
# Python % operator handles correctly.


# Nominal Gregorian Paschal full moon dates for golden numbers 1-19,
# valid for years 1900-2199. Each value is a (month, day) pair.
# These are the standard tabulated values used by the Gregorian
# computus in that date range; they incorporate the single solar
# correction applied starting in 1900 (one day earlier than the
# Julian tabulation).
PASCHAL_FULL_MOON_DATES: List[tuple] = [
    (4, 14),  # index 0, golden number 1  - not used, but keeps indexing simple
    (4, 14),  # golden number 1
    (4, 3),   # golden number 2
    (3, 23),  # golden number 3
    (4, 11),  # golden number 4
    (3, 31),  # golden number 5
    (4, 18),  # golden number 6
    (4, 8),   # golden number 7
    (3, 28),  # golden number 8
    (4, 16),  # golden number 9
    (4, 5),   # golden number 10
    (3, 25),  # golden number 11
    (4, 13),  # golden number 12
    (4, 2),   # golden number 13
    (3, 22),  # golden number 14
    (4, 10),  # golden number 15
    (3, 30),  # golden number 16
    (4, 17),  # golden number 17
    (4, 7),   # golden number 18
    (3, 27),  # golden number 19
]


class MetonicCycleCalculator:
    """Calculate golden numbers and nominal Paschal full moon dates.

    The calculator works with the Gregorian tabulation of the Paschal
    full moon that is valid for the years 1900 through 2199. Years
    outside this range are rejected with :class:`InvalidYearError`
    because the century-level solar corrections would give
    misleading results without a much larger table.
    """

    MIN_YEAR = 1900
    MAX_YEAR = 2199

    def __init__(self) -> None:
        # No state is needed; the class is stateless. The constructor
        # exists so future versions could accept a clock or configuration
        # without changing call sites, and so the object carries its
        # own documented domain (MIN_YEAR / MAX_YEAR).
        pass

    def golden_number(self, year: int) -> int:
        """Return the golden number (1-19) for *year*.

        The golden number is (year mod 19) + 1, matching the classical
        computus convention. Year 0 is rejected because the Gregorian
        calendar has no year 0 and using it would produce a nonsensical
        cycle position.
        """
        if year < self.MIN_YEAR or year > self.MAX_YEAR:
            raise InvalidYearError(
                f"Year {year} is outside the supported range "
                f"({self.MIN_YEAR}-{self.MAX_YEAR})."
            )
        return (year % 19) + 1

    def paschal_full_moon(self, year: int) -> date:
        """Return the nominal Gregorian Paschal full moon date for *year*.

        The returned date is the tabulated ecclesiastical full moon,
        not an astronomical observation. Easter is defined as the
        Sunday following this date.
        """
        gn = self.golden_number(year)
        month, day = PASCHAL_FULL_MOON_DATES[gn]
        return date(year, month, day)

    def cycle_for_year(self, year: int) -> Dict[str, object]:
        """Return a summary of the Metonic cycle position for *year*.

        The keys are:
        - ``year``: the year passed in
        - ``golden_number``: 1-19
        - "paschal_full_moon": the tabulated date
        - ``cycle_start_year``: the first year of the 19-year cycle
          containing *year* in the Julian golden-number reckoning
        """
        gn = self.golden_number(year)
        pfm = self.paschal_full_moon(year)
        # The cycle "starts" at the year whose golden number is 1.
        cycle_start = year - (gn - 1)
        return {
            "year": year,
            "golden_number": gn,
            "paschal_full_moon": pfm,
            "cycle_start_year": cycle_start,
        }


# Convenience module-level constant: the full set of 19 golden numbers.
GOLDEN_NUMBER = tuple(range(1, 20))
