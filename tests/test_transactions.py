import pytest

from app.core.database import Database
from app.core.transactions import TransactionService


@pytest.fixture
def transaction_service(tmp_path):
    database = Database(tmp_path / "test.db")
    return TransactionService(database)


@pytest.fixture
def account_id(tmp_path):
    """Create a test account and return its ID."""
    from app.core.accounts import AccountService
    
    database = Database(tmp_path / "test.db")
    account_service = AccountService(database)
    account_id = account_service.create_account(
        "Test User",
        "testuser",
        "testuser@gmail.com",
        "password123"
    )
    return account_id


def test_add_transaction(transaction_service, account_id):
    """Test adding a transaction."""
    transaction_id = transaction_service.add_transaction(
        account_id,
        1000.0,
        "income",
        "salary",
        "Monthly salary",
    )
    
    assert transaction_id > 0


def test_add_transaction_with_default_date(transaction_service, account_id):
    """Test that transactions get a default date if not provided."""
    transaction_id = transaction_service.add_transaction(
        account_id,
        500.0,
        "expense",
        "food",
    )
    
    rows = transaction_service.list_transactions(account_id)
    assert len(rows) == 1
    assert rows[0]["date"] is not None


def test_list_transactions(transaction_service, account_id):
    """Test listing transactions for an account."""
    transaction_service.add_transaction(account_id, 1000.0, "income", "salary")
    transaction_service.add_transaction(account_id, 200.0, "expense", "food")
    
    rows = transaction_service.list_transactions(account_id)
    
    assert len(rows) == 2


def test_list_transactions_empty(transaction_service, account_id):
    """Test listing transactions when there are none."""
    rows = transaction_service.list_transactions(account_id)
    
    assert len(rows) == 0


def test_delete_transaction(transaction_service, account_id):
    """Test deleting a transaction."""
    transaction_id = transaction_service.add_transaction(
        account_id,
        500.0,
        "expense",
        "food",
    )
    
    transaction_service.delete_transaction(account_id, transaction_id)
    rows = transaction_service.list_transactions(account_id)
    
    assert len(rows) == 0


def test_delete_transaction_wrong_account(transaction_service, account_id):
    """Test that transactions can only be deleted by the account owner."""
    transaction_id = transaction_service.add_transaction(
        account_id,
        500.0,
        "expense",
        "food",
    )
    
    # Try to delete with a different account ID
    transaction_service.delete_transaction(account_id + 1, transaction_id)
    rows = transaction_service.list_transactions(account_id)
    
    # Transaction should still exist
    assert len(rows) == 1


def test_summary_empty(transaction_service, account_id):
    """Test summary for account with no transactions."""
    summary = transaction_service.summary(account_id)
    
    assert summary["income"] == 0
    assert summary["expense"] == 0
    assert summary["balance"] == 0
    assert summary["count"] == 0


def test_summary_with_transactions(transaction_service, account_id):
    """Test summary calculation with multiple transactions."""
    transaction_service.add_transaction(account_id, 1000.0, "income", "salary")
    transaction_service.add_transaction(account_id, 200.0, "expense", "food")
    transaction_service.add_transaction(account_id, 150.0, "expense", "transport")
    
    summary = transaction_service.summary(account_id)
    
    assert summary["income"] == 1000.0
    assert summary["expense"] == 350.0
    assert summary["balance"] == 650.0
    assert summary["count"] == 3


def test_validate_transaction_zero_amount(transaction_service, account_id):
    """Test that zero amount transactions are rejected."""
    with pytest.raises(ValueError):
        transaction_service.add_transaction(
            account_id,
            0.0,
            "income",
            "salary",
        )


def test_validate_transaction_negative_amount(transaction_service, account_id):
    """Test that negative amount transactions are rejected."""
    with pytest.raises(ValueError):
        transaction_service.add_transaction(
            account_id,
            -100.0,
            "income",
            "salary",
        )


def test_validate_transaction_invalid_type(transaction_service, account_id):
    """Test that invalid transaction type is rejected."""
    with pytest.raises(ValueError):
        transaction_service.add_transaction(
            account_id,
            100.0,
            "transfer",
            "salary",
        )


def test_validate_transaction_invalid_category(transaction_service, account_id):
    """Test that invalid category is rejected."""
    with pytest.raises(ValueError):
        transaction_service.add_transaction(
            account_id,
            100.0,
            "income",
            "invalid_category",
        )


def test_transaction_types():
    """Test that transaction types are defined."""
    assert "income" in TransactionService.TYPES
    assert "expense" in TransactionService.TYPES


def test_transaction_categories():
    """Test that transaction categories are defined."""
    required_categories = ["salary", "food", "rent", "transport", "entertainment", "health", "education", "other"]
    for category in required_categories:
        assert category in TransactionService.CATEGORIES
