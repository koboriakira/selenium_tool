from unittest import TestCase
from src.domain.schedule import Date


class DateTest(TestCase):
    def test_convert(self):
        suite = Date(value="2023年10月9日(月)\u3000開場13:00\u3000開始14:00")
        actual = suite.convert_date()

        self.assertEqual(actual.year, 2023)
        self.assertEqual(actual.month, 10)
        self.assertEqual(actual.day, 9)

    def test_開場時間(self):
        suite = Date(value="2023年10月9日(月)\u3000開場13:00\u3000開始14:00")
        actual = suite.open_time

        self.assertEqual(actual.hour, 13)
        self.assertEqual(actual.minute, 0)
        self.assertEqual(actual.second, 0)
