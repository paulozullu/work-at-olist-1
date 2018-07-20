from datetime import timedelta


def get_previous_month(period):
    """
    Get the previous month.

        Args:
            date_ (Date object):
    """
    last_month_period = period.replace(day=1) - timedelta(days=1)
    month = last_month_period.month
    year = last_month_period.year

    return month, year
