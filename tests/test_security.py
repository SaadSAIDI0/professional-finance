import pytest

from app.core.security import PasswordSecurity


def test_hash_password():
    """Test that passwords are hashed and not stored as plain text."""
    security = PasswordSecurity()
    password = "TestPassword123!"
    
    hashed = security.hash_password(password)
    
    assert hashed != password
    assert len(hashed) > len(password)


def test_verify_password_success():
    """Test that correct password is verified successfully."""
    security = PasswordSecurity()
    password = "TestPassword123!"
    
    hashed = security.hash_password(password)
    is_valid = security.verify_password(hashed, password)
    
    assert is_valid is True


def test_verify_password_failure():
    """Test that incorrect password is rejected."""
    security = PasswordSecurity()
    password = "TestPassword123!"
    wrong_password = "WrongPassword123!"
    
    hashed = security.hash_password(password)
    is_valid = security.verify_password(hashed, wrong_password)
    
    assert is_valid is False


def test_hash_password_empty():
    """Test that empty password raises ValueError."""
    security = PasswordSecurity()
    
    with pytest.raises(ValueError):
        security.hash_password("")


def test_hash_password_none():
    """Test that None password raises ValueError."""
    security = PasswordSecurity()
    
    with pytest.raises(ValueError):
        security.hash_password(None)


def test_different_hashes_same_password():
    """Test that the same password produces different hashes (Argon2 feature)."""
    security = PasswordSecurity()
    password = "TestPassword123!"
    
    hash1 = security.hash_password(password)
    hash2 = security.hash_password(password)
    
    # Different hashes but both should verify the same password
    assert hash1 != hash2
    assert security.verify_password(hash1, password) is True
    assert security.verify_password(hash2, password) is True
