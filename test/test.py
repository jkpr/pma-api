#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests."""
import unittest
import json
from os import path

from manage import app
from .utils import HiddenPrints
from docunit import doctest_unittest_runner as docunit
from json.decoder import JSONDecodeError


# Super Classes
class Base(unittest.TestCase):
    """Base test class."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super(Base, self).__init__(*args, **kwargs)
        app.testing = True
        self.app = app.test_client()


class BaseRoutes(Base):
    """Base route test class."""

    ignore_routes = ('/static/<path:filename>',)
    entity_route_end_patterns = ('>',)

    def __init__(self, *args, **kwargs):
        """Init."""
        super(BaseRoutes, self).__init__(*args, **kwargs)

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

    schemata = {
        # '<route>': <expected_format>
        '': ''
    }

    def __init__(self, *args, **kwargs):
        """Init."""
        super(TestCollectionRoutes, self).__init__(*args, **kwargs)
        with HiddenPrints():
            self.routes = BaseRoutes.collection_routes()
            self.responses = self.test_smoke_test()
            self.json_responses = self.test_json_response()

    def test_smoke_test(self):
        """Smoke test routes to ensure no runtime errors."""
        return [self.app.get(route)for route in self.routes]
        # resp.status_code

    def test_json_response(self):
        """Valid json response."""
        try:
            json_responses = [json.loads(response.data) for response in
                              self.responses]
        except:
            json_responses = []

        msg = "Not all responses had valid JSON."
        self.assertEqual(len(self.responses), len(json_responses), msg=msg)

        return json_responses

    @staticmethod
    def execute_hash_table_func(func, hash_table, k, v, func_params=None):
        """Execute hash table function."""
        if func_params is None:
            func(v)
        else:
            params = {'hash_table': hash_table, 'k': k, 'v': v}
            for item in func_params:
                if item not in func_params:
                    params.pop(item)
            func(**params)

    # TODO: Recurse through all keys.
    def recurse_hash_table(self, hash_table, func, func_params=None):
        """Recurse. hash table."""
        for k, v in hash_table.items():
            self.execute_hash_table_func(func, hash_table, k, v, func_params)

    def assert_non_empty(self, hash_table, k, v):
        """Assert non empty."""
        dat = hash_table['results'] if 'results' in hash_table else None
        identifier = [k for k, _ in dat.items()][0] if type(
            dat) is dict and len(dat) != 0 else 'unknown'
        msg = 'Failed test for non-empty response values at endpoint ' \
              'identified by first result key \'{identifier}\', ' \
              'on key \'{key}\'.'

        if type(v) is not int:
            self.assertGreater(len(v), 0, msg.format(
                identifier=identifier, key=k))

    def test_non_empty_response_values(self):
        """Test to make sure that no values come back which are empty."""
        for resp in self.responses:
            data = json.loads(resp.data)
            self.recurse_hash_table(hash_table=data,
                                    func=self.assert_non_empty,
                                    func_params=['hash_table', 'k', 'v'])

    # def test_valid_response_schema(self):
    #     """Test valid response schema."""
    #     schemata = TestCollectionRoutes.schemata


# TODO: Testing of possible data types within fields, e.g. null.
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
    TEST_DIR = path.dirname(path.realpath(__file__)) + '/'
    docunit(test_dir=TEST_DIR, relative_path_to_root='../',
            package_names=['pma_api', 'test'])
