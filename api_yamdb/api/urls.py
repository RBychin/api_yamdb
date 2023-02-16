from django.urls import include, path
from rest_framework import routers

from api.views import ReviewViewSet, CommentViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path(r'', include(router.urls)),
]
