# initialize these with python TAI/manage.py create_packages in bash
from django.core.management.base import BaseCommand
from mainapp.models import TokensPackage

class Command(BaseCommand):
    help = "Create predefined token packages."

    def handle(self, *args, **options):
        packages_data = [
            {
                "name" : "option1",
                "price" : 4.99,
                "token_value" : 70,
                "BV" : False
            },
            {
                "name" : "option2",
                "price" : 9.99,
                "token_value" : 370,
                "BV" : False 
            },
            {
                "name" : "option3",
                "price" : 19.99,
                "token_value" : 1200,
                "BV" : False
            },
            {
                "name" : "option4",
                "price" : 50.0,
                "token_value" : 3190,
                "BV" : False
            },
            {
                "name" : "option5",
                "price" : 100.0,
                "token_value" : 7360,
                "BV" : True
            }
        ]

        for package in packages_data:
            if not TokensPackage.objects.filter(name=package['name']).exists():
                TokensPackage.objects.create(
                    name=package['name'],
                    price=package['price'],
                    token_value=package['token_value'],
                    bv=package['BV']
                )
                self.stdout.write(self.style.SUCCESS(f"Package '{package['name']} created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Package '{package['name']} already exists."))
        
