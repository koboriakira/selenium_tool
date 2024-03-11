from unittest import TestCase
from tjpw_schedule.usecase.request.scrape_range import ScrapeRange
from datetime import datetime


class TestScrapeRange(TestCase):
    def test_対象年月のリストを作成する(self):
        # Given
        suite = ScrapeRange(
            start_date=datetime(2024, 1, 1), end_date=datetime(2024, 3, 1)
        )

        # When
        actual = suite.to_target_yyyymm_list()

        # Then
        expected = ["202401", "202402", "202403"]
        self.assertEqual(actual, expected)

    def test_対象年月のリストを作成する(self):
        # Given
        suite = ScrapeRange(
            start_date=datetime(2024, 1, 1), end_date=datetime(2024, 1, 2)
        )

        # When
        actual = suite.to_target_yyyymm_list()

        # Then
        expected = ["202401"]
        self.assertEqual(actual, expected)
