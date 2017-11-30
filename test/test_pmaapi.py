#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests."""
import os
import unittest

from manage import app
from config import Config


class TestRoutes(unittest.TestCase):
    """Test routes."""

    ignore_routes = ('/static/<path:filename>',)
    ignore_end_patterns = ('>',)

    def setUp(self):
        """Set up: Put Flask app in test mode."""
        app.testing = True
        self.app = app.test_client()

    @staticmethod
    def valid_route(route):
        """Validate route.

        Args:
            route (str): Route url pattern.

        Returns:
            bool: True if valid, else False.
        """
        if route in TestRoutes.ignore_routes \
                or route.endswith(TestRoutes.ignore_end_patterns):
            return False
        return True

    def test_routes(self):
        """Smoke test routes to ensure no runtime errors.."""
        routes = [route.rule for route in app.url_map.iter_rules()
                  if self.valid_route(route.rule)]
        for route in routes:
            self.app.get(route)


class TestPerformance(unittest.TestCase):
    """Test performance."""

    # TODO: Make this database.
    config = Config().SQLALCHEMY_DATABASE_URI =\
        'postgresql+psycopg2://pmaapi:pmaapi@localhost/pmaapi-test'

    def test_create_db(self):
        """Test performance on db creation."""
        # change these values to something reasonable
        expected = expected_seconds_elapsed_by_n_rows = {
            50: 7200,
            100: 7200,
            200: 7200,
            400: 7200,
        }
        actual = {
            50: None,
            100: None,
            200: None,
            400: None
        }

        # from datetime import timedelta
        from datetime import datetime

        for i in expected_seconds_elapsed_by_n_rows:
            # use logger?
            t0 = datetime.now().time()
            ta = datetime.now()
            # Run process on manage.py
            t1 = datetime.now().time()
            tb = datetime.now()
            actual[i] = tb - ta
            print (t1, tb, actual[i])
            # print(actual[i])
            self.assertLess(actual[i], expected[i])

        # determine o(n) for 'actual'
        # do an assert on that o(n)


if __name__ == '__main__':
    from test.utils.doctest_unittest_runner import doctest_unittest_runner
    TEST_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
    doctest_unittest_runner(test_dir=TEST_DIR, relative_path_to_root='../',
                            package_names=['pma_api', 'test'])
