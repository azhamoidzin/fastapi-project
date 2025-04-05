import asyncio


def test_get_user(test_db, test_user):
    from app.services.user_service import get_user

    retrieved_user = asyncio.run(get_user(test_db, test_user.id))
    assert retrieved_user is not None
    assert retrieved_user.id == test_user.id
    assert retrieved_user.email == test_user.email


def test_get_nonexistent_user(test_db):
    from app.services.user_service import get_user

    retrieved_user = asyncio.run(get_user(test_db, 0))
    assert retrieved_user is None


def test_get_user_by_email(test_db, test_user):
    from app.services.user_service import get_user_by_email

    retrieved_user = asyncio.run(get_user_by_email(test_db, test_user.email))
    assert retrieved_user is not None
    assert retrieved_user.id == test_user.id
    assert retrieved_user.email == test_user.email


def test_get_nonexistent_user_by_email(test_db):
    from app.services.user_service import get_user_by_email

    retrieved_user = asyncio.run(get_user_by_email(test_db, "test@example.com"))
    assert retrieved_user is None


def test_get_users(test_db, test_user):
    from app.services.user_service import get_users

    users = asyncio.run(get_users(test_db))
    assert len(users) == 1
    assert users[0].id == test_user.id


def test_get_users_empty(test_db):
    from app.services.user_service import get_users

    users = asyncio.run(get_users(test_db))
    assert len(users) == 0


def test_create_user(test_db):
    from app.services.user_service import create_user
    from app.schemas.user import UserCreate

    # noinspection PyTypeChecker
    user_create = UserCreate(email="test@example.com", password="pwd")
    user = asyncio.run(create_user(test_db, user_create))
    assert user.id is not None
    assert user_create.email == user.email


def test_activate_user(test_db, test_user_inactive):
    from app.services.user_service import activate_user

    user = asyncio.run(activate_user(test_db, "test1@example.com"))
    assert user.is_active is True

