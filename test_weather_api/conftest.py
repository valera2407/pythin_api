
import pytest

@pytest.fixture(scope = 'session')
def base_url():
    return 'https://api.openweathermap.org'

@pytest.fixture(scope = 'session')
def full_url(base_url):
    return base_url + '/data/2.5/forecast'

@pytest.fixture()
def api_key():
    return 'b2ce5b9466a4cdcec5e7a6bf11465c5a'