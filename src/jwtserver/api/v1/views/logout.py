from pydantic import BaseModel
from jwtserver.app import app
from fastapi import Response


class LogoutResponse(BaseModel):
    status: str


@app.get("/api/v1/auth/logout/", response_model=LogoutResponse, tags=["Authorization"],
         description="Delete access_token and refresh_token")
async def logout(response: Response):
    """If the exit, delete the token and that's it
    :param response: fastapi.Response
    :return LogoutResponse
    """
    response.delete_cookie(key='refresh_token')
    return {"status": 'logout'}
