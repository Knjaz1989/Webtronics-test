import pytest

from apps.auth.db_handlers import get_user_by_email
from tests.conftest import async_test_session


class TestAuth:
    email_real = 'knjaz1989@gmail.com'
    password_real = '12345678'
    email_test = '1@1.ru'

    testdata = [
        ('Igor', password_real, email_real, 201),
        ('Vasya', '12345', email_test, 422),
    ]

    @pytest.mark.parametrize('name,password,email,code', testdata)
    async def test_user_sign_up(
            self, async_client, name, password, email, code
    ):
        response = await async_client.post(
            "/user/sign-up",
            json={'name': name, 'email': email, 'password': password}
        )

        assert response.status_code == code
        resp = response.json()
        assert isinstance(resp, dict) is True

    testdata = [
        (email_real, True),
        (email_test, False),
    ]

    @pytest.mark.parametrize('email,bool_value', testdata)
    async def test_get_user_by_email(self, email, bool_value):
        async with async_test_session() as session:
            user = await get_user_by_email(session, email)

            assert bool(user) is bool_value
            if bool(user):
                assert user.hashed_password != self.password_real

    testdata = [
        (email_real, '123456', 422),        # short password
        (email_real, '1234abcde', 401),     # wrong password
        (email_real, '12345678', 200),      # OK
        (email_test, '12345678', 422),      # wrong email
    ]

    @pytest.mark.parametrize('email,password,code', testdata)
    async def test_user_login(self, async_client, email, password, code):
        response = await async_client.post(
            "/user/login",
            json={'email': email, 'password': password}
        )

        assert response.status_code == code
        resp = response.json()
        assert isinstance(resp, dict) is True
