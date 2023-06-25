from django.db import models
from taggit.managers import TaggableManager
from users.models import User


# Create your models here.
class Category(models.Model):
    """카테고리 모델

    Attributes:
    name(Char) : 카테고리 이름, 10자 제한
    info(Text) : 카테고리 설명, 50자 제한

    """

    name = models.CharField(
        max_length=10,
    )
    info = models.TextField(
        max_length=50,
    )

    def __str__(self):
        return f"{self.name} : {self.info.title()}"

    class Meta:
        verbose_name_plural = "Categories"


class Article(models.Model):

    """게시글 모델

    Attributes:
    author(ForeignKey) : 작성자 외래키, int, CASCADE
    category(ForeignKey) : 카테고리 모델 외래키, CASCADE
    title(Varchar) : 제목, 30자 제한, 필수 입력
    content(Text) : 내용, 500자 제한, 필수 입력
    created_at(Date) : 작성시간 Datetime
    updated_at(Date) : 수정시간 Datetime
    recipe(Text) : 레시피 text(html), 500자 제한
    image(Url) : 이미지, 이미지Url로 불러오기
    like(MtoM) : User모델과 MtoM, 역참조 : Likes, 빈 값 가능, 중간 모델 : Like
    bookmark(MtoM) : User모델과 MtoM, 역참조 : Bookmarks, 빈 값 가능, 중간 모델 : Bookmark

    """

    class Meta:
        db_table = "Article"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
        default="",
        null=False,
    )
    content = models.TextField(
        max_length=500,
        default="",
        null=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    recipe = models.TextField(
        blank=True,
        null=True,
    )
    image = models.URLField(blank=True, null=True)
    like = models.ManyToManyField(
        User,
        related_name="likes",
        blank=True,
    )
    bookmark = models.ManyToManyField(
        User,
        related_name="bookmarks",
        blank=True,
    )
    tags = TaggableManager(
        blank=True,
    )

    def __str__(self):
        return str(self.title)

    def tag_list(self):
        tags = ""
        for tag in self.tags.all():
            tags += f"{tag.name},"
        result = tags[0:-1]
        return result


class Comment(models.Model):

    """댓글 모델
    게시글에 작성할 댓글 모델입니다!


    Attributes:

    author(OtoO) : 작성자 int(역참조 : comments)
    article(ForeignKey) : 글 int
    comment(text) : 댓글 내용, 300자 제한, str
    updated_at (date): 수정시간
    created_at (date): 가입시간
    """

    class meta:
        db_table = "Comment"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    comment = models.TextField(
        max_length=300,
    )
    like = models.ManyToManyField(
        User,
        related_name="like_comments",
        blank=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.article)


# 재료 DB 모델
class Ingredient(models.Model):
    ingredient_name = models.CharField(
        max_length=100,
        primary_key=True,
    )
    ingredient_info = models.TextField(
        null=True,
        default=list,
        max_length=100,
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.ingredient_name)


# 레시피 재료 모델
class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    ingredient_quantity = models.IntegerField(
        null=False,
        default=list,
    )
    ingredient_unit = models.CharField(
        null=False,
        default=list,
        max_length=100,
    )

    def __str__(self):
        return str(self.ingredient)


class IngredientLink(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    link = models.URLField(
        max_length=200,
        null=True,
        blank=True,
    )
    link_img = models.URLField(
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.ingredient)
