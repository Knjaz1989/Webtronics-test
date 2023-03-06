import pytest
from sqlalchemy import select

from apps.posts.db_handlers import get_post
from database.models import Rate
from settings import config
from tests.conftest import async_test_session, get_posts_count

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
    33: (
        {
            'title': 'Winter in London',
            'content': 'I went to the London in winter'
        }, 201
    ),
}


class TestPostApi:
    prefix = '/api/post'

    @pytest.mark.parametrize(
        'json,code',
        [
            ({'title': 'new_title'}, 422),
            ({'content': 'new_content'}, 422),
            ({'title': '', 'content': 'new_content'}, 422),
            ({'title': 'new_title', 'content': ''}, 422),
            *main_user_posts_data.values()
        ]
    )
    async def test_add_main_user_post(
            self, async_client, main_token, json, code
    ):
        start_count = await get_posts_count()
        response = await async_client.post(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {main_token}'},
            json=json
        )

        assert response.status_code == code
        assert isinstance(response.json(), dict) is True
        if response.status_code == 201:
            resp = response.json()
            end_count = await get_posts_count()
            assert len(resp.get('data', {})) == 3
            assert end_count == start_count + 1

    @pytest.mark.parametrize(
        'json,code',
        [
            *second_user_posts_data.values()
        ]
    )
    async def test_add_second_user_posts(
            self, async_client, second_token, json, code
    ):
        start_count = await get_posts_count()
        response = await async_client.post(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {second_token}'},
            json=json
        )

        assert response.status_code == code
        end_count = await get_posts_count()
        assert end_count == start_count + 1

    @pytest.mark.parametrize(
        'params,code',
        [
            ({}, 422),
            ({'post_id': 0}, 422),
            *[({'post_id': key}, 200) for key in main_user_posts_data.keys()]
        ]
    )
    async def test_get_post(self, async_client, main_token, params, code):
        response = await async_client.get(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {main_token}'},
            params=params
        )

        assert response.status_code == code
        assert isinstance(response.json(), dict) is True

    @pytest.mark.parametrize(
        'params,count,code',
        [
            ({'limit': 0}, 0, 422),
            ({'limit': 31}, 0, 422),
            ({'page': 0}, 0, 422),
            ({}, config.POSTS_LIMIT, 200),
            ({'limit': 10}, 10, 200),
            ({'page': 200}, 0, 200),
            ({'limit': 10, 'page': 2}, 10, 200),
        ]
    )
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
        resp = response.json()
        st_code = response.status_code

        assert st_code == code
        assert isinstance(resp, dict) is True
        if st_code == 200:
            async with async_test_session() as session:
                post = await get_post(session, json['post_id'])
                del json['post_id']
                for key, value in json.items():
                    assert post.get(key) == value

    @pytest.mark.parametrize(
        'params,count,code',
        [
            ({}, 0, 422),
            ({'content': ''}, 0, 422),
            ({'title': ''}, 0, 422),
            ({'title': 'New'}, config.POSTS_LIMIT, 200),
            ({'title': 'new'}, config.POSTS_LIMIT, 200),
            ({'title': 'new', 'limit': 30}, 30, 200),
            ({'title': 'winter'}, 1, 200),
            ({'content': 'In'}, 2, 200),
            ({'content': 'in'}, 2, 200),
            ({'title': 'new', 'limit': 0}, 0, 422),
            ({'title': 'new', 'limit': 10}, 10, 200),
            ({'title': 'new', 'limit': 31}, 0, 422),
            ({'title': 'new', 'limit': 10, 'page': 0}, 0, 422),
            ({'title': 'new', 'limit': 10, 'page': 10}, 0, 200),
        ]
    )
    async def test_search_posts(
            self, async_client, main_token, params, count, code
    ):
        response = await async_client.get(
            f'{self.prefix}/search',
            headers={'Authorization': f'Bearer {main_token}'},
            params=params
        )
        st_code = response.status_code
        resp = response.json()

        assert st_code == code
        assert isinstance(resp, dict) is True
        if st_code == 200:
            assert len(resp['data']) == count

    @pytest.mark.parametrize(
        'json,code',
        [
            ({}, 422),
            ({'post_id': 1}, 422),
            ({'post_id': 1, 'action': 'go'}, 422),
            ({'post_id': 1, 'action': 'like'}, 403),
            ({'post_id': 31, 'action': 'like'}, 200),
            ({'post_id': 31, 'action': 'like'}, 400),
            ({'post_id': 31, 'action': 'dislike'}, 200),
        ]
    )
    async def test_rate_post(self, async_client, main_token, json, code):
        response = await async_client.post(
            f'{self.prefix}/rate',
            headers={'Authorization': f'Bearer {main_token}'},
            json=json
        )
        resp = response.json()
        st_code = response.status_code

        assert st_code == code
        assert isinstance(resp, dict) is True
        if st_code == 200:
            async with async_test_session() as session:
                rate = await session.execute(
                    select(Rate).where(
                        Rate.post_id == json['post_id'],
                        Rate.user_id == 1
                    )
                )
                rate = rate.scalars().first()
                assert rate.like is not rate.dislike

    @pytest.mark.parametrize(
        'params,code',
        [
            ({}, 422),
            ({'post_id': 0}, 422),
            ({'post_id': 1}, 403),
            ({'post_id': 31}, 200),
            ({'post_id': 31}, 403),
        ]
    )
    async def test_unrate_post(self, async_client, main_token, params, code):
        response = await async_client.delete(
            f'{self.prefix}/rate',
            headers={'Authorization': f'Bearer {main_token}'},
            params=params
        )
        resp = response.json()
        st_code = response.status_code

        assert st_code == code
        assert isinstance(resp, dict) is True
        if st_code == 200:
            async with async_test_session() as session:
                rate = await session.execute(
                    select(Rate)
                )
                rates = rate.scalars().all()
                assert len(rates) == 0

    @pytest.mark.parametrize(
        'params,code',
        [
            ({}, 422),
            ({'post_id': 0}, 422),
            ({'post_id': 1}, 200),
            ({'post_id': 31}, 403),
        ]
    )
    async def test_delete_post(self, async_client, main_token, params, code):
        start_count = await get_posts_count()
        response = await async_client.delete(
            f'{self.prefix}/',
            headers={'Authorization': f'Bearer {main_token}'},
            params=params
        )
        resp = response.json()
        st_code = response.status_code

        assert st_code == code
        assert isinstance(resp, dict) is True
        if st_code == 200:
            end_count = await get_posts_count()
            assert end_count + 1 == start_count
