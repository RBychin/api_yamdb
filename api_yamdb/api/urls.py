from django.urls import include, path
from rest_framework import routers

from api.views import (
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
