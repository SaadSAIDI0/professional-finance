from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordSecurity:
    """Small wrapper around Argon2 password hashing.

    A wrapper keeps the rest of the app independent from the exact security
    library. If we ever change password settings, only this file needs to know.
    """

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty.")
        return self._hasher.hash(password)

    def verify_password(self, password_hash: str, password: str) -> bool:
        try:
            return self._hasher.verify(password_hash, password)
        except VerifyMismatchError:
            return False

