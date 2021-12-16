from jwtserver.app import app
from fastapi import Response


@app.get("/api/v1/auth/logout/")
async def logout(
        response: Response,
):
    response.delete_cookie(
        key='refresh_token',
    )
    return {"status": 'logout'}
