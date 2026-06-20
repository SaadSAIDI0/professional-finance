import pytest

from app.core.accounts import AccountService
from app.core.database import Database


@pytest.fixture
def account_service(tmp_path):
    database = Database(tmp_path / "test.db")
    return AccountService(database)


def test_create_account(account_service):
    account_id = account_service.create_account("Student Name", "student", "student@gmail.com", "password123")

    account = account_service.get_by_username("student")

    assert account_id == account["id"]
    assert account["real_name"] == "Student Name"
    assert account["username"] == "student"
    assert account["password_hash"] != "password123"


def test_login_success(account_service):
    account_service.create_account("Student Name", "student", "student@gmail.com", "password123")

    account = account_service.login("student", "password123")

    assert account is not None
    assert account["username"] == "student"


def test_login_fails_with_wrong_password(account_service):
    account_service.create_account("Student Name", "student", "student@gmail.com", "password123")

    account = account_service.login("student", "wrong-password")

    assert account is None


def test_create_account_validates_password(account_service):
    with pytest.raises(ValueError):
        account_service.create_account("Student Name", "student", "student@gmail.com", "short")


def test_create_account_requires_google_gmail(account_service):
    with pytest.raises(ValueError):
        account_service.create_account("Student Name", "student", "student@hotmail.com", "password123")
