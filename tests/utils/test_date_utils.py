from pandas import Timestamp
from nose_parameterized import parameterized

from zipline.testing import ZiplineTestCase
from zipline.utils.calendars import get_calendar
from zipline.utils.date_utils import (
    compute_date_range_chunks,
    roll_dates_to_previous_session
)


class TestDateUtils(ZiplineTestCase):

    @classmethod
    def init_class_fixtures(cls):
        super(TestDateUtils, cls).init_class_fixtures()
        cls.calendar = get_calendar('NYSE')

    @parameterized.expand([
        (
            Timestamp('05-19-2017', tz='UTC'),  # actual trading date
            Timestamp('05-19-2017', tz='UTC'),
        ),
        (
            Timestamp('07-04-2015', tz='UTC'),  # weekend nyse holiday
            Timestamp('07-02-2015', tz='UTC'),
        ),
        (
            Timestamp('01-16-2017', tz='UTC'),  # weeknight nyse holiday
            Timestamp('01-13-2017', tz='UTC'),
        ),
    ])
    def test_roll_dates_to_previous_session(self, date, expected_rolled_date):
        self.assertEqual(
            roll_dates_to_previous_session(
                self.calendar.all_sessions,
                date
            )[0],
            expected_rolled_date
        )

    @parameterized.expand([
        (
            None,
            [
                (
                    Timestamp('01-03-2017', tz='UTC'),
                    Timestamp('01-31-2017', tz='UTC')
                )
            ]
        ),
        (
            10,
            [
                (
                    Timestamp('01-03-2017', tz='UTC'),
                    Timestamp('01-17-2017', tz='UTC')
                ),
                (
                    Timestamp('01-18-2017', tz='UTC'),
                    Timestamp('01-31-2017', tz='UTC')
                )
            ]
        ),
        (
            15,
            [
                (
                    Timestamp('01-03-2017', tz='UTC'),
                    Timestamp('01-24-2017', tz='UTC')
                ),
                (
                    Timestamp('01-25-2017', tz='UTC'),
                    Timestamp('01-31-2017', tz='UTC')
                )
            ]
        ),
    ])
    def test_compute_date_range_chunks(self, chunksize, expected):
        # These date ranges result in 20 business days
        start_date = Timestamp('01-03-2017', tz='UTC')
        end_date = Timestamp('01-31-2017', tz='UTC')

        date_ranges = compute_date_range_chunks(
            self.calendar.all_sessions,
            start_date,
            end_date,
            chunksize
        )

        self.assertListEqual(list(date_ranges), expected)

    def test_compute_date_range_chunks_invalid_input(self):

        # Start date not found in calendar
        with self.assertRaises(KeyError) as cm:
            compute_date_range_chunks(
                self.calendar.all_sessions,
                Timestamp('05-07-2017'),  # Sunday
                Timestamp('06-01-2017'),
                None
            )
        self.assertEqual(
            cm.exception.message,
            "Start date 2017-05-07 is not found in calendar."
        )

        # End date not found in calendar
        with self.assertRaises(KeyError) as cm:
            compute_date_range_chunks(
                self.calendar.all_sessions,
                Timestamp('05-01-2017'),
                Timestamp('05-27-2017'),  # Saturday
                None
            )
        self.assertEqual(
            cm.exception.message,
            "End date 2017-05-27 is not found in calendar."
        )

        # End date before start date
        with self.assertRaises(ValueError) as cm:
            compute_date_range_chunks(
                self.calendar.all_sessions,
                Timestamp('06-01-2017'),
                Timestamp('05-01-2017'),
                None
            )
        self.assertEqual(
            cm.exception.message,
            "End date 2017-05-01 cannot precede start date 2017-06-01."
        )
