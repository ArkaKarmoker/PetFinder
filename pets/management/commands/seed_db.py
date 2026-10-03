from django.core.management.base import BaseCommand
from pets.seed import run_seed


class Command(BaseCommand):
    help = "Seeds database with demo pets, users, adoption requests, and favorites"

    def handle(self, *args, **options):
        self.stdout.write("Running database seeder...")
        run_seed()
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
