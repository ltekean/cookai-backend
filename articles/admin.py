from django.contrib import admin
from articles.models import (
    Article,
    Comment,
    Category,
    Ingredient,
    IngredientLink,
    RecipeIngredient,
    Recomment,
)


@admin.action(description="선택한 글의 유저를 비활성화 시킵니다.")
def deactivate_users(model_admin, request, articles):
    for article in articles.all():
        user = article.author
        user.is_active = False
        user.save()
        print("비활성화 완료!")


class WordFilter(admin.SimpleListFilter):
    title = "악성유저 골라내기"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("cookai", "cookai를 언급한 댓글"),
            ("욕", "대충 욕하는 댓글"),
            ("금지어", "대충 금지어 언급하는 댓글"),
        ]

    def queryset(self, request, comments):
        word = self.value()
        if word:
            return comments.filter(comment__contains=word)
        else:
            return comments


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = (deactivate_users,)
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_display = (
        "author",
        "category",
        "title",
        "content",
        "updated_at",
        "created_at",
        "recipe",
        "image",
        "tag_list",
    )

    list_filter = (
        "author",
        "category",
        "recipe",
        "like",
        "bookmark",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "^author__username",
        "tags",
        "category",
        "recipe",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_display = (
        "author",
        "article",
        "comment",
        "updated_at",
        "created_at",
    )
    list_filter = (
        WordFilter,
        "author",
        "article",
        "comment",
        "created_at",
        "updated_at",
    )


@admin.register(Recomment)
class RecommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "info",
    )
    list_filter = ("info", "name")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "ingredient_name",
        "ingredient_info",
        "updated_at",
    )
    list_filter = ("ingredient_name", "ingredient_info", "updated_at")


@admin.register(IngredientLink)
class IngredientLinkAdmin(admin.ModelAdmin):
    list_display = (
        "link",
        "link_img",
        "price",
        "created_at",
    )
    list_filter = ("link", "link_img", "created_at", "price")


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    list_display = ["tag_list"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
