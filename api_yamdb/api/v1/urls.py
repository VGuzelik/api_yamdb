from api.v1.views import (CategoryViewSet, CommentViewSet, ConfirmationView,
                          GenreViewSet, ReviewViewSet, SignupView,
                          TitleViewSet, UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()


v1_router.register('categories', CategoryViewSet, basename="categories")
v1_router.register('genres', GenreViewSet, basename="genres")
v1_router.register('titles', TitleViewSet, basename='titles')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(r'users', UserViewSet, basename='user')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', ConfirmationView.as_view()),
    path('', include(v1_router.urls)),
]
