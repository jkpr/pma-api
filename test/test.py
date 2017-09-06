#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests."""
import unittest
import json
from os import path

from docunit import doctest_unittest_runner as docunit

from manage import app
from .utils import HiddenPrints


# Super Classes
class Base(unittest.TestCase):
    """Base test class."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super(Base, self).__init__(*args, **kwargs)
        app.testing = True
        self.app = app.test_client()


# pylint: disable=dangerous-default-value
class BaseRoutes(Base):
    """Base route test class."""

    ignore_routes = ('/static/<path:filename>',)
    entity_route_end_patterns = ('>',)
    non_json_routes = ('/', )

    # TODO: (jef 2017-09-06) Test that route responses adhere to expected
    # schema. Needs: Time.
    # schemata = {
    #     # '<route>': <expected_format>
    #     '': ''
    # }

    # pylint: disable=dangerous-default-value
    @staticmethod
    def valid_route(route, conditions=list(), overrides=list()):
        """Validate route.

        Args:
            route (str): Route url pattern.
            conditions (list): Conditions.
            overrides (list): Overrides.

        Returns:
            bool: True if valid, else False.
        """
        validity = True
        validity_conditions = {
            'collections': lambda: False if route.endswith(
                BaseRoutes.entity_route_end_patterns) else True,
            'json':
                lambda: False if route in BaseRoutes.non_json_routes else True,
            'ignore_routes':
                lambda: False if route in BaseRoutes.ignore_routes else True
        }
        if 'ignore_routes' not in overrides:
            conditions.append('ignore_routes')

        for condition, check in validity_conditions.items():
            if condition in conditions:
                validity *= check()
                if validity is False:
                    break

        return bool(validity)

    # pylint: disable=dangerous-default-value
    @staticmethod
    def routes(conditions=list(), overrides=list()):
        """Get list of routes."""
        return [route.rule for route in app.url_map.iter_rules()
                if BaseRoutes.valid_route(route=route.rule,
                                          conditions=conditions,
                                          overrides=overrides)]


# Test Classes
class TestCollectionRoutes(BaseRoutes):
    """Smoke test all collection routes via HTTP GET."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super(TestCollectionRoutes, self).__init__(*args, **kwargs)
        self.empty_test = False
        self.collection_routes = BaseRoutes.routes(conditions=['collections'])
        self.json_routes = BaseRoutes.routes(conditions=['collections',
                                                         'json'])
        self.json_responses = self.test_json_response()

    def test_smoke_test(self):
        """Smoke test routes to ensure no runtime errors."""
        with HiddenPrints():
            return [self.app.get(route) for route in self.collection_routes]

    def test_json_response(self):
        """Valid json response."""
        with HiddenPrints():
            return [json.loads(self.app.get(route).data)
                    for route in self.json_routes]

    @staticmethod
    def execute_hash_table_func(hash_table, k, v, func, func_params=None):
        """Execute hash table function."""
        if func_params is None:
            func(v)
        else:
            params = {'hash_table': hash_table, 'k': k, 'v': v}
            params_list = [k for k in params]
            for item in params_list:
                if item not in func_params:
                    params.pop(item)
            func(**params)

    def recurse_hash_table(self, hash_table, func, func_params=None):
        """Recurse. hash table."""
        for k, v in hash_table.items():
            if isinstance(v, dict):
                self.recurse_hash_table(hash_table=v,
                                        func=func,
                                        func_params=func_params)
            else:
                self.execute_hash_table_func(hash_table=hash_table, func=func,
                                             func_params=func_params, k=k, v=v)

    def assert_non_empty(self, hash_table, k, v):
        """Assert non empty."""
        dat = hash_table['results'] if 'results' in hash_table else None
        identifier = [k for k, _ in dat.items()][0] \
            if isinstance(dat, dict) and dat else 'unknown'
        msg = 'Failed test for non-empty response values at endpoint ' \
              'identified by first result key \'{identifier}\', ' \
              'on key \'{key}\'.'

        if not isinstance(v, int):
            self.assertGreater(len(v), 0, msg.format(
                identifier=identifier, key=k))

    def is_empty_value(self, v):
        """Test if value is empty.

        Helper function for meta test on test_non_empty_response_values().
        """
        if v and not isinstance(v, int):
            self.empty_test = True

    def test_non_empty_response_values(self):
        """Test to make sure that no values come back which are empty.

        Catches empty values for major keys in response schema.

        Does not catch empty values for individual items, such as an empty
        field value for a given data point.

        TODO: (jef 2017-09-06) Optionally add test to catch empty field values
        for individual items based on whether or not the field is nullable.
        Needs: Time.

        Example:
                "metadata": {
                    "dataset_metadata": [],  <-- Catches Empty
                    "version": ""  <-- Catches Empty
                },
                "results": [
                    {
                        "characteristic.id": "none",
                        "characteristicGroup.id": "none",
                        "indicator.id": "",  <-- Doesn't catch.
                        "precision": 1,
                        "survey.id": "GH2013PMA",
                        "value": 15.4
                    }
                ]
            }


        """
        for route in self.json_routes:
            with HiddenPrints():
                resp = self.app.get(route)
            data = json.loads(resp.data)
            self.recurse_hash_table(hash_table=data,
                                    func=self.assert_non_empty,
                                    func_params=['hash_table', 'k', 'v'])

        def meta_tests(selfie):
            """Meta tests using static values.

            Meta tests to ensure dynamic test test_non_empty_response_values()
            is working as intended.
            """
            from copy import copy
            good_dict = {
                "metadata": {
                    "dataset_metadata": [
                        {"created_on": "Thu, 31 Aug 2017 15:06:12 GMT"},
                        {"created_on": "Thu, 31 Aug 2017 15:06:12 GMT"}
                    ],
                    "version": "0.1.2"
                },
                "resultSize": 1,
                "results": [
                    {
                        "characteristic.id": "none",
                        "characteristicGroup.id": "none",
                        "indicator.id": "mcpr_aw",
                        "precision": 1,
                        "survey.id": "GH2013PMA",
                        "value": 15.4
                    }
                ]
            }
            selfie.recurse_hash_table(hash_table=good_dict,
                                      func=selfie.assert_non_empty,
                                      func_params=['hash_table', 'k', 'v'])

            selfie.empty_test = False
            bad_dict = copy(good_dict)
            bad_dict['test_empty_1'] = []
            bad_dict['test_empty_2'] = ''
            selfie.recurse_hash_table(hash_table=bad_dict,
                                      func=selfie.is_empty_value,
                                      func_params=['v'])
            selfie.assertTrue(selfie.empty_test)
        meta_tests(self)

    # TODO: (jef 2017-09-06) Test that route responses adhere to expected
    # schema. Needs: Time.
    # def test_valid_response_schema(self):
    #     """Test valid response schema."""
    #     schemata = TestCollectionRoutes.schemata

# TODO: (jef 2017-09-06) Testing of possible data types within fields,
# e.g. null. Needs: Time
# class TestDatalabInit(TestRoutes):
#     """Test route: /datalab/init."""
#
#     routes = []
#
#     def test_datalab_init(self):
#         """Smoke test routes to ensure no runtime errors.."""
#         TestRoutes.test_routes(routes)


# class TestDB(unittest.TestCase):
#     """Test database functionality.
#
#     Link to Flask tutorial: http://flask.pocoo.org/docs/0.12/testing/
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
