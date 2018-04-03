#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_borea
----------------------------------

Tests for `borea` module.
"""

import unittest
import json
import tornado.testing
import borea.app


class TestBorea(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return borea.app.make_app()
    
    def test_add_user(self):
        response = self.fetch("/borea/userTest")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        self.assertTrue("userTest" in res)

    def test_list_users(self):
        response = self.fetch("/borea")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        self.assertEqual(len(res), 0)

        response = self.fetch("/borea/uno")
        self.assertEqual(response.code, 200)
        response = self.fetch("/borea/due")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        self.assertEqual(len(res), 2)
        self.assertTrue("due" in res)
        self.assertTrue("uno" in res)

        # check for duplicates
        response = self.fetch("/borea/uno")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        self.assertEqual(len(res), 2)
        self.assertTrue("due" in res)
        self.assertTrue("uno" in res)

    def test_remove_users(self):
        response = self.fetch("/borea/uno")
        self.assertEqual(response.code, 200)
        response = self.fetch("/borea/due")
        self.assertEqual(response.code, 200)

        response = self.fetch("/borea/uno/remove")
        response = self.fetch("/borea")
        res = json.loads(response.body)
        self.assertEqual(len(res), 1)
        self.assertTrue("due" in res)
        self.assertTrue("uno" not in res)
        
        
        

if __name__ == '__main__':
    unittest.main()
