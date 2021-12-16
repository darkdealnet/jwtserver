from os import getenv
# import requests
import httpx
from urllib import parse
from .init_redis import redis
from loguru import logger
from random import randint
from jwtserver.functions.config import load_config

config = load_config().sms


def string_to_dict(text: str):
    return {
        k.strip(): v.strip()
        for k, v in [b.split(' - ', 1) for b in text.split(',')]
    }


class SMSCRULES:
    def __init__(self):

        self.url = "https://smsc.ru/sys/send.php?"

        self.param_url = {
            'login': config.login,
            'psw': config.password
        }
        self.call_code_redis_time = int(config.time_call)
        self.sms_code_redis_time = int(config.time_sms)

    async def call(self, telephone):
        param_url = {
            **self.param_url,
            **{
                'phones': telephone,
                'mes': 'code',
                'call': 1,
            }
        }
        if config.debug:
            code = '{:0>4d}'.format(randint(0, 9999))
        else:
            async with httpx.AsyncClient() as client:
                # resp = await client.get(self.url + parse.urlencode(param_url))
                resp: httpx.Response = await client.get(self.url, params=param_url)

                if resp.status_code == httpx.codes.OK:
                    text = resp.text
                    if "ERROR" in text:
                        return None, None, 'Wait1min'
                    data = string_to_dict(text)

                else:
                    return None, None, 'response status not 200 OK'

            code = data['CODE'][-4:]
        await redis.set(telephone, code, self.call_code_redis_time)
        logger.info(code)

        return code, self.call_code_redis_time - 1, None

    async def send_sms(self, telephone):
        code = '{:0>4d}'.format(randint(0, 9999))
        param_url = {
            **self.param_url,
            **{
                'phones': telephone,
                'mes': code,
            }
        }
        if config.debug:
            pass
        else:

            async with httpx.AsyncClient() as client:
                # resp = requests.get(self.url + parse.urlencode(param_url))
                resp: httpx.Response = await client.get(self.url, params=param_url)
                if resp.status_code == httpx.codes.OK:
                    text = resp.text
                    if "ERROR" in text:
                        return None, None, 'Wait1min'
                else:
                    return None, None, 'response status not 200 OK'

        await redis.set(telephone, code, self.sms_code_redis_time)
        logger.info(code)

        return code, self.sms_code_redis_time - 1, None
