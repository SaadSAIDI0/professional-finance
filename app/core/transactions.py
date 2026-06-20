from datetime import datetime

from app.core.database import Database


class TransactionService:
    """Transaction operations for one authenticated account."""

    CATEGORIES = ["salary", "food", "rent", "transport", "entertainment", "health", "education", "other"]
    TYPES = ["income", "expense"]

    def __init__(self, database: Database):
        self.database = database

    def add_transaction(
        self,
        account_id: int,
        amount: float,
        type_: str,
        category: str,
        note: str = "",
        date: str | None = None,
    ) -> int:
        self._validate_transaction(amount, type_, category)
        date = date or datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor = self.database.connection.execute(
            """
            INSERT INTO transactions (account_id, amount, type, category, note, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (account_id, float(amount), type_, category, note.strip(), date),
        )
        self.database.connection.commit()
        return int(cursor.lastrowid)

    def list_transactions(self, account_id: int):
        return self.database.connection.execute(
            """
            SELECT * FROM transactions
            WHERE account_id = ?
            ORDER BY id DESC
            """,
            (account_id,),
        ).fetchall()

    def delete_transaction(self, account_id: int, transaction_id: int):
        self.database.connection.execute(
            "DELETE FROM transactions WHERE id = ? AND account_id = ?",
            (transaction_id, account_id),
        )
        self.database.connection.commit()

    def summary(self, account_id: int) -> dict:
        rows = self.list_transactions(account_id)
        income = sum(row["amount"] for row in rows if row["type"] == "income")
        expense = sum(row["amount"] for row in rows if row["type"] == "expense")
        return {
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "count": len(rows),
        }

    def _validate_transaction(self, amount: float, type_: str, category: str):
        if float(amount) <= 0:
            raise ValueError("Amount must be greater than zero.")
        if type_ not in self.TYPES:
            raise ValueError("Transaction type must be income or expense.")
        if category not in self.CATEGORIES:
            raise ValueError("Invalid transaction category.")

