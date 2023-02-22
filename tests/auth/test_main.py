import pytest


@pytest.mark.asyncio
class TestUser:

    @pytest.fixture(autouse=True)
    def set_up(self, app_client) -> None:
        """Declare fixtures as class attributes"""
        self.client = app_client


    async def test_create_user(self):
        response = await self.client.post(
            "/user/sign-up", json={
                'name': 'Melanie', 'email': '40@mail.ru', 'password': '12345'}
        )
        assert response.status_code == 200

