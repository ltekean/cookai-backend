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


class MyModelAdmin(admin.ModelAdmin):
    list_display = ["tag_list"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
