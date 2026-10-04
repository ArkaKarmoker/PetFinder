from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Pet, AdoptionRequest, Favorite
from .serializers import (
    PetSerializer,
    AdoptionRequestSerializer,
    FavoriteSerializer,
    UserSerializer,
    UserRegisterSerializer
)


@extend_schema(tags=['Authentication'], summary="Register a new user account")
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully.",
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Authentication'], summary="Retrieve or update authenticated user profile")
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    get=extend_schema(tags=['Pets'], summary="List all pets (supports search, filter, and pagination)"),
    post=extend_schema(tags=['Pets'], summary="Create a new pet listing (requires authentication)")
)
class PetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_type', 'gender', 'location', 'status', 'breed']
    search_fields = ['name', 'breed', 'location', 'description', 'animal_type']
    ordering_fields = ['created_at', 'age', 'name']


@extend_schema_view(
    get=extend_schema(tags=['Pets'], summary="Retrieve pet details by ID"),
    put=extend_schema(tags=['Pets'], summary="Update all pet details"),
    patch=extend_schema(tags=['Pets'], summary="Partially update pet details"),
    delete=extend_schema(tags=['Pets'], summary="Delete a pet listing")
)
class PetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema_view(
    get=extend_schema(tags=['Adoptions'], summary="List adoption requests (User sees own requests; Staff sees all)"),
    post=extend_schema(tags=['Adoptions'], summary="Submit a new adoption application for an available pet")
)
class AdoptionRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'pet']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AdoptionRequest.objects.none()
        user = self.request.user
        if user.is_staff:
            return AdoptionRequest.objects.all().select_related('user', 'pet')
        return AdoptionRequest.objects.filter(user=user).select_related('user', 'pet')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(tags=['Adoptions'], summary="Retrieve an adoption request by ID"),
    put=extend_schema(tags=['Adoptions'], summary="Update an adoption request (Staff can approve/reject status)"),
    patch=extend_schema(tags=['Adoptions'], summary="Partially update an adoption request")
)
class AdoptionRequestDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AdoptionRequest.objects.none()
        user = self.request.user
        if user.is_staff:
            return AdoptionRequest.objects.all().select_related('user', 'pet')
        return AdoptionRequest.objects.filter(user=user).select_related('user', 'pet')


@extend_schema_view(
    get=extend_schema(tags=['Favorites'], summary="List authenticated user's favorited pets"),
    post=extend_schema(tags=['Favorites'], summary="Add a pet to user's favorites")
)
class FavoriteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user).select_related('pet')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Favorites'], summary="Remove a pet from favorites by ID")
class FavoriteDestroyAPIView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)
