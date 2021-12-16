from fastapi.param_functions import Form


class SignInRequestForm:
    def __init__(
            self,
            uuid: str = Form(...),
            password: str = Form(...),
    ):
        self.uuid = uuid
        self.password = password
