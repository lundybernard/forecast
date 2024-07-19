from unittest import TestCase

from ..sensors import sensor_array, blue, red


class SensorsTests(TestCase):

    def test_sensor_array(t):
        # sensor array generator object
        sa = sensor_array()

        ret = [next(sa) for _ in range(4)]

        # Assume random seed=42
        t.assertListEqual(
            ret,
            [
                (1, "blue", 10),
                (1, "red", 81),
                (2, "blue", 3),
                (2, "red", 14),
            ],
        )

    def test_anomaly_sensor(t):
        sa = sensor_array(maxt=100)
        anomaly: tuple[int, bool] | None = None
        blue_hist: dict[int, int] = {}
        red_hist: dict[int, int] = {}

        while anomaly is None:
            time, channel, value = next(sa)
            match channel:
                case "anomaly":
                    anomaly = time
                case "blue":
                    blue_hist[time] = value
                case "red":
                    red_hist[time] = value

        blue_2 = blue_hist[time - 2]
        red_2 = red_hist[time - 2]

        t.assertEqual(6, anomaly)
        t.assertGreaterEqual(red_2 + blue_2 / 10, 90)

    def test_blue(t):
        b = blue()
        ret = [next(b) for _ in range(4)]
        t.assertListEqual(
            [(1, "blue", 10), (2, "blue", 3), (3, "blue", 0), (4, "blue", 0)],
            ret,
        )

    def test_red(t):
        r = red()
        ret = [next(r) for _ in range(4)]
        t.assertListEqual(
            [(1, "red", 81), (2, "red", 14), (3, "red", 3), (4, "red", 94)],
            ret,
        )
