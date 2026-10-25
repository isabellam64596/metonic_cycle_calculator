# metonic_cycle_calculator

A small, dependency-free Python library that computes the 19-year Metonic cycle position and nominal Gregorian Paschal full moon date for a given year. These are the quantities that underpin the computus — the method for calculating the date of Easter and other movable feasts.

```python
from metonic_cycle_calculator import MetonicCycleCalculator

calc = MetonicCycleCalculator()
info = calc.cycle_for_year(2024)
print(info["golden_number"])        # 11
print(info["paschal_full_moon"])    # 2024-03-25
print(info["cycle_start_year"])     # 2014
```

## Why this exists

The date of Easter is the Sunday following the "Paschal full moon," which is not an astronomical observation but a tabulated value derived from the 19-year Metonic cycle. Computing that table entry for a given year is a small, self-contained job, but it is easy to get wrong in details that matter: the golden-number formula wraps at 19 (not 20), the Gregorian calendar applies century-level solar corrections to the raw Julian table, and the tabulated dates are ecclesiastical conventions rather than astronomical predictions.

This library does one thing: it maps a year to its golden number and to the corresponding nominal Paschal full moon date from the Gregorian tabulation. It deliberately stops short of computing Easter itself, because that involves the "following Sunday" rule and additional logic that belongs in a separate, equally focused module.

## Interpretation and scope

The Gregorian computus applies a solar correction that shifts the Paschal full moon one day earlier starting in 1900, with further corrections in later centuries. This library uses the corrected tabulation valid for the years 1900 through 2199. Years outside this range are rejected with `InvalidYearError` rather than returning a silently wrong value, because the accumulated corrections would diverge from the official tables.

The exported names are:

- `MetonicCycleCalculator` — the main class, with methods `golden_number(year)`, `paschal_full_moon(year)`, and `cycle_for_year(year)`.
- `InvalidYearError` — raised when a year is outside 1900–2199.
- `GOLDEN_NUMBER` — the tuple `(1, 2, ..., 19)`.
- `PASCHAL_FULL_MOON_DATES` — the lookup table of 19 `(month, day)` pairs, indexed by golden number (index 0 is a placeholder for clean 1-based indexing).

## Edge case to know about

The golden-number formula `(year % 19) + 1` means the cycle "restarts" at years where `year % 19 == 0` (golden number 19). Do not assume golden number 1 always falls on a round-numbered year. For example, the cycle containing 2024 starts in 2014, not 2020.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

