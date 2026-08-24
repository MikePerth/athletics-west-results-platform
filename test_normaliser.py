from app.services.performance_utils import (
    normalise_event_name
)

tests = [
    "80m Hurdles",
    "90m Hurdles",
    "100m Hurdles",
    "110m Hurdles",
    "200m Hurdles",
    "400m Hurdles",

    "LA Hurdles 68cm 80m Hurdles",
    "LA Hurdles 68cm 200m Hurdles",

    "Mcgillivray Discus Throw",

    "U20 and Open Hammer Throw",
    "U20 to Open Discus Throw",

    "(Pit 4) Long Jump",

    "U20 - Open Shot Put",
]

for test in tests:

    result = normalise_event_name(test)

    print(
        f"{test} --> {result}"
    )