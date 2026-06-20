# Professional Finance App

This is a study project for building a professional personal finance desktop app with Python.

The project is intentionally organized like a real application instead of a single script. The goal is to practice clean architecture, database logic, password security, testing, and a polished PySide6 interface.

## What The App Does

- Create an account
- Securely hash passwords with Argon2
- Log in with username and password
- Require Gmail addresses for accounts
- Add income and expense transactions
- Show balance, total income, and total expense
- Show an account bar and settings panel
- Support a custom logo in `app/assets/logo.png`
- Display recent transactions in a desktop UI
- Test the core logic with pytest

## Tech Stack

- Python
- SQLite for local data storage
- PySide6 for the desktop interface
- argon2-cffi for password hashing
- pytest for automated testing

## Why Argon2?

Passwords must never be stored as plain text. This project uses Argon2 through `argon2-cffi`, because Argon2 is a modern memory-hard password hashing algorithm. That means it is designed to make password cracking harder than simple hashes like SHA-256.

## Project Structure

```text
professional_finance/
  app/
    main.py
    core/
      accounts.py
      database.py
      security.py
      transactions.py
    ui/
      auth_screen.py
      dashboard.py
      styles.py
  tests/
    test_accounts.py
    test_security.py
    test_transactions.py
  requirements.txt
  README.md
```

## Important Ideas For Learners

The app is split into two big parts:

1. Core logic

This is the part that manages data, accounts, password hashing, and transactions. It should not know anything about buttons or windows.

2. User interface

This is the part that displays screens and receives user input. It calls the core logic instead of doing database work itself.

This separation makes the project easier to test, debug, and improve.

## Install

```bash
cd professional_finance
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run The App

```bash
python -m app.main
```

## Run Tests

```bash
pytest
```

## Add A Logo

Put a PNG logo here:

```text
app/assets/logo.png
```

The dashboard will automatically use it. If the file is missing, the app shows a simple `PF` badge.

Recommended size:

```text
512x512 PNG
```

## About Real Gmail Verification

The app currently checks that the email ends with `@gmail.com`. This is format validation only.

A real Gmail verification system means:

1. The user enters a Gmail address.
2. The app generates a random 6-digit code.
3. The app sends that code to the Gmail address.
4. The user types the code in the app.
5. The app creates the account only if the code is correct.

To send email from a Gmail account, do not use your normal Gmail password. Use a Google App Password:

1. Enable 2-Step Verification on your Google account.
2. Go to Google Account security settings.
3. Create an App Password for mail.
4. Store it in environment variables, not in code.

Example environment variables:

```text
GMAIL_ADDRESS=youraddress@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

This project does not hard-code Gmail credentials because that would be unsafe. A professional app never stores private email passwords inside source code.

## Learning Roadmap

First, understand `app/core/security.py`. It teaches why password hashing is needed.

Second, understand `app/core/accounts.py`. It teaches how account data is saved and checked.

Third, understand `app/core/transactions.py`. It teaches how user-specific finance data is stored.

Fourth, understand the UI files. They show how PySide6 screens call the backend.

## Next Improvements

- Edit and delete transactions from the UI
- Add date filters
- Add category filters
- Add charts
- Add CSV export
- Add account settings
- Add better form validation
- Package the app as an executable
