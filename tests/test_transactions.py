import pytest

from app.core.accounts import AccountService
from app.core.database import Database
from app.core.transactions import TransactionService


@pytest.fixture
def services(tmp_path):
    database = Database(tmp_path / "test.db")
    accounts = AccountService(database)
    transactions = TransactionService(database)
    account_id = accounts.create_account("Student Name", "student", "student@gmail.com", "password123")
    return account_id, transactions


def test_add_and_list_transactions(services):
    account_id, transactions = services

    transactions.add_transaction(account_id, 1000, "income", "salary", "monthly income", "2026-06-19")
    rows = transactions.list_transactions(account_id)

    assert len(rows) == 1
    assert rows[0]["amount"] == 1000
    assert rows[0]["type"] == "income"
    assert rows[0]["category"] == "salary"


def test_summary(services):
    account_id, transactions = services

    transactions.add_transaction(account_id, 1000, "income", "salary")
    transactions.add_transaction(account_id, 250, "expense", "food")
    summary = transactions.summary(account_id)

    assert summary["income"] == 1000
    assert summary["expense"] == 250
    assert summary["balance"] == 750
    assert summary["count"] == 2


def test_delete_transaction(services):
    account_id, transactions = services

    transaction_id = transactions.add_transaction(account_id, 1000, "income", "salary")
    transactions.delete_transaction(account_id, transaction_id)

    assert transactions.list_transactions(account_id) == []


def test_invalid_amount_is_rejected(services):
    account_id, transactions = services

    with pytest.raises(ValueError):
        transactions.add_transaction(account_id, 0, "income", "salary")
