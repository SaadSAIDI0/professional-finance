import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QStackedWidget

from app.core.accounts import AccountService
from app.core.database import Database
from app.core.transactions import TransactionService
from app.ui.auth_screen import AuthScreen
from app.ui.dashboard import Dashboard
from app.ui.styles import APP_STYLESHEET


class FinanceApplication(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Finance")
        self.resize(1100, 680)
        self.setMinimumSize(980, 620)
        self.setStyleSheet(APP_STYLESHEET)

        database_path = Path(__file__).resolve().parents[1] / "data" / "finance.db"
        self.database = Database(database_path)
        self.account_service = AccountService(self.database)
        self.transaction_service = TransactionService(self.database)

        self.auth_screen = AuthScreen(self.account_service)
        self.auth_screen.login_successful.connect(self.show_dashboard)
        self.addWidget(self.auth_screen)

        self.screen_bool = True

    def show_dashboard(self, account: dict):
        dashboard = Dashboard(account, self.transaction_service)
        dashboard.logout_requested.connect(self.show_auth)
        self.addWidget(dashboard)
        self.setCurrentWidget(dashboard)
        self.screen_bool = False

    def show_auth(self):
        
        self.setCurrentWidget(self.auth_screen)


def main():
    app = QApplication(sys.argv)
    window = FinanceApplication()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
