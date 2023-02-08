"""Test request module"""
import requests
import pytest
from request_module import Req


def test_login():
    url = 'https://x44.emaint.com/wc.dll?X3~dologin~&loc=en&languageid=en'
    if url is None:
        pytest.skip("URL is not set, skipping functional tests")
    session = requests.Session()
    if url.startswith("https://"):
        session.verify = False

    request = requests.Request('GET', url)
    prepared_request = session.prepare_request(request)

    response = session.send(prepared_request)

    assert response.status_code == 200
