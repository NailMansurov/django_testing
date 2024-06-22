from datetime import datetime, timedelta

from django.test.client import Client
from django.utils import timezone

import pytest

from news.models import Comment, News

NEWS_COUNT_ON_HOME_PAGE = 10


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор',)


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create(username='Читатель',)


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def auth_user_client(auth_user):
    client = Client()
    client.force_login(auth_user)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def news_id(news):
    return (news.pk,)


@pytest.fixture
def list_of_news():
    now = datetime.today()
    all_news = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость {index}.',
            text=f'Текст новости {index}.'
        )
        news.date = now - timedelta(days=index)
        all_news.append(news)
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text='Текст',
        news=news,
        author=author,
    )
    return comment


@pytest.fixture
def post_comment():
    return {'text': 'Комментарий'}


@pytest.fixture
def comment_id(comment):
    return (comment.pk,)


@pytest.fixture
def list_of_comments(news, author):
    now = timezone.now()
    comments = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Комментарий {index}.'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)
    return comments
