import argparse
import datetime

from goal import Goal

ERROR_MESSAGES = {
    "not_an_integer": "{0} is not a valid integer. Goal must be a number "
                      "greater than zero.",
    "not_greater_than_zero": "{0} is not a goal greater than 0. Goal must be "
                             "a number greater than zero.",
    "invalid_date_format": "{0} is not a proper date format. Date format must "
                           "be in YYYY-MM-DD.",
    "date_not_in_future": "{0} is not in the future. The date must be in the "
                          "future.",
    "date_in_future": "{0} is in the future. The date must be today or in the "
                      "past.",
    "start_date_after_end_date": "{0} is not after {1}. Start date must come "
                                 "before end date.",
}


def ArgTypeError(message, *args):
    return argparse.ArgumentTypeError(ERROR_MESSAGES[message].format(*args))


def get_num_of_args(cl_input):
    if isinstance(cl_input, str):
        return 1
    return len(cl_input)


def goal_number(goal_num):
    try:
        goal_num = int(goal_num)
    except ValueError:
        raise ArgTypeError("not_an_integer", goal_num)
    if goal_num <= 0:
        raise ArgTypeError("not_greater_than_zero", goal_num)
    return goal_num


def get_date(date, in_the_future=False):
    try:
        valid_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise ArgTypeError("invalid_date_format", date)

    if in_the_future and valid_date <= datetime.datetime.today().date():
        raise ArgTypeError("date_not_in_future", date)
    elif not in_the_future and valid_date > datetime.datetime.today().date():
        raise ArgTypeError("date_in_future", date)
    return valid_date


def get_future_date(date):
    return get_date(date, in_the_future=True)


def goal(goal_num, start_date, end_date):
    if start_date >= end_date:
        raise ArgTypeError("start_date_after_end_date", start_date, end_date)
    return Goal(num_books=goal_num, start_date=start_date, end_date=end_date)
