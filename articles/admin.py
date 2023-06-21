from django.contrib import admin
from articles.models import (
    Article,
    Comment,
    Category,
    Ingredient,
    IngredientLink,
    RecipeIngredient,
)


# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(IngredientLink)
admin.site.register(RecipeIngredient)
