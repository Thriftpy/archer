# -*- coding: utf-8 -*-
from archer import TestClient


def test_test_client(app):
    test_client = TestClient(app)
    assert test_client.query(123) == 'id'
