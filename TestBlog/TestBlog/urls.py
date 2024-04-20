from django.contrib import admin
from django.urls import path
from app_blog.views import blog
from auth.views import api_auth
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('blog/', blog)
api.add_router('auth/', api_auth)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
