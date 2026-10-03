from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Pet(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Bird', 'Bird'),
        ('Rabbit', 'Rabbit'),
        ('Other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
    ]

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=ANIMAL_TYPE_CHOICES, default='Dog')
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(help_text="Age in years")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.animal_type} - {self.breed})"

    @property
    def is_available(self):
        return self.status == 'Available'

    @property
    def age_display(self):
        if self.age == 1:
            return "1 year"
        return f"{self.age} years"


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    phone = models.CharField(max_length=20)
    address = models.TextField()
    reason = models.TextField()
    previous_pet_experience = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request by {self.user.username} for {self.pet.name} [{self.status}]"

    def clean(self):
        super().clean()
        # Rule 1: Only available pets can be adopted for new applications
        if not self.pk:
            if hasattr(self, 'pet') and self.pet_id:
                if self.pet.status != 'Available':
                    raise ValidationError({'pet': 'This pet is not available for adoption.'})

            # Rule 2: One user cannot submit multiple active (Pending) requests for the same pet
            if hasattr(self, 'user') and self.user_id and hasattr(self, 'pet') and self.pet_id:
                existing_active = AdoptionRequest.objects.filter(
                    user=self.user,
                    pet=self.pet,
                    status='Pending'
                )
                if existing_active.exists():
                    raise ValidationError({'pet': 'You already have a pending adoption request for this pet.'})

    def save(self, *args, **kwargs):
        # Rule 3: Approved application changes pet status to Adopted
        if self.status == 'Approved' and self.pet.status != 'Adopted':
            self.pet.status = 'Adopted'
            self.pet.save(update_fields=['status'])
            # Reject other pending requests for the same pet as it is now adopted
            AdoptionRequest.objects.filter(pet=self.pet, status='Pending').exclude(pk=self.pk).update(status='Rejected')
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pet')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} favorited {self.pet.name}"
