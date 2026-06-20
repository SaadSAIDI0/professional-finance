from app.core.security import PasswordSecurity


def test_password_hash_is_not_plain_text():
    security = PasswordSecurity()
    password_hash = security.hash_password("strong-password")

    assert password_hash != "strong-password"
    assert security.verify_password(password_hash, "strong-password")
    assert not security.verify_password(password_hash, "wrong-password")

