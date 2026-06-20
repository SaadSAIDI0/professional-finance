import sqlite3
import re

from app.core.database import Database
from app.core.security import PasswordSecurity


class AccountService:
    """Account operations used by both tests and the PySide UI."""

    def __init__(self, database: Database, security: PasswordSecurity | None = None):
        self.database = database
        self.security = security or PasswordSecurity()

    def create_account(self, real_name: str, username: str, email: str, password: str) -> int:
        self._validate_account(real_name, username, email, password)
        password_hash = self.security.hash_password(password)
        cursor = self.database.connection.execute(
            """
            INSERT INTO accounts (real_name, username, email, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (real_name.strip(), username.strip(), email.strip(), password_hash),
        )
        self.database.connection.commit()
        return int(cursor.lastrowid)

    def login(self, username: str, password: str) -> dict | None:
        account = self.get_by_username(username)
        if account is None:
            return None
        if not self.security.verify_password(account["password_hash"], password):
            return None
        return dict(account)

    def get_by_username(self, username: str):
        return self.database.connection.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()

    def username_exists(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def _validate_account(self, real_name: str, username: str, email: str, password: str):
        if len(real_name.strip()) < 3:
            raise ValueError("Real name must contain at least 3 characters.")
        if len(username.strip()) < 4:
            raise ValueError("Username must contain at least 4 characters.")
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email.strip()):
            raise ValueError("Email must be a Gmail address from Google, for example name@gmail.com.")
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")

    def safe_create_account(self, real_name: str, username: str, email: str, password: str) -> tuple[bool, str]:
        try:
            self.create_account(real_name, username, email, password)
            return True, "Account created successfully."
        except sqlite3.IntegrityError:
            return False, "Username or email already exists."
        except ValueError as error:
            return False, str(error)
