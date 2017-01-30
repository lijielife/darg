#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
mixins to enhance several tests with common code
"""

from django.db import DEFAULT_DB_ALIAS, connections
from django.test.utils import CaptureQueriesContext


# stolen here https://goo.gl/IdWkTr
class _AssertLessNumQueriesContext(CaptureQueriesContext):
    """ context manager to check for queries less then x """

    def __init__(self, test_case, num, connection):
        self.test_case = test_case
        self.num = num
        super(_AssertLessNumQueriesContext, self).__init__(connection)

    def __exit__(self, exc_type, exc_value, traceback):
        super(_AssertLessNumQueriesContext, self).__exit__(
            exc_type, exc_value, traceback)
        if exc_type is not None:
            return
        executed = len(self)
        # altered here from assertEqual to assertLess
        self.test_case.assertLessEqual(
            executed, self.num,
            "%d queries executed, less then %d expected\n"
            "Captured queries were:\n%s" % (
                executed, self.num,
                '\n'.join(
                    query['sql'] for query in self.captured_queries
                )
            )
        )


class MoreAssertsTestCaseMixin(object):
    """
    some very helpfull asserts...
    """

    def assertLessNumQueries(self, num, func=None, *args, **kwargs):
        """
        ensure we do not run more queries then what's good for us
        learned here https://goo.gl/0Z8QW2
        """
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _AssertLessNumQueriesContext(self, num, conn)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)
