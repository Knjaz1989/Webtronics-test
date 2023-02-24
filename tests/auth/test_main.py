import pytest


class TestUser:

    async def test_create_user(self, async_client):
        response = await async_client.post(
            "/user/sign-up", json={
                'name': 'Melanie', 'email': '40@mail.ru', 'password': '12345'}
        )
        assert response.status_code == 200

