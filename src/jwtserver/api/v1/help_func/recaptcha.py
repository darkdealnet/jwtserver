from loguru import logger
import httpx
from fastapi import HTTPException, Body
from starlette import status
from jwtserver.functions.config import load_config

config = load_config().google


class RecaptchaV3:
    def __init__(
            self,
            recaptcha_token: str = Body(...)
    ):
        self.action_name = None
        self.success = False
        self.action_valid = False
        self.r_json = None
        self.recaptcha_token = recaptcha_token

    def set_action_name(self, name):
        self.action_name = name
        return self

    async def greenlight(self):
        await self.post()
        if not self.r_json['success']:
            logger.critical("invalid reCAPTCHA token")
            return True

        if not self.r_json['action'] == self.action_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="hm... u r hacker?",
            )
        if self.r_json['score'] < 0.7:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="hm... u r bot?",
            )

        return True

    async def post(self):
        data = {
            'secret': config.secret_key,
            'response': self.recaptcha_token,
        }
        async with httpx.AsyncClient() as client:
            r: httpx.Response = await client.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            self.r_json = r.json()
        return self
