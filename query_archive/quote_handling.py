"""This file is supposed to help handle quotes from date objects elaborated in the
following tutorial. However, I have found that it also affects the quotes in
other places that were intended to be left alone. Will need to manually write some
touch or don't touch indicator flags in order to use this properly. See tutorial
https://towardsdatascience.com/a-simple-approach-to-templated-sql-queries-in-python-adc4f0dc511
"""
from copy import deepcopy

from six import string_types


def quote_sql_string(value):
    """
    If `value` is a string type, escapes single quotes in the string
    and returns the string enclosed in single quotes.
    """
    if isinstance(value, string_types):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return "'{}'".format(new_value)
    return value


def get_sql_from_template(query, bind_params):
    if not bind_params:
        return query
    params = deepcopy(bind_params)
    for key, val in params.items():
        params[key] = quote_sql_string(val)
    return query % params
