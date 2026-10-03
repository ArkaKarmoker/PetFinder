import os
import io
from pathlib import Path
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw

from pets.models import Pet, AdoptionRequest, Favorite


def generate_pet_image(name, animal_type, color_bg):
    """Generate a clean, beautiful placeholder image for demo pets using Pillow."""
    img = Image.new('RGB', (800, 600), color=color_bg)
    draw = ImageDraw.Draw(img)

    # Draw decorative accents
    draw.ellipse([(580, -60), (860, 220)], fill=(255, 255, 255, 30))
    draw.ellipse([(-80, 380), (280, 740)], fill=(255, 255, 255, 25))

    # Center card area
    card_box = [(220, 160), (580, 340)]
    draw.rectangle(card_box, fill=(255, 255, 255))

    # Draw colored header band in card
    draw.rectangle([(220, 160), (580, 210)], fill=color_bg)

    # Texts inside image
    draw.text((400, 185), f"{animal_type.upper()} PROFILE", fill=(255, 255, 255), anchor="mm")
    draw.text((400, 250), name, fill=(33, 37, 41), anchor="mm")
    draw.text((400, 295), f"PetFinder Adoption Platform", fill=(108, 117, 125), anchor="mm")

    # Bottom caption
    draw.text((400, 480), f"Adopt {name} - Healthy, Vaccinated & Friendly", fill=(255, 255, 255), anchor="mm")
    draw.text((400, 520), "Visit PetFinder to submit an adoption application", fill=(230, 230, 230), anchor="mm")

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=92)
    return ContentFile(buffer.getvalue(), name=f"{name.lower()}_{animal_type.lower()}.jpg")


def run_seed():
    print("Seeding database with demo data...")

    # 1. Superuser & Demo Users
    admin_user, _ = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@petfinder.local",
            "first_name": "System",
            "last_name": "Admin",
            "is_staff": True,
            "is_superuser": True,
        }
    )
    admin_user.set_password("admin123")
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("  [OK] Admin user created: admin / admin123")

    rahim, _ = User.objects.get_or_create(
        username="rahim",
        defaults={
            "email": "rahim@example.com",
            "first_name": "Rahim",
            "last_name": "Ahmed",
        }
    )
    rahim.set_password("rahim123")
    rahim.save()

    sarah, _ = User.objects.get_or_create(
        username="sarah",
        defaults={
            "email": "sarah@example.com",
            "first_name": "Sarah",
            "last_name": "Khan",
        }
    )
    sarah.set_password("sarah123")
    sarah.save()

    karim, _ = User.objects.get_or_create(
        username="karim",
        defaults={
            "email": "karim@example.com",
            "first_name": "Karim",
            "last_name": "Chowdhury",
        }
    )
    karim.set_password("karim123")
    karim.save()
    print("  [OK] Regular users created: rahim (rahim123), sarah (sarah123), karim (karim123)")

    # 2. Demo Pets
    pets_data = [
        {
            "name": "Max",
            "animal_type": "Dog",
            "breed": "Golden Retriever",
            "age": 2,
            "gender": "Male",
            "location": "Dhaka",
            "description": "Max is a friendly, highly energetic, and obedient Golden Retriever. He loves fetch games, running in the park, and greeting everyone with an enthusiastic tail wag. He is fully vaccinated, house-trained, and great with children.",
            "status": "Available",
            "color": (41, 128, 185),  # Blue
        },
        {
            "name": "Luna",
            "animal_type": "Cat",
            "breed": "Persian Cat",
            "age": 1,
            "gender": "Female",
            "location": "Chittagong",
            "description": "Luna is a calm, fluffy indoor Persian cat with gorgeous blue eyes. She loves cuddling up on soft blankets, napping near sunlit windows, and receiving gentle head scratches. Litter box trained and very quiet.",
            "status": "Adopted",
            "color": (142, 68, 173),  # Purple
        },
        {
            "name": "Charlie",
            "animal_type": "Dog",
            "breed": "Beagle",
            "age": 3,
            "gender": "Male",
            "location": "Sylhet",
            "description": "Charlie is a curious and intelligent Beagle with a keen nose for adventure. He gets along well with other dogs and loves weekend hikes. Looking for an active family who can give him ample outdoor time.",
            "status": "Available",
            "color": (39, 174, 96),  # Green
        },
        {
            "name": "Bella",
            "animal_type": "Cat",
            "breed": "British Shorthair",
            "age": 2,
            "gender": "Female",
            "location": "Dhaka",
            "description": "Bella is an easygoing and independent companion. She enjoys playful wand sessions and curling up beside you while you read or work. Fully vaccinated and dewormed.",
            "status": "Available",
            "color": (230, 126, 34),  # Orange
        },
        {
            "name": "Rocky",
            "animal_type": "Dog",
            "breed": "German Shepherd",
            "age": 4,
            "gender": "Male",
            "location": "Dhaka",
            "description": "Rocky is a loyal, courageous, and well-disciplined German Shepherd. He knows basic and advanced commands, walks well on a leash, and serves as both a loving protector and a gentle family companion.",
            "status": "Available",
            "color": (44, 62, 80),  # Dark Slate
        },
        {
            "name": "Milo",
            "animal_type": "Rabbit",
            "breed": "Holland Lop",
            "age": 1,
            "gender": "Male",
            "location": "Chittagong",
            "description": "Milo is a miniature lop-eared bunny with a gentle temperament. He loves munching on timothy hay, fresh coriander, and hopping around safe carpeted areas. Litter-trained and friendly.",
            "status": "Available",
            "color": (22, 160, 133),  # Teal
        },
        {
            "name": "Kiwi",
            "animal_type": "Bird",
            "breed": "Cockatiel",
            "age": 1,
            "gender": "Female",
            "location": "Rajshahi",
            "description": "Kiwi is a cheerful and vocal Cockatiel with bright yellow crest plumage. She enjoys mimicking melodies, perching on friendly shoulders, and snacking on fresh seeds and apple slices.",
            "status": "Available",
            "color": (243, 156, 18),  # Amber
        },
        {
            "name": "Daisy",
            "animal_type": "Dog",
            "breed": "Labrador Retriever",
            "age": 2,
            "gender": "Female",
            "location": "Dhaka",
            "description": "Daisy is sweet, patient, and loves splashing in water. She is wonderful with young kids and loves meeting new people. Spayed, vaccinated, and microchipped.",
            "status": "Available",
            "color": (52, 152, 219),  # Light Blue
        },
        {
            "name": "Simba",
            "animal_type": "Cat",
            "breed": "Bengal Cat",
            "age": 3,
            "gender": "Male",
            "location": "Khulna",
            "description": "Simba is an athletic and vocal Bengal cat with striking leopard-like rosettes. He loves high perches, interactive laser toys, and exploring puzzle feeders.",
            "status": "Available",
            "color": (211, 84, 0),  # Rust
        },
        {
            "name": "Coco",
            "animal_type": "Rabbit",
            "breed": "Mini Rex",
            "age": 2,
            "gender": "Female",
            "location": "Dhaka",
            "description": "Coco has velvet-like fur and an inquisitive nature. She has found her loving forever home with a quiet and attentive family.",
            "status": "Adopted",
            "color": (127, 140, 141),  # Gray
        },
    ]

    created_pets = {}
    for pdata in pets_data:
        color = pdata.pop("color")
        pet, created = Pet.objects.get_or_create(
            name=pdata["name"],
            defaults=pdata
        )
        if not pet.image:
            img_file = generate_pet_image(pet.name, pet.animal_type, color)
            pet.image.save(img_file.name, img_file, save=True)
        created_pets[pet.name] = pet

    print(f"  [OK] {len(created_pets)} demo pets created/verified.")

    # 3. Adoption Requests
    # Max -> Rahim (Pending)
    max_pet = created_pets.get("Max")
    if max_pet:
        AdoptionRequest.objects.get_or_create(
            user=rahim,
            pet=max_pet,
            defaults={
                "phone": "+8801712345678",
                "address": "House 12, Road 4, Dhanmondi, Dhaka",
                "reason": "I have a large house with a secure backyard and work from home. Looking for an energetic companion for morning jogs.",
                "previous_pet_experience": True,
                "message": "Ready to welcome Max anytime! Can visit this weekend.",
                "status": "Pending",
            }
        )

    # Luna -> Sarah (Approved)
    luna_pet = created_pets.get("Luna")
    if luna_pet:
        req, created = AdoptionRequest.objects.get_or_create(
            user=sarah,
            pet=luna_pet,
            defaults={
                "phone": "+8801812345678",
                "address": "Apartment 5B, GEC Circle, Chittagong",
                "reason": "I previously cared for Persian cats for 6 years. We have a peaceful, indoor-only environment ideal for Luna.",
                "previous_pet_experience": True,
                "message": "All cat supplies, scratchers, and high-quality food are already arranged.",
                "status": "Approved",
            }
        )
        if created and req.status == 'Approved' and luna_pet.status != 'Adopted':
            luna_pet.status = 'Adopted'
            luna_pet.save()

    # Coco -> Karim (Rejected)
    coco_pet = created_pets.get("Coco")
    if coco_pet:
        AdoptionRequest.objects.get_or_create(
            user=karim,
            pet=coco_pet,
            defaults={
                "phone": "+8801912345678",
                "address": "Sector 3, Uttara, Dhaka",
                "reason": "First-time adopting a pet, want to see how it goes.",
                "previous_pet_experience": False,
                "message": "Please let me know requirements.",
                "status": "Rejected",
            }
        )

    print("  [OK] Demo adoption requests created with Pending, Approved, and Rejected statuses.")

    # 4. Demo Favorites
    if max_pet:
        Favorite.objects.get_or_create(user=sarah, pet=max_pet)
    charlie_pet = created_pets.get("Charlie")
    if charlie_pet:
        Favorite.objects.get_or_create(user=rahim, pet=charlie_pet)
    bella_pet = created_pets.get("Bella")
    if bella_pet:
        Favorite.objects.get_or_create(user=rahim, pet=bella_pet)

    print("  [OK] Demo favorites created.")
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()
    run_seed()
