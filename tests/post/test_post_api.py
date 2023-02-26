import pytest

from apps.posts.db_handlers import get_post
from tests.conftest import async_test_session

main_user_posts_data = {
    number: (
        {
            'title': f'New post {number}',
            'content': f'This is the data of the {number} post'
        }, 201
    ) for number in range(1, 31)
}

second_user_posts_data = {
    31: ({'title': 'New post 31', 'content': 'How to get data'}, 201),
    32: ({'title': 'New post 32', 'content': 'Places in the Ney York'}, 201),
    33: ({'title': 'New post 33', 'content': 'Winter in London'}, 201),
}


class TestPostApi:
    prefix = '/post'

    testdata = [
        ({'title': 'new_title'}, 422),
        ({'content': 'new_content'}, 422),
        ({'title': '', 'content': 'new_content'}, 422),
        ({'title': 'new_title', 'content': ''}, 422),
        *main_user_posts_data.values()
    ]

    @pytest.mark.parametrize('json,code', testdata)
    async def test_add_post(self, async_client, main_token, json, code):
        response = await async_client.post(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {main_token}'},
            json=json
        )

        assert response.status_code == code
        assert isinstance(response.json(), dict) is True
        if response.status_code == 201:
            resp = response.json()
            assert len(resp.get('data', {})) == 3

    testdata = [
        *second_user_posts_data.values()
    ]

    @pytest.mark.parametrize('json,code', testdata)
    async def test_add_second_user_posts(
            self, async_client, second_token, json, code
    ):
        response = await async_client.post(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {second_token}'},
            json=json
        )

    testdata = [
        ({}, 422),
        ({'post_id': 0}, 422),
        *[({'post_id': key}, 200) for key in main_user_posts_data.keys()]
    ]

    @pytest.mark.parametrize('params,code', testdata)
    async def test_get_post(self, async_client, main_token, params, code):
        response = await async_client.get(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {main_token}'},
            params=params
        )

        assert response.status_code == code
        assert isinstance(response.json(), dict) is True

    testdata = [
        ({'limit': 0}, 0, 422),
        ({'limit': 31}, 0, 422),
        ({'page': 0}, 0, 422),
        ({}, 15, 200),
        ({'limit': 10}, 10, 200),
        ({'page': 200}, 0, 200),
        ({'limit': 10, 'page': 2}, 10, 200),
    ]

    @pytest.mark.parametrize('params,count,code', testdata)
    async def test_get_all_posts(
            self, async_client, main_token, params, count, code
    ):
        response = await async_client.get(
            f'{self.prefix}/all',
            headers={'Authorization': f'Bearer {main_token}'},
            params=params
        )
        resp = response.json()

        assert response.status_code == code
        assert isinstance(resp, dict) is True
        if response.status_code == 200:
            assert len(resp.get('data')) == count

    @pytest.mark.parametrize(
        'json, code',
        [
            ({'post_id': 1, 'title': 'Not new title'}, 200),
            ({'post_id': 2, 'content': 'Not new content'}, 200),
            ({
                 'post_id': 3, 'title': 'change title',
                 'content': 'Change content'
             }, 200),
            ({'post_id': 31, 'title': 'Other title'}, 403),
            ({'post_id': 32, 'content': 'Other content'}, 403),
            ({'post_id': 4}, 422),
        ]
    )
    async def test_change_post(self, async_client, main_token, json, code):
        response = await async_client.patch(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {main_token}'},
            json=json
        )

        status_code = response.status_code
        assert status_code == code
        if status_code == 200:
            async with async_test_session() as session:
                post = await get_post(session, json['post_id'])
                del json['post_id']
                for key, value in json.items():
                    assert post.get(key) == value

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
