from rest_framework import serializers
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from .models import Pet, AdoptionRequest, Favorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
        read_only_fields = ('id',)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class PetSerializer(serializers.ModelSerializer):
    age_display = serializers.CharField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = (
            'id', 'name', 'animal_type', 'breed', 'age', 'age_display',
            'gender', 'location', 'description', 'image', 'image_url',
            'status', 'is_available', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AdoptionRequestSerializer(serializers.ModelSerializer):
    pet_name = serializers.ReadOnlyField(source='pet.name')
    pet_details = PetSerializer(source='pet', read_only=True)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AdoptionRequest
        fields = (
            'id', 'user', 'username', 'pet', 'pet_name', 'pet_details',
            'phone', 'address', 'reason', 'previous_pet_experience',
            'message', 'status', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        # Only staff users can modify the adoption status via API
        if not (request and hasattr(request, 'user') and request.user.is_staff):
            fields['status'].read_only = True
        return fields

    def validate_pet(self, value):
        # Rule 1: Only available pets can be adopted
        if value.status != 'Available':
            raise serializers.ValidationError("This pet has already been adopted or is not available.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        pet = attrs.get('pet')

        # Rule 2: One user cannot submit multiple active requests for the same pet
        if self.instance is None:  # On create
            if pet and AdoptionRequest.objects.filter(user=user, pet=pet, status='Pending').exists():
                raise serializers.ValidationError({"pet": "You already have a pending adoption request for this pet."})

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    pet_details = PetSerializer(source='pet', read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'pet', 'pet_details', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        pet = validated_data['pet']
        favorite, _ = Favorite.objects.get_or_create(user=user, pet=pet)
        return favorite
