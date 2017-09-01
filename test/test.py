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
                data = self.app.get(route)
            # print(dir(data))
            # print(data.content())
            # '_status_code', '_wrap_response', 'accept_ranges', 'add_etag', 'age', 'allow', 'autocorrect_location_header', 'automatically_set_content_length', 'cache_control', 'calculate_content_length', 'call_on_close', 'charset', 'close', 'content_encoding', 'content_language', 'content_length', 'content_location', 'content_md5', 'content_range', 'content_type', 'data', 'date', 'default_mimetype', 'default_status', 'delete_cookie', 'direct_passthrough', 'expires', 'force_type', 'freeze', 'from_app', 'get_app_iter', 'get_data', 'get_etag', 'get_wsgi_headers', 'get_wsgi_response', 'headers', 'implicit_sequence_conversion', 'is_sequence', 'is_streamed', 'iter_encoded', 'last_modified', 'location', 'make_conditional', 'make_sequence', 'mimetype', 'mimetype_params', 'response', 'retry_after', 'set_cookie', 'set_data', 'set_etag', 'status', 'status_code', 'stream', 'vary', 'www_authenticate']


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
