from django.contrib import admin
from articles.models import Article, Ingredient, IngredientLink


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        "ingredient_name",
        "ingredient_info",
        "updated_at",
    ]


@admin.register(IngredientLink)
class IngredientLinkAdmin(admin.ModelAdmin):
    list_display = [
        "ingredient_id",
        "link",
        "link_img",
    ]
