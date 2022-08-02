
import json
import requests_mock

from http import HTTPStatus
from src.app import MemberStruct


def test_member_info_avg_ok(client):

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api1.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api2.com?member_id=1', json={'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api3.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        response = client.get('/members/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json.get(MemberStruct.DEDUCTIBLE.value) == 1067
    assert response.json.get(MemberStruct.STOP_LOSS.value) == 11000
    assert response.json.get(MemberStruct.OOPS_MAX.value) == 5667


def test_member_info_min_ok(client):

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api1.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api2.com?member_id=1', json={'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api3.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        response = client.get('/members/1/?aggregation_strategy=MIN')

    assert response.status_code == HTTPStatus.OK
    assert response.json.get(MemberStruct.DEDUCTIBLE.value) == 1000
    assert response.json.get(MemberStruct.STOP_LOSS.value) == 10000
    assert response.json.get(MemberStruct.OOPS_MAX.value) == 5000


def test_member_info_max_ok(client):

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api1.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api2.com?member_id=1', json={'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api3.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        response = client.get('/members/1/?aggregation_strategy=MAX')

    assert response.status_code == HTTPStatus.OK
    assert response.json.get(MemberStruct.DEDUCTIBLE.value) == 1200
    assert response.json.get(MemberStruct.STOP_LOSS.value) == 13000
    assert response.json.get(MemberStruct.OOPS_MAX.value) == 6000


def test_member_info_unknown_aggregation_strategy(client):

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api1.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api2.com?member_id=1', json={'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api3.com?member_id=1', json={'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        response = client.get('/members/1/?aggregation_strategy=MEDIAN')

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_member_info_all_external_apis_offline(client):

    response = client.get('/members/1/')
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_member_info_avg_single_api_online(client):

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api2.com?member_id=1', json={'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
                   status_code=HTTPStatus.OK)
        response = client.get('/members/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json.get(MemberStruct.DEDUCTIBLE.value) == 1200
    assert response.json.get(MemberStruct.STOP_LOSS.value) == 13000
    assert response.json.get(MemberStruct.OOPS_MAX.value) == 6000


def test_member_info_avg_and_zeroes(client):

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api1.com?member_id=1', json={'deductible': 0, 'stop_loss': 0, 'oop_max': 0},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api2.com?member_id=1', json={'deductible': 0, 'stop_loss': 0, 'oop_max': 0},
                   status_code=HTTPStatus.OK)
        mocker.get('https://api3.com?member_id=1', json={'deductible': 0, 'stop_loss': 0, 'oop_max': 0},
                   status_code=HTTPStatus.OK)
        response = client.get('/members/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json.get(MemberStruct.DEDUCTIBLE.value) == 0
    assert response.json.get(MemberStruct.STOP_LOSS.value) == 0
    assert response.json.get(MemberStruct.OOPS_MAX.value) == 0
