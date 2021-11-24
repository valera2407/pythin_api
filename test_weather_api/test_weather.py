import requests
import pytest
import xml.etree.ElementTree as ET


def check_name(resp):
    return resp['city']['name']


def something_with_mode(mode, resp, city_name):
    if mode.lower() == 'xml':
        response_xml = ET.fromstring(resp.text)
        check_city_name = response_xml.find('location').findtext('name')
        assert check_city_name == city_name
    elif mode.lower() == 'json':
        response = resp.json()
        assert check_name(response) == city_name
    else:
        print("You should use 'xml' or 'json' mode to we can validation city name")


@pytest.mark.positive
class TestCityName:
    data_city_name = ['London', 'Kharkiv', 'Rechtenstein']
    data_coordinate = [(46.655281, 35.151669, 'Volodymyrivka'),
                       (48.748379, 30.22184, 'Uman\''),
                       (54.339008, -1.43243, 'Northallerton')]
    data_city_id = [(2878234, 'Leverkusen'), (3105789, 'Vilecha'), (688157, 'Omelyaniv')]
    data_zip_code = [(35004, 'Moody'), (71601, 'Pine Bluff'), (90001, 'Los Angeles')]

    @pytest.mark.parametrize('city', data_city_name)
    def test_city_name(self, full_url, api_key, city):
        query = {'q': city, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city

    #    j = json.loads(resp.text)
    #    assert j['cnt'] == listSize

    @pytest.mark.parametrize('latitude, longitude, city', data_coordinate)
    def test_coordinates(self, full_url, api_key, latitude, longitude, city):
        query = {'lat': latitude, 'lon': longitude, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city

    @pytest.mark.parametrize('city_id, city_name', data_city_id)
    def test_city_id(self, full_url, api_key, city_id, city_name):
        query = {'id': city_id, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name

    @pytest.mark.parametrize('zip_code, city_name', data_zip_code)
    def test_zip_code(self, full_url, api_key, zip_code, city_name):
        query = {'zip': zip_code, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name


@pytest.mark.positive
class TestOtherParameters:
    data_count = [('Dedenevo', 15), ('New York', 24), ('Bryansk', 40)]
    data_language = [(2878234, 'Леверкузен', 'ru'), (2643743, 'Londyn', 'pl'), (703448, 'كييف', 'ar')]
    data_mode = [(2878234, 'Leverkusen', 'xml'), (2643743, 'London', 'json'), (703448, 'Kyiv', 'xml')]

    @pytest.mark.parametrize('city_id, city_name, language', data_language)
    def test_language(self, full_url, api_key, city_id, city_name, language):
        query = {'id': city_id, 'lang': language, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name

    @pytest.mark.parametrize('city_name, size', data_count)
    def test_count(self, full_url, api_key, city_name, size):
        query = {'q': city_name, 'cnt': size, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        response = resp.json()
        assert resp.status_code == 200
        assert check_name(response) == city_name
        assert response['cnt'] == size

    @pytest.mark.parametrize('city_id, city_name, mode_request', data_mode)
    def test_format_response(self, full_url, api_key, city_id, city_name, mode_request):
        query = {'id': city_id, 'mode': mode_request, 'APPID': api_key}
        resp = requests.get(url=full_url, params=query)
        something_with_mode(mode_request, resp, city_name)
        assert resp.status_code == 200
        assert mode_request in resp.headers['Content-Type']
