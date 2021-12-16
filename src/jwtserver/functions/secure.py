from passlib.context import CryptContext
# import schemas

pwd_context = CryptContext(schemes=["sha256_crypt", "ldap_salted_md5"],
                           sha256_crypt__default_rounds=649342,
                           ldap_salted_md5__salt_size=16)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# async def authenticate_user(db, uuid: str, password: str):
#     user: schemas.UserFullPD = crud.get_user(db, uuid)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user


def get_password_hash(password):
    return pwd_context.hash(password)
