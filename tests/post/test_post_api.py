import pytest

posts_data = {
    1: ({'title': 'New post 1', 'content': 'This is first post'}, 201),
    2: ({'title': 'New post 2', 'content': 'This is second post'}, 201),
    3: ({'title': 'New post 3', 'content': 'This is third post'}, 201),
}


class TestPostApi:
    prefix = '/post'
    owner_posts = []

    testdata = [
        ({'title': 'new_title'}, 422),
        ({'content': 'new_content'}, 422),
        ({'title': '', 'content': 'new_content'}, 422),
        ({'title': 'new_title', 'content': ''}, 422),
        *posts_data.values()
    ]

    @pytest.mark.parametrize('json,code', testdata)
    async def test_add_post(self, async_client, token, json, code):
        response = await async_client.post(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {token}'},
            json=json
        )

        assert response.status_code == code
        assert isinstance(response.json(), dict) is True
        if response.status_code == 201:
            resp = response.json()
            assert len(resp.get('data', {})) == 3
            self.owner_posts.append(resp['data']['id'])

    testdata = [
        ({}, 422),
        ({'post_id': 0}, 422),
        *[({'post_id': key}, 200) for key in posts_data.keys()]
    ]

    @pytest.mark.parametrize('params,code', testdata)
    async def test_get_post(self, async_client, token, params, code):
        response = await async_client.get(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {token}'},
            params=params
        )
        print(response.json())
        assert response.status_code == code
        assert isinstance(response.json(), dict) is True

    # testdata = [
    #     ({'post_id': 1, 'title': 'Not new title'}, 200),
    #     ({'post_id': 1, 'content': 'Not new content'}, 200),
    #     ({'post_id': 1, 'title': 'Second changes',
    #       'content': 'Second my content'}, 422),
    #     ({'post_id': 1}, 422),
    # ]
    #
    # @pytest.mark.parametrize('json, code', testdata)
    # async def test_change_post(self, async_client, token, json, code):
    #     response = await async_client.patch(
    #         f'{self.prefix}/',
    #         headers={'Authorization': f'Bearer {token}'},
    #         json=json
    #     )
    #     pass
    #
    # async def test_get_all_posts(self):
    #     pass
    #
    # async def test_search_posts(self):
    #     pass
    #
    # async def test_rate_post(self):
    #     pass
    #
    # async def test_unrate_post(self):
    #     pass
    #
    # async def test_delete_post(self):
    #     pass
