from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api_views

urlpatterns = [
    # JWT Authentication Endpoints
    path('auth/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', api_views.UserProfileAPIView.as_view(), name='api_profile'),

    # Pet API Endpoints
    path('pets/', api_views.PetListCreateAPIView.as_view(), name='api_pet_list_create'),
    path('pets/<int:pk>/', api_views.PetDetailAPIView.as_view(), name='api_pet_detail'),

    # Adoption Request API Endpoints
    path('adoptions/', api_views.AdoptionRequestListCreateAPIView.as_view(), name='api_adoption_list_create'),
    path('adoptions/<int:pk>/', api_views.AdoptionRequestDetailAPIView.as_view(), name='api_adoption_detail'),

    # Favorites API Endpoints (Bonus)
    path('favorites/', api_views.FavoriteListCreateAPIView.as_view(), name='api_favorite_list_create'),
    path('favorites/<int:pk>/', api_views.FavoriteDestroyAPIView.as_view(), name='api_favorite_detail'),
]
