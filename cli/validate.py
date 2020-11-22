import argparse
import datetime

ERROR_MESSAGES = {
    "not_an_integer": "{0} is not a valid integer. Goal must be a number "
                      "greater than zero.",
    "not_greater_than_zero": "{0} is not a goal greater than 0. Goal must be "
                             "a number greater than zero.",
    "invalid_date_format": "{0} is not a proper date format. Date format must "
                           "be in YYYY-MM-DD.",
    "date_not_in_future": "{0} is not in the future. The date must be in the "
                          "future.",
    "start_date_after_end_date": "{0} is not after {1}. Start date must come "
                                 "before end date."
}


def ArgTypeError(message, *args):
    return argparse.ArgumentTypeError(ERROR_MESSAGES[message].format(*args))


def get_num_of_args(cl_input):
    if isinstance(cl_input, str):
        return 1
    return len(cl_input)


def get_goal(goal):
    try:
        goal = int(goal)
    except ValueError:
        raise ArgTypeError("not_an_integer", goal)
    if goal <= 0:
        raise ArgTypeError("not_greater_than_zero", goal)
    return goal


def get_date(date, in_the_future=False):
    try:
        valid_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise ArgTypeError("invalid_date_format", date)
    if in_the_future and valid_date <= datetime.datetime.today().date():
        raise ArgTypeError("date_not_in_future", date)
    return valid_date


def add_goal(cl_input):
    num_of_args_passed = get_num_of_args(cl_input)
    goal = get_goal(cl_input if num_of_args_passed == 1 else cl_input[0])
    today = datetime.datetime.today().date()
    year_from_now = datetime.datetime(today.year + 1, today.month,
                                      today.day).date()
    if num_of_args_passed == 1:
        # only goal passed
        start_date = today
        end_date = year_from_now
    elif num_of_args_passed == 2:
        # only goal and end date passed
        start_date = today
        end_date = get_date(cl_input[1], in_the_future=True)
    elif num_of_args_passed == 3:
        # goal, start date, and end date passed
        # Do we need this? Unsure. Secret feature.
        start_date = get_date(cl_input[1])
        end_date = get_date(cl_input[2], in_the_future=True)
        if start_date >= end_date:
            raise ArgTypeError("start_date_after_end_date", start_date,
                               end_date)
