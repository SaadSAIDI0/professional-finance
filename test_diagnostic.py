# Professional Finance App - Test Runner & Diagnostic Script
# This script tests all critical functionality

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("PROFESSIONAL FINANCE APP - DIAGNOSTIC TEST SUITE")
print("=" * 70)
print()

# ============================================================================
# TEST 1: Check Python environment and imports
# ============================================================================
print("TEST 1: Checking Python environment and imports...")
print("-" * 70)

try:
    import PySide6
    print("✅ PySide6 imported successfully")
except ImportError as e:
    print(f"❌ PySide6 import failed: {e}")
    sys.exit(1)

try:
    import argon2
    print("✅ argon2 imported successfully")
except ImportError as e:
    print(f"❌ argon2 import failed: {e}")
    sys.exit(1)

try:
    import pytest
    print("✅ pytest imported successfully")
except ImportError as e:
    print(f"❌ pytest import failed: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 2: Check core modules
# ============================================================================
print("TEST 2: Checking core application modules...")
print("-" * 70)

try:
    from app.core.security import PasswordSecurity
    print("✅ PasswordSecurity module loaded")
except ImportError as e:
    print(f"❌ PasswordSecurity import failed: {e}")
    sys.exit(1)

try:
    from app.core.database import Database
    print("✅ Database module loaded")
except ImportError as e:
    print(f"❌ Database import failed: {e}")
    sys.exit(1)

try:
    from app.core.accounts import AccountService
    print("✅ AccountService module loaded")
except ImportError as e:
    print(f"❌ AccountService import failed: {e}")
    sys.exit(1)

try:
    from app.core.transactions import TransactionService
    print("✅ TransactionService module loaded")
except ImportError as e:
    print(f"❌ TransactionService import failed: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 3: Check UI modules
# ============================================================================
print("TEST 3: Checking UI modules...")
print("-" * 70)

try:
    from app.ui.auth_screen import AuthScreen
    print("✅ AuthScreen module loaded")
except ImportError as e:
    print(f"❌ AuthScreen import failed: {e}")
    sys.exit(1)

try:
    from app.ui.dashboard import Dashboard
    print("✅ Dashboard module loaded")
except ImportError as e:
    print(f"❌ Dashboard import failed: {e}")
    sys.exit(1)

try:
    from app.ui.styles import APP_STYLESHEET
    print("✅ Styles module loaded")
except ImportError as e:
    print(f"❌ Styles import failed: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 4: Test Password Security
# ============================================================================
print("TEST 4: Testing Password Security...")
print("-" * 70)

try:
    security = PasswordSecurity()
    
    # Test password hashing
    password = "TestPassword123!"
    hashed = security.hash_password(password)
    
    assert hashed != password, "Password should be hashed, not stored as plain text"
    print("✅ Password hashing works correctly")
    
    # Test password verification - success
    is_valid = security.verify_password(hashed, password)
    assert is_valid is True, "Password verification should succeed with correct password"
    print("✅ Password verification (correct) works")
    
    # Test password verification - failure
    is_invalid = security.verify_password(hashed, "WrongPassword")
    assert is_invalid is False, "Password verification should fail with wrong password"
    print("✅ Password verification (incorrect) works")
    
    # Test empty password
    try:
        security.hash_password("")
        print("❌ Empty password should raise ValueError")
        sys.exit(1)
    except ValueError:
        print("✅ Empty password validation works")
    
except Exception as e:
    print(f"❌ Password security test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# ============================================================================
# TEST 5: Test Account Service
# ============================================================================
print("TEST 5: Testing Account Service...")
print("-" * 70)

try:
    import tempfile
    from pathlib import Path
    
    # Create temporary database
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test.db"
        database = Database(db_path)
        account_service = AccountService(database)
        
        # Test account creation
        account_id = account_service.create_account(
            "Test User",
            "testuser",
            "testuser@gmail.com",
            "password123"
        )
        assert account_id > 0, "Account ID should be positive"
        print("✅ Account creation works")
        
        # Test account retrieval
        account = account_service.get_by_username("testuser")
        assert account is not None, "Account should be retrievable"
        assert account["real_name"] == "Test User"
        print("✅ Account retrieval works")
        
        # Test login success
        login_result = account_service.login("testuser", "password123")
        assert login_result is not None, "Login should succeed with correct credentials"
        print("✅ Login (success) works")
        
        # Test login failure
        login_fail = account_service.login("testuser", "wrongpassword")
        assert login_fail is None, "Login should fail with wrong password"
        print("✅ Login (failure) works")
        
        # Test validation - invalid email
        try:
            account_service.create_account(
                "Another User",
                "anotheruser",
                "notgmail@hotmail.com",
                "password123"
            )
            print("❌ Should reject non-Gmail addresses")
            sys.exit(1)
        except ValueError:
            print("✅ Email validation works")
        
except Exception as e:
    print(f"❌ Account service test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# ============================================================================
# TEST 6: Test Transaction Service
# ============================================================================
print("TEST 6: Testing Transaction Service...")
print("-" * 70)

try:
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test.db"
        database = Database(db_path)
        account_service = AccountService(database)
        transaction_service = TransactionService(database)
        
        # Create test account
        account_id = account_service.create_account(
            "Test User",
            "testuser",
            "testuser@gmail.com",
            "password123"
        )
        
        # Test transaction creation
        tx_id = transaction_service.add_transaction(
            account_id,
            1000.0,
            "income",
            "salary",
            "Monthly salary"
        )
        assert tx_id > 0, "Transaction ID should be positive"
        print("✅ Transaction creation works")
        
        # Test transaction retrieval
        transactions = transaction_service.list_transactions(account_id)
        assert len(transactions) == 1, "Should have 1 transaction"
        print("✅ Transaction retrieval works")
        
        # Test summary
        summary = transaction_service.summary(account_id)
        assert summary["income"] == 1000.0, "Income should be 1000.0"
        assert summary["balance"] == 1000.0, "Balance should equal income"
        print("✅ Transaction summary works")
        
        # Add expense
        transaction_service.add_transaction(
            account_id,
            200.0,
            "expense",
            "food",
            "Groceries"
        )
        
        # Test updated summary
        summary = transaction_service.summary(account_id)
        assert summary["expense"] == 200.0, "Expense should be 200.0"
        assert summary["balance"] == 800.0, "Balance should be 800.0"
        print("✅ Transaction summary (updated) works")
        
        # Test deletion
        transaction_service.delete_transaction(account_id, tx_id)
        transactions = transaction_service.list_transactions(account_id)
        assert len(transactions) == 1, "Should have 1 transaction left"
        print("✅ Transaction deletion works")
        
        # Test validation - negative amount
        try:
            transaction_service.add_transaction(
                account_id,
                -100.0,
                "expense",
                "food"
            )
            print("❌ Should reject negative amounts")
            sys.exit(1)
        except ValueError:
            print("✅ Amount validation works")
        
except Exception as e:
    print(f"❌ Transaction service test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# ============================================================================
# TEST 7: Check Dashboard delete functionality
# ============================================================================
print("TEST 7: Checking Dashboard delete functionality...")
print("-" * 70)

try:
    from app.ui.dashboard import Dashboard
    import inspect
    
    # Check if delete_transaction method exists
    if hasattr(Dashboard, 'delete_transaction'):
        print("✅ delete_transaction method exists in Dashboard")
        
        # Check method signature
        sig = inspect.signature(Dashboard.delete_transaction)
        params = list(sig.parameters.keys())
        assert 'self' in params and 'row_index' in params, "Method should have row_index parameter"
        print("✅ delete_transaction method has correct signature")
    else:
        print("❌ delete_transaction method not found in Dashboard")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Dashboard test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 70)
print("✅ ALL DIAGNOSTIC TESTS PASSED!")
print("=" * 70)
print()
print("Summary:")
print("  ✅ Python environment configured")
print("  ✅ All imports working")
print("  ✅ Password security operational")
print("  ✅ Account service operational")
print("  ✅ Transaction service operational")
print("  ✅ Dashboard delete feature implemented")
print()
print("Next steps:")
print("  Run: pytest")
print("  Or: python -m pytest -v")
print()
