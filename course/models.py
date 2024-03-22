import uuid
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # slugify title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="uploads", blank=True, null=True)

    def __str__(self):
        return self.title

    # fetch default image if not provided in the input
    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return "https://cdn-icons-png.flaticon.com/512/2936/2936719.png"

    # slugify title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)


class Lesson(models.Model):

    DRAFT = "draft"
    PUBLISHED = "published"

    CHOICES_STATUS = (
        (DRAFT, "Draft"),
        (PUBLISHED, "published"),
    )

    ARTICLE = "article"
    QUIZ = "quiz"

    CHOICES_LESSON_TYPE = (
        (ARTICLE, "Article"),
        (QUIZ, "Quiz"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=PUBLISHED)
    type = models.CharField(max_length=20, choices=CHOICES_LESSON_TYPE, default=ARTICLE)

    def __str__(self):
        return self.title

    # slugify title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    lesson = models.ForeignKey(
        Lesson, related_name="comments", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="comments", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
