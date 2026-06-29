"""
Management command to seed the database with sample recipes.
Run with: python manage.py seed_data

Creates a demo user and 6 sample recipes with tags and ingredients
so new visitors see real content when they first log in.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Ingredient, Recipe, Tag

User = get_user_model()

DEMO_EMAIL    = "demo@recipeapp.com"
DEMO_PASSWORD = "DemoPass123!"
DEMO_NAME     = "Recipe Bot"

SEED_RECIPES = [
    {
        "title": "Spaghetti Carbonara",
        "description": (
            "A classic Roman pasta dish made with eggs, Pecorino Romano, "
            "guanciale, and black pepper. The key is removing the pan from "
            "heat before adding the egg mixture to avoid scrambling."
        ),
        "time_minutes": 25,
        "price": "8.50",
        "link": "https://www.bonappetit.com/recipe/spaghetti-carbonara",
        "tags": ["Italian", "Pasta", "Quick"],
        "ingredients": [
            "200g spaghetti",
            "100g guanciale",
            "2 large eggs",
            "2 egg yolks",
            "50g Pecorino Romano",
            "Black pepper",
            "Salt",
        ],
    },
    {
        "title": "Chicken Tikka Masala",
        "description": (
            "Tender marinated chicken in a rich, creamy tomato-based sauce "
            "spiced with garam masala, cumin, and coriander. Serve with "
            "basmati rice and naan for a complete meal."
        ),
        "time_minutes": 45,
        "price": "12.00",
        "link": "",
        "tags": ["Indian", "Chicken", "Spicy"],
        "ingredients": [
            "500g chicken breast",
            "200ml yoghurt",
            "400ml coconut cream",
            "400g tinned tomatoes",
            "1 onion",
            "3 garlic cloves",
            "Garam masala",
            "Cumin",
            "Coriander",
            "Ginger",
        ],
    },
    {
        "title": "Avocado Toast",
        "description": (
            "Simple, nutritious, and endlessly customisable. Creamy mashed "
            "avocado on toasted sourdough with a squeeze of lemon and chilli "
            "flakes. Top with a poached egg for extra protein."
        ),
        "time_minutes": 10,
        "price": "5.00",
        "link": "",
        "tags": ["Vegetarian", "Breakfast", "Quick"],
        "ingredients": [
            "2 slices sourdough bread",
            "1 ripe avocado",
            "Lemon juice",
            "Chilli flakes",
            "Salt",
            "Black pepper",
            "2 eggs (optional)",
        ],
    },
    {
        "title": "Beef Tacos",
        "description": (
            "Seasoned ground beef in crispy corn tortillas loaded with fresh "
            "pico de gallo, shredded cheese, sour cream, and lime. A crowd "
            "pleaser that comes together in under 30 minutes."
        ),
        "time_minutes": 25,
        "price": "10.00",
        "link": "",
        "tags": ["Mexican", "Beef", "Quick"],
        "ingredients": [
            "500g ground beef",
            "8 corn tortillas",
            "2 tomatoes",
            "1 onion",
            "Cheddar cheese",
            "Sour cream",
            "Lime",
            "Cumin",
            "Paprika",
            "Garlic powder",
        ],
    },
    {
        "title": "Greek Salad",
        "description": (
            "A refreshing Mediterranean salad with crisp cucumbers, ripe "
            "tomatoes, Kalamata olives, and creamy feta cheese dressed with "
            "extra-virgin olive oil and dried oregano. No cooking required."
        ),
        "time_minutes": 10,
        "price": "6.00",
        "link": "",
        "tags": ["Greek", "Vegetarian", "Salad", "Quick"],
        "ingredients": [
            "2 cucumbers",
            "4 tomatoes",
            "1 red onion",
            "200g feta cheese",
            "Kalamata olives",
            "Extra virgin olive oil",
            "Dried oregano",
            "Salt",
        ],
    },
    {
        "title": "Chocolate Lava Cake",
        "description": (
            "Warm individual chocolate cakes with a gooey molten centre. "
            "Serve immediately from the oven with a scoop of vanilla ice cream "
            "and a dusting of icing sugar. Impressive but surprisingly easy."
        ),
        "time_minutes": 20,
        "price": "7.00",
        "link": "",
        "tags": ["Dessert", "Chocolate", "Quick"],
        "ingredients": [
            "200g dark chocolate",
            "100g butter",
            "4 eggs",
            "100g caster sugar",
            "60g plain flour",
            "Icing sugar",
            "Vanilla ice cream",
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample recipes for demo purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing seed data before re-seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing demo data…")
            try:
                demo_user = User.objects.get(email=DEMO_EMAIL)
                Recipe.objects.filter(user=demo_user).delete()
                Tag.objects.filter(user=demo_user).delete()
                Ingredient.objects.filter(user=demo_user).delete()
                self.stdout.write(self.style.WARNING("Demo data cleared."))
            except User.DoesNotExist:
                self.stdout.write("No demo user found — nothing to clear.")

        # Get or create demo user
        user, created = User.objects.get_or_create(
            email=DEMO_EMAIL,
            defaults={"name": DEMO_NAME},
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created demo user: {DEMO_EMAIL}"))
        else:
            self.stdout.write(f"Using existing demo user: {DEMO_EMAIL}")

        # Skip if recipes already exist for this user
        if Recipe.objects.filter(user=user).exists():
            self.stdout.write(
                self.style.WARNING("Seed data already exists. Run with --clear to re-seed.")
            )
            return

        # Create recipes
        for data in SEED_RECIPES:
            recipe = Recipe.objects.create(
                user=user,
                title=data["title"],
                description=data["description"],
                time_minutes=data["time_minutes"],
                price=data["price"],
                link=data.get("link", ""),
            )

            for tag_name in data["tags"]:
                tag, _ = Tag.objects.get_or_create(user=user, name=tag_name)
                recipe.tags.add(tag)

            for ing_name in data["ingredients"]:
                ing, _ = Ingredient.objects.get_or_create(user=user, name=ing_name)
                recipe.ingredients.add(ing)

            self.stdout.write(f"  ✓ Created: {recipe.title}")

        self.stdout.write(self.style.SUCCESS(
            f"\nSeeding complete! {len(SEED_RECIPES)} recipes created.\n"
            f"Demo login → email: {DEMO_EMAIL}  password: {DEMO_PASSWORD}"
        ))
