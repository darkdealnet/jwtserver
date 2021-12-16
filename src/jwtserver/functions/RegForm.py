from fastapi.param_functions import Form
from functions.telephone_validate import telephone_validate
from functions.init_redis import redis
from fastapi import HTTPException


def code_validation(code, telephone):
    value = redis.get(telephone)
    code_in_redis = value if value else None
    if code != code_in_redis:
        raise HTTPException(status_code=400, detail="Fake user")
    return code


class RegRequestForm:
    def __init__(
            self,
            telephone: str = Form(...),
            password: str = Form(...),
            fingerprint: str = Form(...),
            code: str = Form(...),
    ):
        self.telephone = telephone_validate(telephone)
        self.password = password
        self.fingerprint = fingerprint
        self.code = code
        self.code_is_valid = code_validation(self.code, self.telephone)
