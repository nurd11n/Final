from django.urls import path, include
from .views import CommentViewSet, RatingViewSet, FavouriteViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('rating', RatingViewSet)
router.register('favourite', FavouriteViewSet)

urlpatterns = [
    path('', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls