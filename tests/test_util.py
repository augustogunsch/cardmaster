import unittest
from datetime import datetime, timezone, timedelta
from ..app.util.date import normalize

class TestUtil(unittest.TestCase):
    def test_normalize(self):
        tz = timezone(timedelta(hours=1))
        date = datetime(2023, 11, 7, hour=13, minute=51, tzinfo=tz)
        pre_normalized = datetime(2023, 11, 7, hour=12, minute=51)
        normalized = normalize(date)
        self.assertEqual(normalized, pre_normalized)
