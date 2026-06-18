from models.user import User

def test_user_creation():
    user = User("Alice", "alice@test.com")
    assert user.name == "Alice"
    assert user.email == "alice@test.com"