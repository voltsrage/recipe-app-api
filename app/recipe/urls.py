"""
URL mappings for the user API
"""

from django.urls import path,include

from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes',views.RecipeViewSet)

app_name='recipe'

urlpatterns = [
	path('',include(router.urls))
]