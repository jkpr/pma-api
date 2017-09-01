#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests."""
import os
import unittest

from manage import app
from .utils import doctest_unittest_runner, HiddenPrints


# Super Classes
class Base(unittest.TestCase):
    """Base test class."""

    def setUp(self):
        """Set up: Put Flask app in test mode."""
        app.testing = True
        self.app = app.test_client()


class BaseRoutes(Base):
    """Base route test class."""

    ignore_routes = ('/static/<path:filename>', )
    entity_route_end_patterns = ('>',)

    @staticmethod
    def valid_collection_route(route):
        """Validate route.

        Args:
            route (str): Route url pattern.

        Returns:
            bool: True if valid, else False.
        """
        if route in BaseRoutes.ignore_routes \
                or route.endswith(BaseRoutes.entity_route_end_patterns):
            return False
        return True

    @staticmethod
    def collection_routes():
        """Return all collection routes."""
        return [route.rule for route in app.url_map.iter_rules()
                if BaseRoutes.valid_collection_route(route.rule)]


# Test Classes
class TestCollectionRoutes(BaseRoutes):
    """Smoke test all collection routes via HTTP GET."""

    def test_smoke_test_collection_routes(self):
        """Smoke test routes to ensure no runtime errors."""
        routes = BaseRoutes.collection_routes()

        with HiddenPrints():
            for route in routes:
                self.app.get(route)


class TestNonEmptyResponseValues(BaseRoutes):
    """Test non-empty response values."""

    def test_non_empty_response_values(self):
        """Test to make sure that no values come back which are empty."""
        for route in BaseRoutes.collection_routes():
            with HiddenPrints():
                response = self.app.get(route)
                response_data = response.data
            # print(type(response_data))  # bytes
            # print(dict(response_data))


class TestValidResponseSchema(BaseRoutes):
    """Test valid response schema."""

    schemata = {
        # '<route>': <expected_format>
        '': ''
    }

    pass


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
    TEST_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
    doctest_unittest_runner(test_dir=TEST_DIR, relative_path_to_root='../',
                            package_names=['pma_api', 'test'])
