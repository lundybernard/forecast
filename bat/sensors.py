"""This module provides a generator for synthetic time-series data

The data simulates 2 sensors (Red, and Blue)
and an anomly that occurs based on when Red+Blue > Threshold

Sensors will include some invalid data
Anomaly events will be detected with some time-delay
"""

from typing import Generator, Literal
from random import Random


sensor_data_channel_type = Literal["anomaly", "blue", "red"]
sensor_data_values_type = bool | int

sensor_data_type = tuple[
    int, sensor_data_channel_type, sensor_data_values_type
]


def sensor_array(
    maxt: int = 1_000_000,
) -> Generator[
    int,
    sensor_data_type,
    sensor_data_values_type,
]:
    t = 0
    red_channel = red(maxt)
    blue_channel = blue(maxt)
    reds: dict[int, int] = {-1: 0, 0: 0}
    blues: dict[int, int] = {-1: 0, 0: 0}

    while t <= maxt:
        t, chan, val = next(blue_channel)
        blues[t] = val
        # print(f"yield {t=}, {chan=}, {val=}")
        yield t, chan, val

        t, chan, val = next(red_channel)
        reds[t] = val
        # print(f"yield {t=}, {chan=}, {val=}")
        yield t, chan, val

        b_2 = blues.pop(t - 2)
        r_2 = reds.pop(t - 2)

        if b_2 / 10 + r_2 > 90:
            yield t, "anomaly", True


def blue(maxt: int = 1_000_000, seed: int = 42) -> Generator[str, int, int]:
    rng = Random()
    rng.seed(seed)
    t = 0
    v = 0
    lower_bound = 0
    upper_bound = 1000

    while t < maxt:
        v += rng.randint(-10, 10)
        v = max(min(v, upper_bound), lower_bound)
        t += 1
        yield t, "blue", v


def red(maxt=1_000_000, seed=42) -> Generator[str, int, int]:
    rng = Random()
    rng.seed(seed)
    t = 0
    lower_bound = 0
    upper_bound = 100
    while t < maxt:
        t += 1
        yield t, "red", rng.randint(lower_bound, upper_bound)
