from typing import Literal

from loguru import logger
import httpx
from fastapi import HTTPException, Body
from starlette import status
from jwtserver.functions.config import load_config

config = load_config().recaptcha_v3


class Recaptcha:
    """Recaptcha.md v3
    :raises HTTPException:
    https://www.google.com/recaptcha/admin/create"""

    def __init__(
            self,
            recaptcha_token: str = Body(...)
    ):
        self.action_name = None
        self.success = False
        self.action_valid = False
        self.r_json = None
        self.recaptcha_token = recaptcha_token

    def set_action_name(self, name) -> 'Recaptcha.md':
        """Set google action name"""
        self.action_name = name
        return self

    async def greenlight(self) -> Literal[True]:
        """If the recaptcha is ok, then the light is green.
        our minimum checks
        :return: True or raise HTTPException
        """

        def bad_request(detail: str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            )

        await self.check()
        if not self.r_json['success']:
            logger.critical("invalid reCAPTCHA token")

            bad_request('server error: invalid reCAPTCHA token for your site')

        if not self.r_json['action'] == self.action_name:
            bad_request('hm... u r hacker?')

        if self.r_json['score'] <= config.score:
            bad_request('hm... u r bot?')

        return True

    async def check(self) -> 'Recaptcha.md':
        """send post and save response json to self.r_json"""
        data = {
            'secret': config.secret_key,
            'response': self.recaptcha_token,
        }
        async with httpx.AsyncClient() as client:
            r: httpx.Response = await client.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            self.r_json = r.json()
        return self
