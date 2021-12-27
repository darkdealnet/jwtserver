from loguru import logger
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from starlette import status
from jwtserver.api.v1.help_func.ParseToken import TokenProcessor
from jwtserver.Google.Recaptcha_v3 import Recaptcha
from jwtserver.app import app
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Response, HTTPException, Body
from jwtserver.functions.secure import verify_password
from jwtserver.functions.session_db import async_db_session
from jwtserver.models import User
from jwtserver.functions.config import load_config

token_config = load_config().token


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


@app.post("/api/v1/auth/login/", response_model=LoginResponse)
async def login(
        response: Response,
        recaptcha: Recaptcha = Depends(Recaptcha),
        session: AsyncSession = Depends(async_db_session),
        telephone: str = Body(...),
        password: str = Body(...),
):
    """ docs http://127.0.0.1:8000/ru/api_v1/#_1
    :param [Response] response: fastapi response
    :param [recaptcha_v3.md] recaptcha: Depends jwtserver.Google.Recaptcha_v3
        https://jwtserver.darkdeal.net/Recaptcha/
    :param [AsyncSession] session: Depends jwtserver.functions.session_db
        https://jwtserver.darkdeal.net/Database/#asyncsession-class
    :param str telephone: request Body(...)
    :param str password: request Body(...)
    :raises HTTPException: recaptcha_v3.md all raises
    :raises HTTPException: If there is no user
    :return dict: LoginResponse
    """
    logger.debug(telephone, password)
    await recaptcha.set_action_name('LoginPage/LoginButton').greenlight()
    stmt = select(User).where(User.telephone == telephone)
    result = await session.execute(stmt)
    try:
        user = result.scalars().one()
        logger.debug(user)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный номер или пароль",
            headers={"WWW-Authenticate": "JSv1"},
        )

    if verify_password(password, user.password):
        token_processor = TokenProcessor()
        logger.debug(token_processor)
        access_token, refresh_token = token_processor.create_pair_tokens(user.uuid.hex)
        logger.debug(access_token, refresh_token)
        logger.debug(access_token, refresh_token)
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            max_age=token_config.refresh_expire_time * 60)

        logger.debug({"access_token": access_token, "token_type": "JSv1"})
        return {"access_token": access_token, "token_type": "JSv1"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный номер или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
