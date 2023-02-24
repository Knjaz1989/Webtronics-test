import pytest


class TestPostApi:
    prefix = '/post'

    testdata = [
        ({'title': 'New title', 'content': 'This is a new post'}, 201),
        ({'title': 'new_title'}, 422),
        ({'content': 'new_content'}, 422),
        ({'title': '', 'content': 'new_content'}, 422),
        ({'title': 'new_title', 'content': ''}, 422),
    ]

    @pytest.mark.parametrize('json, code', testdata)
    async def test_add_post(self, async_client, token, json, code):
        response = await async_client.post(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {token}'},
            json=json
        )

        assert response.status_code == code
        assert isinstance(response.json(), dict) is True

    async def test_change_post(self):
        pass

    async def test_get_post(self):
        pass

    async def test_get_all_posts(self):
        pass

    async def test_search_posts(self):
        pass

    async def test_rate_post(self):
        pass

    async def test_unrate_post(self):
        pass

    async def test_delete_post(self):
        pass
