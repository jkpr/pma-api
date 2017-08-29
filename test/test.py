#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests."""
import os
import unittest

from manage import app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up: Put Flask app in test mode."""
        app.testing = True
        self.app = app.test_client()

    def test_routes(self, routes):
        """Smoke test routes to ensure no runtime errors.."""
        for route in routes:
            self.app.get(route)


class TestAllRoutes(TestRoutes):
    """Test routes."""

    ignore_routes = ('/static/<path:filename>',)
    ignore_end_patterns = ('>',)

    # Init?

    def test_all_routes(self):
        """Test all routes."""
        routes = [route.rule for route in app.url_map.iter_rules()
              if self.valid_route(route.rule)]
        self.test_routes(routes)

    @staticmethod
    def valid_route(route):
        """Validate route.

        Args:
            route (str): Route url pattern.

        Returns:
            bool: True if valid, else False.
        """
        if route in TestAllRoutes.ignore_routes \
                or route.endswith(TestAllRoutes.ignore_end_patterns):
            return False
        return True


# class TestDatalabInit(TestRoutes):
#     """Test route: /datalab/init."""
#
#     routes = []
#
#     def test_datalab_init(self):
#         """Smoke test routes to ensure no runtime errors.."""
#         TestRoutes.test_routes(routes)


# class TestDB(unittest.TestCase):  # TODO: Adapt from tutorial.
#     """Test database functionality.
#
#     Tutorial: http://flask.pocoo.org/docs/0.12/testing/
#     """
#
#     def setUp(self):
#         """Set up: (1) Put Flask app in test mode, (2) Create temp DB."""
#         import tempfile
#         from manage import initdb
#         self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#         app.testing = True
#         self.app = app.test_client()
#         with app.app_context():
#             initdb()
#
#     def tearDown(self):
#         """Tear down: (1) Close temp DB."""
#         os.close(self.db_fd)
#         os.unlink(app.config['DATABASE'])
#
#     def test_empty_db(self):
#         """Test empty database."""
#         resp = self.app.get('/')
#         assert b'No entries here so far' in resp.data


if __name__ == '__main__':
    from test.utils.doctest_unittest_runner import doctest_unittest_runner
    TEST_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
    doctest_unittest_runner(test_dir=TEST_DIR, relative_path_to_root='../',
                            package_names=['pma_api', 'test'])
