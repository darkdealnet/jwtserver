import asyncio

import aioredis
import pytest
from starlette.testclient import TestClient
from jwtserver import app
from jwtserver.Google.Recaptcha_v3 import Recaptcha
from jwtserver.functions.init_redis import redis_conn
from jwtserver.functions.session_db import async_db_session
from jwtserver.tests.depends import override_async_db_session, override_redis_conn, \
    OverrideRecaptcha, redis

app.dependency_overrides[async_db_session] = override_async_db_session
app.dependency_overrides[redis_conn] = override_redis_conn
app.dependency_overrides[Recaptcha] = OverrideRecaptcha
pytestmark = pytest.mark.asyncio
client = TestClient(app)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
async def flushall():
    r = aioredis.from_url("redis://:@localhost:6380/1", decode_responses=True)
    await r.flushall()
    await r.close()


# registration_uuid = None
# registration_password = 'Qwerty123'
# registration_access_token = None
#
# fingerprint = 'RgAAOblb90zuv3OCtiPg'
# fingerprint_fake = 'qgBfOblb10zuv3OCtiPg'
#
telephone_for_test = '+71234567890'


# def check_refresh_token_cookie(cookies):
#     for cookie in cookies:
#         if cookie.name == 'refresh_token':
#             assert cookie.has_nonstandard_attr('HttpOnly')
#             expires = datetime.fromtimestamp(cookie.expires)
#             expires_fix = timedelta(minutes=1) + expires
#             delta_days = (expires_fix - datetime.now()).days
#             # assert delta_days == KEYS.REFRESH_TOKEN_EXPIRE_DAYS
#             return True
#     return False

def test_phone_status():
    data = {
        'telephone': telephone_for_test,
        'recaptcha_token': 'success:SignUpPage/PhoneStatus:0.8'
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = client.post(
        "/api/v1/phone_status/",
        headers=headers,
        json=data
    )
    assert response.status_code == 200, response.text
    assert response.headers['content-type'] == 'application/json'
    # assert response.headers['content-length'] == '64'
    assert response.json()['free']
    assert response.json()['telephone']
    assert not response.json()['sent']
    assert not response.json()['time']


def test_send_code():
    data = {
        "telephone": telephone_for_test,
    }
    headers = {"accept": "application/json"}
    response = client.post(
        "/api/v1/send_code/",
        headers=headers,
        json=data
    )
    assert response.status_code == 200, response.text
    # assert response.json()['status'] == 'send'
    # repeat_response = client.post(
    #     "api/v1/send_code/",
    #     headers=headers,
    #     data=data
    # )
    # assert repeat_response.status_code == 200, repeat_response.text
    # assert repeat_response.json()['detail'] == 'code is send'

#
# def test_check_code_valid():
#     data = {"telephone": telephone_for_test, "code": redis.get(telephone_for_test)}
#     headers = {"accept": "application/x-www-form-urlencoded"}
#     response = client.post(
#         "/api/v1/auth/check_code",
#         headers=headers,
#         data=data
#     )
#     assert response.status_code == 200
#     assert response.json()['status'] == 'valid'
#
#
# def test_check_code_fake():
#     """
#     Кидаем на существующий номер фейковый код
#     """
#     data = {"telephone": telephone_for_test, "code": "99999"}
#     headers = {"accept": "application/x-www-form-urlencoded"}
#     response = client.post(
#         "/api/v1/auth/check_code",
#         headers=headers,
#         data=data
#     )
#     assert response.status_code == 200
#     assert response.json()['status'] == 'not valid'
#
#
# def test_registration_user():
#     response = client.post(
#         "/api/v1/auth/registration_user",
#         data={
#             "telephone": telephone_for_test,
#             "password": registration_password,
#             "code": redis.get(telephone_for_test),
#             "fingerprint": fingerprint
#         }
#     )
#     response_json = response.json()
#     assert response.status_code == 200
#     assert 'password' not in response_json
#     assert response_json['token_type'] == 'bearer'
#     access_token = response_json['access_token']
#     payload = access_token.split('.', 2)[1] + "==="
#     payload_decoded = json.loads(base64.urlsafe_b64decode(payload))
#     assert 'uuid' and 'isActive' and 'exp' in payload_decoded
#     assert payload_decoded['isActive']
#     assert UUID(payload_decoded['uuid']).version == 4
#     global registration_uuid
#     registration_uuid = payload_decoded['uuid']
#     refresh_token = response.cookies['refresh_token']
#     global registration_access_token
#     registration_access_token = access_token
#     assert refresh_token
#     assert check_refresh_token_cookie(response.cookies)
#     refresh_token_data = redis.hgetall(refresh_token)
#     assert refresh_token_data['uuid']
#     assert refresh_token_data['refresh_token']
#     assert refresh_token_data['fingerprint']
#     assert refresh_token_data['expires_date']
#     assert refresh_token_data['create_date']
#     assert float(refresh_token_data['expires_date']) > datetime.now().timestamp()
#     assert float(refresh_token_data['create_date']) < datetime.now().timestamp()
#
#
# def test_registration_user_fake_code():
#     response = client.post(
#         "/api/v1/auth/registration_user",
#         headers={
#             "accept": "application/x-www-form-urlencoded"
#         },
#         data={
#             "telephone": telephone_for_test,
#             "password": registration_password,
#             "code": "1234",
#             "fingerprint": fingerprint_fake
#         }
#     )
#     response_json = response.json()
#     assert response.status_code == 400
#     assert response_json['detail'] == 'Fake user'
#
#
# def test_get_token():
#     response = client.post(
#         "/api/v1/auth/token",
#         headers={
#             "accept": "application/x-www-form-urlencoded"
#         },
#         data={
#             'uuid': registration_uuid,
#             'password': registration_password
#         }
#     )
#     resp_json = response.json()
#     assert 'access_token' and 'token_type' in resp_json
#     assert response.status_code == 200, response.text
#     payload = jwt.decode(resp_json['access_token'], KEYS.SECRET_KEY, algorithms=[KEYS.ALGORITHM])
#     assert "uuid" and "exp" in payload
#     assert payload['uuid'] == registration_uuid, payload
#     assert type(payload['exp']) == float, payload['exp']
#     assert resp_json
#
#
# def test_get_token_for_fake_password():
#     data_copy = data_fake_auth.copy()
#     data_copy.update({'uuid': 'abdula'})
#     response = client.post(
#         "/api/v1/auth/token",
#         headers={
#             "accept": "application/x-www-form-urlencoded"
#         },
#         data=data_copy
#     )
#
#     assert response.status_code == 401, response.text
#     assert response.json()['detail'] == 'Incorrect uuid or password'
#
#
# def test_get_token_for_fake_user():
#     data_copy = data_fake_auth.copy()
#     data_copy.update({'password': '2131'})
#     response = client.post(
#         "/api/v1/auth/token",
#         headers={
#             "accept": "application/x-www-form-urlencoded"
#         },
#         data=data_copy
#     )
#
#     assert response.status_code == 401, response.text
#     assert response.json()['detail'] == 'Incorrect uuid or password'
#
#
# def client_post_refresh_token(**kwargs):
#     return client.post(
#         "/api/v1/auth/refresh_token",
#         data={"access_token": registration_access_token, "fingerprint": fingerprint},
#         **kwargs
#     )
#
#
# def test_new_refresh_token():
#     response = client_post_refresh_token()
#     assert response.status_code == 200, response.text
#     assert "access_token" and "token_type" in response.json()
#     assert check_refresh_token_cookie(response.cookies)
#     assert len(response.json()['access_token'].split('.')) == 3
#     assert response.json()['token_type'] == 'bearer'
#
#     global registration_access_token
#     registration_access_token = response.json()['access_token']
#
#
# def test_repeat_new_refresh_token():
#     response = client_post_refresh_token()
#     assert response.json()['access_token'] != registration_access_token
#     assert response.status_code == 200, response.text
#     assert "access_token" and "token_type" in response.json()
#     assert check_refresh_token_cookie(response.cookies)
#     assert len(response.json()['access_token'].split('.')) == 3
#     assert response.json()['token_type'] == 'bearer'
#
#
# def test_new_refresh_token__old_is_none():
#     client.cookies.clear()
#     response = client_post_refresh_token()
#     assert response.status_code == 422, response.text
#     response_json = response.json()
#     assert response_json['detail']
#
#
# def test_new_refresh_token__old_is_fake():
#     response = client_post_refresh_token(cookies={"refresh_token": "fake_token"})
#     assert response.status_code == 400, response.text
#     response_json = response.json()
#     assert response_json['detail']
