import requests
import pytest


def check_name(resp):
    return resp['city']['name']

@pytest.mark.xfail()
@pytest.mark.negative
class TestNegativeXFail:

    data_zip_code = [(3004, 'Moody'), (7101, 'Pine Bluff'), (9001, 'Los Angeles')]
    data_city_name = ['Lndon', 'Khariv', 'Rechtestein']
    data_coordinate = [(105, 9416, 'Volodymyrivka'),
                       (111, 87, 'Uman\''),
                       (5, 1.43243, 'Northallerton')]
    data_city_id = [(2879234, 'Leverkusen'), (3205789, 'Vilecha'), (788157, 'Omelyaniv')]

    @pytest.mark.parametrize('city', data_city_name)
    def test_invalid_city_name(self, full_url, api_key, city):
        query = {'q': city, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city

    @pytest.mark.parametrize('latitude, longitude, city', data_coordinate)
    def test_invalid_coordinates(self, full_url, api_key, latitude, longitude, city):
        query = {'lat': latitude, 'lon': longitude, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city

    @pytest.mark.parametrize('city_id, city_name', data_city_id)
    def test_invalid_city_id(self, full_url, api_key, city_id, city_name):
        query = {'id': city_id, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name

    @pytest.mark.parametrize('zip_code, city_name', data_zip_code)
    def test_invalid_zip_code(self, full_url, api_key, zip_code, city_name):
        query = {'zip': zip_code, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name

    @pytest.mark.parametrize('zip_code, city_name', data_zip_code)
    def test_invalid_api_key(self, full_url, zip_code, city_name):
        query = {'zip': zip_code, 'APPID': 'nsnuignaseoij124u'}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name


@pytest.mark.negative
class TestNegative:
    data_zip_code = [3004, 7101, 9001]
    data_city_name = ['Lndon', 'Khariv', 'Rechtestein']
    data_coordinate = [(105, 9416),
                       (111, 87),
                       (5, 981)]
    data_city_id = [2879234, 3205789, 788157]

    @pytest.mark.skip('Skipped just to try')
    @pytest.mark.parametrize('city', data_city_name)
    def test_invalid_city_name(self, full_url, api_key, city):
        query = {'q': city, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 404
        assert response['message'] == 'city not found'

    @pytest.mark.parametrize('latitude, longitude', data_coordinate)
    def test_invalid_coordinates(self, full_url, api_key, latitude, longitude):
        query = {'lat': latitude, 'lon': longitude, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 400
        assert response['message'] == 'wrong latitude' or 'wrong longitude'

    @pytest.mark.parametrize('city_id', data_city_id)
    def test_invalid_city_id(self, full_url, api_key, city_id):
        query = {'id': city_id, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 404
        assert response['message'] == 'city not found'

    @pytest.mark.parametrize('zip_code', data_zip_code)
    def test_invalid_zip_code(self, full_url, api_key, zip_code):
        query = {'zip': zip_code, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 404
        assert response['message'] == 'city not found'

    @pytest.mark.parametrize('zip_code', data_zip_code)
    def test_invalid_api_key(self, full_url, zip_code):
        query = {'zip': zip_code, 'APPID': 'yurtihnuishnui214'}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 401
        assert 'Invalid API key' in response['message']
