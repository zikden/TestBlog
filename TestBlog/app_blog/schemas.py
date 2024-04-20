from datetime import datetime
from ninja import Schema


class Category(Schema):
    id: int
    name: str


class Article(Schema):
    id: int
    author_id: int
    title: str
    text: str
    category: Category
    created_date: datetime
    published_date: datetime
    published: bool


class Comment(Schema):
    user_id: int = None
    article_id: int = None
    text: str


class CreateArticle(Schema):
    id: int
    author_id: int
    title: str
    text: str
    category_id: int
    created_date: datetime
    published_date: datetime
    published: bool
