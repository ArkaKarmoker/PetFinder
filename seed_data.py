"""
Standalone database seeding script for PetFinder.
Can be executed using:
    python seed_data.py
or via Django management command:
    python manage.py seed_db
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from pets.seed import run_seed

if __name__ == "__main__":
    run_seed()
