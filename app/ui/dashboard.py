from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.core.transactions import TransactionService
from app.ui.styles import BLUE, GREEN, MUTED, RED, TEXT


class Dashboard(QWidget):
    logout_requested = Signal()

    def __init__(self, account: dict, transaction_service: TransactionService):
        super().__init__()
        self.setObjectName("dashboard")
        self.account = account
        self.transaction_service = transaction_service
        self.build()
        self.refresh()

    def build(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self.build_sidebar())

        self.pages = QStackedWidget()
        self.pages.setObjectName("contentPanel")
        self.dashboard_page = self.build_dashboard_page()
        self.settings_page = self.build_settings_page()
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.settings_page)

        root.addWidget(self.pages, 1)

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(22, 24, 22, 24)
        layout.setSpacing(12)

        brand = QHBoxLayout()
        brand.addWidget(self.build_logo())

        brand_text = QVBoxLayout()
        name = QLabel("Professional Finance")
        name.setStyleSheet(f"color: {TEXT}; font-size: 15px; font-weight: 900;")
        subtitle = QLabel("Money workspace")
        subtitle.setObjectName("muted")
        brand_text.addWidget(name)
        brand_text.addWidget(subtitle)
        brand.addLayout(brand_text)

        self.dashboard_button = self.nav_button("Dashboard", self.show_dashboard_page)
        self.settings_button = self.nav_button("Settings", self.show_settings_page)

        layout.addLayout(brand)
        layout.addSpacing(26)
        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.settings_button)
        layout.addStretch()
        layout.addWidget(self.build_account_card())

        logout = QPushButton("Logout")
        logout.setObjectName("dangerButton")
        logout.setCursor(Qt.PointingHandCursor)
        logout.clicked.connect(self.logout_requested.emit)
        layout.addWidget(logout)

        return sidebar

    def build_logo(self):
        logo_path = Path(__file__).resolve().parents[1] / "assets" / "logo.png"

        if logo_path.exists():
            logo = QLabel()
            logo.setFixedSize(44, 44)
            logo.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(str(logo_path)).scaled(38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            return logo

        badge = QFrame()
        badge.setObjectName("logoBadge")
        badge.setFixedSize(44, 44)
        badge_layout = QVBoxLayout(badge)
        badge_layout.setContentsMargins(0, 0, 0, 0)
        initials = QLabel("PF")
        initials.setAlignment(Qt.AlignCenter)
        initials.setStyleSheet("color: white; font-size: 15px; font-weight: 900;")
        badge_layout.addWidget(initials)
        return badge

    def nav_button(self, text: str, callback):
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(callback)
        return button

    def build_account_card(self):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        name = QLabel(self.account["real_name"])
        name.setStyleSheet(f"color: {TEXT}; font-size: 14px; font-weight: 800;")
        username = QLabel(f"@{self.account['username']}")
        username.setObjectName("muted")
        email = QLabel(self.account["email"])
        email.setObjectName("muted")
        email.setWordWrap(True)

        layout.addWidget(name)
        layout.addWidget(username)
        layout.addWidget(email)
        return card

    def build_dashboard_page(self):
        page = QWidget()
        page.setObjectName("contentPanel")
        root = QVBoxLayout(page)
        root.setContentsMargins(34, 28, 34, 28)
        root.setSpacing(22)

        header = QHBoxLayout()
        header_text = QVBoxLayout()
        title = QLabel(f"Welcome, {self.account['username']}")
        title.setObjectName("screenTitle")
        subtitle = QLabel("Your personal finance dashboard")
        subtitle.setObjectName("muted")
        header_text.addWidget(title)
        header_text.addWidget(subtitle)
        header.addLayout(header_text)
        header.addStretch()
        root.addLayout(header)

        metrics = QGridLayout()
        metrics.setSpacing(18)
        self.balance_card, self.balance_value = self.metric_card("Balance", "0.00 DH", BLUE)
        self.income_card, self.income_value = self.metric_card("Income", "0.00 DH", GREEN)
        self.expense_card, self.expense_value = self.metric_card("Expense", "0.00 DH", RED)
        metrics.addWidget(self.balance_card, 0, 0)
        metrics.addWidget(self.income_card, 0, 1)
        metrics.addWidget(self.expense_card, 0, 2)
        root.addLayout(metrics)

        content = QHBoxLayout()
        content.setSpacing(18)
        content.addWidget(self.build_transaction_form(), 1)
        content.addWidget(self.build_transaction_table(), 2)
        root.addLayout(content)
        return page

    def build_settings_page(self):
        page = QWidget()
        page.setObjectName("contentPanel")
        root = QVBoxLayout(page)
        root.setContentsMargins(34, 28, 34, 28)
        root.setSpacing(18)

        title = QLabel("Settings")
        title.setObjectName("screenTitle")
        subtitle = QLabel("Manage your account details and future preferences.")
        subtitle.setObjectName("muted")

        card = QFrame()
        card.setObjectName("card")
        grid = QGridLayout(card)
        grid.setContentsMargins(24, 22, 24, 22)
        grid.setHorizontalSpacing(34)
        grid.setVerticalSpacing(12)

        rows = [
            ("Real name", self.account["real_name"]),
            ("Username", self.account["username"]),
            ("Gmail", self.account["email"]),
            ("Password", "Protected with Argon2 hash"),
        ]
        for row_index, (label_text, value_text) in enumerate(rows):
            label = QLabel(label_text)
            label.setObjectName("muted")
            value = QLabel(value_text)
            value.setWordWrap(True)
            grid.addWidget(label, row_index, 0)
            grid.addWidget(value, row_index, 1)

        notice = QLabel("Editing profile data and changing passwords will be added after the transaction tools are complete.")
        notice.setObjectName("muted")
        notice.setWordWrap(True)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addWidget(card)
        root.addWidget(notice)
        root.addStretch()
        return page

    def show_dashboard_page(self):
        self.pages.setCurrentWidget(self.dashboard_page)

    def show_settings_page(self):
        self.pages.setCurrentWidget(self.settings_page)

    def metric_card(self, label_text: str, value_text: str, color: str):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 18, 22, 18)

        label = QLabel(label_text)
        label.setObjectName("muted")
        value = QLabel(value_text)
        value.setObjectName("metricValue")
        value.setStyleSheet(f"color: {color};")

        layout.addWidget(label)
        layout.addWidget(value)
        return card, value

    def build_transaction_form(self):
        frame = QFrame()
        frame.setObjectName("card")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QLabel("Add transaction")
        title.setObjectName("screenTitle")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.type_input = QComboBox()
        self.type_input.addItems(TransactionService.TYPES)
        self.category_input = QComboBox()
        self.category_input.addItems(TransactionService.CATEGORIES)
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Note (optional)")

        add_button = QPushButton("Add transaction")
        add_button.setObjectName("primaryButton")
        add_button.clicked.connect(self.add_transaction)

        layout.addWidget(title)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.type_input)
        layout.addWidget(self.category_input)
        layout.addWidget(self.note_input)
        layout.addWidget(add_button)
        layout.addStretch()
        return frame

    def build_transaction_table(self):
        frame = QFrame()
        frame.setObjectName("card")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)

        title = QLabel("Recent transactions")
        title.setObjectName("screenTitle")

        # Table now has 6 columns: Amount, Type, Category, Note, Date, and Action (Delete button)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Amount", "Type", "Category", "Note", "Date", "Action"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        layout.addWidget(title)
        layout.addWidget(self.table)
        return frame

    def add_transaction(self):
        amount_text = self.amount_input.text().strip()

        if not amount_text:
            QMessageBox.warning(self, "Validation Error", "Amount is required.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid number for the amount.")
            return

        try:
            self.transaction_service.add_transaction(
                self.account["id"],
                amount,
                self.type_input.currentText(),
                self.category_input.currentText(),
                self.note_input.text().strip(),
            )
        except ValueError as error:
            QMessageBox.warning(self, "Invalid transaction", str(error))
            return

        self.amount_input.clear()
        self.note_input.clear()
        self.refresh()

    def delete_transaction(self, row_index: int):
        """Delete a transaction from the table and database."""
        # Get transaction ID from row data
        transaction_id = self.table.item(row_index, 0).data(Qt.UserRole)
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this transaction?",
            QMessageBox.Yes | QMessageBox.No,
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.transaction_service.delete_transaction(self.account["id"], transaction_id)
                self.refresh()
                QMessageBox.information(self, "Success", "Transaction deleted successfully.")
            except Exception as error:
                QMessageBox.warning(self, "Error", f"Failed to delete transaction: {str(error)}")

    def format_currency(self, value: float) -> str:
        """Format a float value as currency with 2 decimal places."""
        return f"{value:.2f} DH"

    def refresh(self):
        summary = self.transaction_service.summary(self.account["id"])
        self.balance_value.setText(self.format_currency(summary["balance"]))
        self.income_value.setText(self.format_currency(summary["income"]))
        self.expense_value.setText(self.format_currency(summary["expense"]))

        rows = self.transaction_service.list_transactions(self.account["id"])
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            # Create cells for: Amount, Type, Category, Note, Date
            values = [
                self.format_currency(row["amount"]),
                row["type"],
                row["category"],
                row["note"],
                row["date"],
            ]
            
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                # Store transaction ID in the first column for deletion
                if column_index == 0:
                    item.setData(Qt.UserRole, row["id"])
                self.table.setItem(row_index, column_index, item)
            
            # Add Delete button in the Action column
            delete_button = QPushButton("Delete")
            delete_button.setObjectName("dangerButton")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.clicked.connect(lambda checked, r=row_index: self.delete_transaction(r))
            self.table.setCellWidget(row_index, 5, delete_button)
