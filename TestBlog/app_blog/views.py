from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router
from . import models, schemas
from auth.jwt import AuthBearer
blog = Router()
api = NinjaAPI()


@blog.get("/category", response=List[schemas.Category])
def get_category(request):
    return models.Category.objects.all()


@blog.get("/article", response=List[schemas.Article])
def get_list_article(request):
    return models.Article.objects.filter(published=True)


@blog.post("/article", response=schemas.CreateArticle, auth=AuthBearer())
def create_article(request, article: schemas.CreateArticle):
    return models.Article.objects.create(author=request.auth, **article.dict())


@blog.get("/article/{article_pk}", response=schemas.Article)
def get_single_article(request, article_pk: int):
    return get_object_or_404(models.Article, id=article_pk, published=True)


@blog.put("/article/{article_pk}", response=schemas.Article, auth=AuthBearer())
def put_single_article(request, article: schemas.Article, article_pk: int):
    if article.author_id == request.auth.id:
        _article = get_object_or_404(models.Article, id=article_pk, author=request.auth)
        _article.title = article.title
        _article.text = article.text
        _article.save()
        return _article
    return api.create_response(
        request,
        data={"message": "403 Forbidden"},
        status=403
    )


@blog.delete("/article/{article_pk}", auth=AuthBearer())
def delete_single_article(request, article: schemas.Article, article_pk: int):
    if article.author_id == request.auth.id:
        _article = get_object_or_404(models.Article,
                                     id=article_pk,
                                     author=request.auth)
        _article.delete()
        return {"success": 204}
    return api.create_response(
        request,
        data={"message": "403 Forbidden"},
        status=403
    )


@blog.post("/comment", response=schemas.Comment, auth=AuthBearer())
def create_comment(request, comment: schemas.Comment):
    return models.Comment.objects.create(user=request.auth, **comment.dict())


@blog.get("/comment/{comment_id}", response=List[schemas.Comment])
def get_comments(request, comment_id: int):
    return models.Comment.objects.filter(id=comment_id)

@blog.put("/comment/{comment_id}", response=schemas.Comment, auth=AuthBearer())
def put_comment(request, comment_id: int, comment: schemas.Comment):
    if comment.user_id == request.auth.id:
        _comment = get_object_or_404(models.Comment,
                                     id=comment_id,
                                     user=request.auth)
        _comment.article_id = comment.article_id
        _comment.text = comment.text
        _comment.save()
        return _comment
    return api.create_response(
        request,
        data={"message": "403 Forbidden"},
        status=403
    )


@blog.delete("/comment/{comment_id}", auth=AuthBearer())
def delete_comment(request, comment_id: int, comment: schemas.Comment):
    if comment.user_id == request.auth.id:
        _comment = get_object_or_404(models.Comment,
                                     id=comment_id,
                                     user=request.auth)
        _comment.delete()
        return {"success": 204}
    return api.create_response(
        request,
        data={"message": "403 Forbidden"},
        status=403
    )
