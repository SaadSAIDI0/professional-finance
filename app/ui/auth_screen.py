from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget

from app.core.accounts import AccountService
from app.ui.styles import BLUE, GREEN, MUTED, RED, TEXT


class AuthScreen(QWidget):
    login_successful = Signal(dict)

    def __init__(self, account_service: AccountService):
        super().__init__()
        self.account_service = account_service
        self.mode = "login"
        self.build()

    def build(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.left_panel = QFrame()
        self.left_panel.setObjectName("sidePanel")
        self.right_panel = QFrame()
        self.right_panel.setObjectName("authPanel")

        root.addWidget(self.left_panel, 3)
        root.addWidget(self.right_panel, 2)

        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        layout = QVBoxLayout(self.left_panel)
        layout.setContentsMargins(70, 72, 70, 72)
        layout.setSpacing(22)

        title = QLabel("Take control\nof your money")
        title.setObjectName("heroTitle")

        subtitle = QLabel("A secure finance workspace for tracking income, expenses, and balance.")
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(430, 230)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 26, 28, 26)

        card_label = QLabel("Total Balance")
        card_label.setObjectName("muted")
        card_value = QLabel("7,800 DH")
        card_value.setObjectName("metricValue")

        row = QHBoxLayout()
        income = QLabel("+ 12,000 DH\nIncome")
        income.setStyleSheet(f"color: {GREEN}; font-size: 14px; font-weight: 700;")
        expense = QLabel("- 4,200 DH\nExpense")
        expense.setStyleSheet(f"color: {RED}; font-size: 14px; font-weight: 700;")
        expense.setAlignment(Qt.AlignRight)
        row.addWidget(income)
        row.addStretch()
        row.addWidget(expense)

        card_layout.addWidget(card_label)
        card_layout.addWidget(card_value)
        card_layout.addStretch()
        card_layout.addLayout(row)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(card)
        layout.addSpacing(22)
        quote = QLabel('"Simple, secure, and focused on your money habits."')
        quote.setObjectName("muted")
        quote.setWordWrap(True)
        layout.addWidget(quote)
        layout.addStretch()

    def build_right_panel(self):
        self.form_layout = QVBoxLayout(self.right_panel)
        self.form_layout.setContentsMargins(64, 70, 64, 70)
        self.form_layout.setSpacing(14)
        self.show_login_form()

    def clear_form(self):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_login_form(self):
        self.mode = "login"
        self.clear_form()
        self.form_layout.addStretch()

        title = QLabel("Sign in")
        title.setObjectName("screenTitle")
        subtitle = QLabel("Welcome back. Enter your account details.")
        subtitle.setObjectName("muted")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        options_row = QHBoxLayout()
        remember = QCheckBox("Remember me")
        forgot = QPushButton("Forgot password?")
        forgot.setObjectName("textButton")
        forgot.setCursor(Qt.PointingHandCursor)
        options_row.addWidget(remember)
        options_row.addStretch()
        options_row.addWidget(forgot)

        login_button = QPushButton("Login")
        login_button.setObjectName("primaryButton")
        login_button.clicked.connect(self.login)

        switch_button = QPushButton("Create an account")
        switch_button.setObjectName("textButton")
        switch_button.clicked.connect(self.show_signup_form)

        self.form_layout.addWidget(title)
        self.form_layout.addWidget(subtitle)
        self.form_layout.addSpacing(18)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_input)
        self.form_layout.addLayout(options_row)
        self.form_layout.addWidget(login_button)
        self.form_layout.addWidget(switch_button)
        self.form_layout.addStretch()

    def show_signup_form(self):
        self.mode = "signup"
        self.clear_form()
        self.form_layout.addStretch()

        title = QLabel("Create account")
        title.setObjectName("screenTitle")
        subtitle = QLabel("Use a Google Gmail address to create your local finance account.")
        subtitle.setObjectName("muted")

        self.real_name_input = QLineEdit()
        self.real_name_input.setPlaceholderText("Real name")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Gmail address")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password (min. 8 characters)")
        self.password_input.setEchoMode(QLineEdit.Password)

        password_hint = QLabel("Password must be at least 8 characters")
        password_hint.setObjectName("muted")
        password_hint.setStyleSheet(f"color: {MUTED}; font-size: 12px;")

        signup_button = QPushButton("Create account")
        signup_button.setObjectName("primaryButton")
        signup_button.clicked.connect(self.signup)

        switch_button = QPushButton("Already have an account? Sign in")
        switch_button.setObjectName("textButton")
        switch_button.clicked.connect(self.show_login_form)

        self.form_layout.addWidget(title)
        self.form_layout.addWidget(subtitle)
        self.form_layout.addSpacing(18)
        self.form_layout.addWidget(self.real_name_input)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.email_input)
        self.form_layout.addWidget(self.password_input)
        self.form_layout.addWidget(password_hint)
        self.form_layout.addWidget(signup_button)
        self.form_layout.addWidget(switch_button)
        self.form_layout.addStretch()

    def create_divider(self, text: str):
        row = QHBoxLayout()
        left = QFrame()
        left.setObjectName("dividerLine")
        left.setFixedHeight(1)
        label = QLabel(text)
        label.setObjectName("muted")
        right = QFrame()
        right.setObjectName("dividerLine")
        right.setFixedHeight(1)
        row.addWidget(left)
        row.addWidget(label)
        row.addWidget(right)
        return row

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter both username and password.")
            return

        account = self.account_service.login(username, password)
        if not account:
            QMessageBox.warning(self, "Login failed", "Invalid username or password.")
            return
        self.login_successful.emit(account)

    def signup(self):
        real_name = self.real_name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not real_name or not username or not email or not password:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields.")
            return

        ok, message = self.account_service.safe_create_account(real_name, username, email, password)
        if not ok:
            QMessageBox.warning(self, "Account error", message)
            return
        account = self.account_service.login(username, password)
        if account:
            self.login_successful.emit(account)
