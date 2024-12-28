from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('forms', FormViewSet, basename='form')
router.register('admin-forms', AdminFormViewSet, basename='admin-forms')

urlpatterns = [
    # path("forms", FormView.as_view(), name="create_form"),
    path('', include(router.urls)),
    path("forms/<int:id>/responses", ResponseCreateView.as_view(), name="submit-response"),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth')
]
