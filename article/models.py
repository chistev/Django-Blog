from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # generate a slug based on the post title
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', default='uncategorized')

    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    is_edited = models.BooleanField(default=False)

    post = RichTextField(blank=True, null=True)

    def get_api_like_url(self):
        return reverse('article:like-api', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Generate a slug based on the post title
        self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.post[:300] + '...'

    def get_absolute_url(self):
        return reverse('article:detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comment_likes", blank=True)
    edited_comment = models.TextField(blank=True, null=True)
    is_edited = models.BooleanField(default=False)

    def get_api_like_url(self):
        return reverse('article:comment-like-api', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.user}'s comment"
