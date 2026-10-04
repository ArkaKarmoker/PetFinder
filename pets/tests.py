from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Pet, AdoptionRequest, Favorite

# Create your tests here.


class PetModelTests(TestCase):
    def setUp(self):
        self.pet = Pet.objects.create(
            name="Buddy",
            animal_type="Dog",
            breed="Golden Retriever",
            age=2,
            gender="Male",
            location="Dhaka",
            description="A playful golden pup.",
            status="Available"
        )

    def test_pet_str(self):
        self.assertEqual(str(self.pet), "Buddy (Dog - Golden Retriever)")

    def test_pet_properties(self):
        self.assertTrue(self.pet.is_available)
        self.assertEqual(self.pet.age_display, "2 years")

        self.pet.age = 1
        self.assertEqual(self.pet.age_display, "1 year")

        self.pet.status = "Adopted"
        self.assertFalse(self.pet.is_available)


class BusinessLogicTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="password123", email="user2@example.com")
        self.pet = Pet.objects.create(
            name="Milo",
            animal_type="Dog",
            breed="Beagle",
            age=3,
            gender="Male",
            location="Dhaka",
            description="Friendly beagle.",
            status="Available"
        )

    def test_rule1_cannot_adopt_already_adopted_pet(self):
        """Rule 1: Only available pets can be adopted."""
        self.pet.status = "Adopted"
        self.pet.save()

        adoption = AdoptionRequest(
            user=self.user1,
            pet=self.pet,
            phone="01711111111",
            address="Dhaka",
            reason="I love dogs"
        )
        with self.assertRaises(ValidationError):
            adoption.clean()

    def test_rule2_cannot_submit_duplicate_active_pending_request(self):
        """Rule 2: One user cannot submit multiple active requests for the same pet."""
        AdoptionRequest.objects.create(
            user=self.user1,
            pet=self.pet,
            phone="01711111111",
            address="Dhaka",
            reason="First request",
            status="Pending"
        )

        second_request = AdoptionRequest(
            user=self.user1,
            pet=self.pet,
            phone="01711111111",
            address="Dhaka",
            reason="Second request"
        )
        with self.assertRaises(ValidationError):
            second_request.clean()

    def test_rule2_different_user_can_submit_request(self):
        """Different users can submit requests for the same available pet."""
        req1 = AdoptionRequest.objects.create(
            user=self.user1,
            pet=self.pet,
            phone="01711111111",
            address="Dhaka",
            reason="Request by user 1",
            status="Pending"
        )
        req2 = AdoptionRequest(
            user=self.user2,
            pet=self.pet,
            phone="01722222222",
            address="Chittagong",
            reason="Request by user 2"
        )
        # Should not raise
        req2.clean()
        req2.save()
        self.assertEqual(AdoptionRequest.objects.filter(pet=self.pet).count(), 2)

    def test_rule3_approved_request_changes_pet_status_to_adopted(self):
        """Rule 3: Approved application changes pet status to Adopted and rejects other pending requests."""
        req1 = AdoptionRequest.objects.create(
            user=self.user1,
            pet=self.pet,
            phone="01711111111",
            address="Dhaka",
            reason="User 1 request",
            status="Pending"
        )
        req2 = AdoptionRequest.objects.create(
            user=self.user2,
            pet=self.pet,
            phone="01722222222",
            address="Chittagong",
            reason="User 2 request",
            status="Pending"
        )

        # Admin approves req1
        req1.status = "Approved"
        req1.save()

        self.pet.refresh_from_db()
        self.assertEqual(self.pet.status, "Adopted")

        # Other pending request should be rejected
        req2.refresh_from_db()
        self.assertEqual(req2.status, "Rejected")


class TemplateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.pet_available = Pet.objects.create(
            name="Simba",
            animal_type="Cat",
            breed="Bengal",
            age=2,
            gender="Male",
            location="Dhaka",
            description="Lovely bengal cat.",
            status="Available"
        )
        self.pet_adopted = Pet.objects.create(
            name="Bella",
            animal_type="Cat",
            breed="Persian",
            age=1,
            gender="Female",
            location="Sylhet",
            description="Adopted persian cat.",
            status="Adopted"
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PetFinder")
        self.assertContains(response, "Simba")

    def test_pet_list_page(self):
        response = self.client.get(reverse('pet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Simba")
        self.assertContains(response, "Bella")

    def test_pet_list_filtering(self):
        # Filter by animal_type
        response = self.client.get(reverse('pet_list'), {'animal_type': 'Cat'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Simba")

        # Filter by search
        response = self.client.get(reverse('pet_list'), {'search': 'Simba'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Simba")
        self.assertNotContains(response, "Bella")

        # Filter by status
        response = self.client.get(reverse('pet_list'), {'status': 'Adopted'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bella")
        self.assertNotContains(response, "Simba")

    def test_pet_detail_page(self):
        # Available pet
        response = self.client.get(reverse('pet_detail', args=[self.pet_available.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Simba")

        # Adopted pet
        response = self.client.get(reverse('pet_detail', args=[self.pet_adopted.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This pet has already been adopted")

    def test_apply_adoption_requires_login(self):
        response = self.client.get(reverse('apply_adoption', args=[self.pet_available.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_apply_adoption_submission(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse('apply_adoption', args=[self.pet_available.id]), {
            'phone': '+8801712345678',
            'address': 'House 1, Dhaka',
            'reason': 'Great family for Simba',
            'previous_pet_experience': True,
            'message': 'Looking forward to meeting him'
        })
        self.assertRedirects(response, reverse('user_dashboard'))
        self.assertTrue(AdoptionRequest.objects.filter(user=self.user, pet=self.pet_available).exists())

    def test_cannot_apply_for_adopted_pet(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('apply_adoption', args=[self.pet_adopted.id]))
        self.assertRedirects(response, reverse('pet_detail', args=[self.pet_adopted.id]))

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Adoption Requests")

    def test_toggle_favorite(self):
        self.client.login(username="testuser", password="password123")
        # Add favorite
        response = self.client.post(reverse('toggle_favorite', args=[self.pet_available.id]))
        self.assertTrue(Favorite.objects.filter(user=self.user, pet=self.pet_available).exists())

        # Remove favorite
        response = self.client.post(reverse('toggle_favorite', args=[self.pet_available.id]))
        self.assertFalse(Favorite.objects.filter(user=self.user, pet=self.pet_available).exists())


class RestAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="apiuser", password="password123", email="api@example.com")
        self.other_user = User.objects.create_user(username="otheruser", password="password123", email="other@example.com")
        self.admin = User.objects.create_superuser(username="apiadmin", password="password123", email="admin@example.com")

        self.pet = Pet.objects.create(
            name="Rex",
            animal_type="Dog",
            breed="German Shepherd",
            age=3,
            gender="Male",
            location="Dhaka",
            description="Loyal dog.",
            status="Available"
        )

    def test_jwt_auth_flow(self):
        # 1. Obtain Token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'apiuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        access_token = response.data['access']
        refresh_token = response.data['refresh']

        # 2. Refresh Token
        refresh_response = self.client.post(reverse('token_refresh'), {
            'refresh': refresh_token
        })
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

        # 3. Access Protected Profile with JWT
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_response = self.client.get(reverse('api_profile'))
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], 'apiuser')

    def test_api_user_registration(self):
        response = self.client.post(reverse('api_register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'secretpassword',
            'password_confirm': 'secretpassword',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])

    def test_pet_api_endpoints(self):
        # List Pets
        response = self.client.get(reverse('api_pet_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        # Search Pets
        response = self.client.get(reverse('api_pet_list_create'), {'search': 'Rex'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        # Filter by animal_type
        response = self.client.get(reverse('api_pet_list_create'), {'animal_type': 'Cat'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        # Retrieve Pet Detail
        response = self.client.get(reverse('api_pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Rex')

    def test_adoption_api_flow_and_isolation(self):
        # Obtain token for apiuser
        token_res = self.client.post(reverse('token_obtain_pair'), {
            'username': 'apiuser',
            'password': 'password123'
        })
        access_token = token_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Create Adoption Request via API
        post_res = self.client.post(reverse('api_adoption_list_create'), {
            'pet': self.pet.id,
            'phone': '+8801700000000',
            'address': 'Dhanmondi, Dhaka',
            'reason': 'Great environment for dogs',
            'previous_pet_experience': True,
            'message': 'Can pick up tomorrow'
        })
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        req_id = post_res.data['id']

        # Rule 2 in API: Duplicate active request rejected
        duplicate_res = self.client.post(reverse('api_adoption_list_create'), {
            'pet': self.pet.id,
            'phone': '+8801700000000',
            'address': 'Dhanmondi, Dhaka',
            'reason': 'Duplicate request'
        })
        self.assertEqual(duplicate_res.status_code, status.HTTP_400_BAD_REQUEST)

        # Check list of adoption requests for apiuser
        list_res = self.client.get(reverse('api_adoption_list_create'))
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertEqual(list_res.data['count'], 1)

        # Switch to other_user
        token_other = self.client.post(reverse('token_obtain_pair'), {
            'username': 'otheruser',
            'password': 'password123'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_other.data["access"]}')

        # Isolation: other_user should see 0 requests
        other_list = self.client.get(reverse('api_adoption_list_create'))
        self.assertEqual(other_list.status_code, status.HTTP_200_OK)
        self.assertEqual(other_list.data['count'], 0)

        # other_user cannot access apiuser's adoption request directly
        detail_res = self.client.get(reverse('api_adoption_detail', args=[req_id]))
        self.assertEqual(detail_res.status_code, status.HTTP_404_NOT_FOUND)


class AdminActionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpassword", email="admin@test.com")
        self.applicant = User.objects.create_user(username="applicant", password="userpassword")
        self.pet = Pet.objects.create(
            name="Bruno",
            animal_type="Dog",
            breed="Boxer",
            age=3,
            gender="Male",
            location="Dhaka",
            description="Boxer dog.",
            status="Available"
        )
        self.adoption_req = AdoptionRequest.objects.create(
            user=self.applicant,
            pet=self.pet,
            phone="01712345678",
            address="Dhaka",
            reason="Loves dogs",
            status="Pending"
        )

    def test_admin_approve_action(self):
        self.client.login(username="admin", password="adminpassword")
        # Change status via admin change view
        response = self.client.post(
            reverse('admin:pets_adoptionrequest_change', args=[self.adoption_req.id]),
            {
                'user': self.applicant.id,
                'pet': self.pet.id,
                'phone': '01712345678',
                'address': 'Dhaka',
                'reason': 'Loves dogs',
                'status': 'Approved',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.adoption_req.refresh_from_db()
        self.assertEqual(self.adoption_req.status, 'Approved')
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.status, 'Adopted')


class SwaggerAndFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.pet = Pet.objects.create(
            name="Rocky",
            animal_type="Dog",
            breed="Husky",
            age=2,
            gender="Male",
            location="Sylhet",
            description="Active husky dog.",
            status="Available"
        )

    def test_swagger_and_schema_endpoints(self):
        # OpenAPI JSON schema endpoint
        schema_res = self.client.get(reverse('schema'))
        self.assertEqual(schema_res.status_code, 200)

        # Swagger UI HTML view
        swagger_res = self.client.get(reverse('swagger-ui'))
        self.assertEqual(swagger_res.status_code, 200)
        self.assertContains(swagger_res, "swagger-ui")

        # ReDoc HTML view
        redoc_res = self.client.get(reverse('redoc'))
        self.assertEqual(redoc_res.status_code, 200)

    def test_breed_filter(self):
        response = self.client.get(reverse('pet_list'), {'breed': 'Husky'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rocky")

        empty_res = self.client.get(reverse('pet_list'), {'breed': 'Poodle'})
        self.assertEqual(empty_res.status_code, 200)
        self.assertNotContains(empty_res, "Rocky")

